# node_wavespeed_api.py
import requests
import time
import os
import sys
import torch
import numpy as np
from PIL import Image
from io import BytesIO

def _print_progress(percent, status="processing", width=40):
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    sys.stdout.write(f"\r⏳ [{bar}] {int(percent)}% | {status}")
    sys.stdout.flush()

def _clear_progress():
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

class WaveSpeedAPINode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "make her smile, studio lighting"}),
                "endpoint_url": ("STRING", {
                    "multiline": False,
                    "default": "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit"
                }),
                "poll_interval": ("INT", {"default": 3, "min": 1, "max": 10}),
            },
            "optional": {
                "image_url": ("STRING", {"multiline": False, "default": ""}),
                "image": ("IMAGE",),
                "api_key": ("STRING", {"multiline": False, "default": ""}),
                "extra_payload": ("STRING", {
                    "multiline": True,
                    "default": "{}",
                    "placeholder": "JSON adicional (ex: {\"resolution\": \"2k\"})"
                }),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "request_id", "raw_response")
    FUNCTION = "generate"
    NODE_ID = "WaveSpeedAPI"
    DISPLAY_NAME = "WaveSpeed API (Generic)"
    CATEGORY = "api node/image/WaveSpeed"

    def generate(self, prompt, endpoint_url, poll_interval, image_url="", image=None, api_key="", extra_payload="{}"):
        # 1. Resolve API key
        final_api_key = api_key.strip() or os.getenv("WAVESPEED_API_KEY", "").strip()
        if not final_api_key:
            raise ValueError("API key não fornecida.")

        # 2. Resolve imagem
        if image is not None:
            print("📤 Upload da imagem no WaveSpeed CDN...")
            image_url = self._upload_to_wavespeed(image, final_api_key)
            print(f"✅ URL oficial: {image_url}")
        elif not image_url.strip():
            # ❗ Alguns endpoints não exigem imagem (ex: text-to-video)
            print("⚠️ Nenhuma imagem fornecida — verifique se o endpoint a suporta.")

        # 3. Monta payload base
        payload = {"prompt": prompt}
        if image_url:
            payload["images"] = [image_url]

        # 4. Adiciona extra_payload (JSON seguro)
        import json
        try:
            extra = json.loads(extra_payload) if extra_payload.strip() else {}
            payload.update(extra)
        except Exception as e:
            raise ValueError(f"extra_payload inválido (deve ser JSON): {e}")

        # 5. Headers
        headers = {
            "Authorization": f"Bearer {final_api_key}",
            "Content-Type": "application/json"
        }

        # 6. POST
        print(f"📤 Enviando para: {endpoint_url}")
        response = requests.post(endpoint_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        resp_json = response.json()
        raw_response_str = json.dumps(resp_json, indent=2)

        data = resp_json.get("data", {})
        request_id = data.get("id")
        get_url = data.get("urls", {}).get("get", "").strip()

        if not request_id or not get_url:
            raise RuntimeError(f"Resposta inválida. Campos ausentes: id={bool(request_id)}, get_url={bool(get_url)}")

        print(f"\n🚀 Job iniciado: {request_id}")

        # 7. Polling com progresso
        current_percent = 0
        ESTIMATED_TOTAL_SECONDS = 20  # adaptável
        steps = max(1, int(ESTIMATED_TOTAL_SECONDS / poll_interval))
        increment = 99.0 / steps

        try:
            while True:
                time.sleep(poll_interval)
                result = requests.get(get_url, headers=headers, timeout=30)
                result.raise_for_status()
                poll_data = result.json()
                poll_result = poll_data.get("data", {})
                status = poll_result.get("status")

                if status == "completed":
                    _print_progress(100.0, "done")
                    print()
                    outputs = poll_result.get("outputs", [])
                    if not outputs:
                        _clear_progress()
                        raise RuntimeError("Nenhum output retornado.")
                    # Suporta image ou video
                    output_url = outputs[0]
                    break

                elif status == "failed":
                    _clear_progress()
                    error = poll_result.get("error", "Erro desconhecido")
                    raise RuntimeError(f"Falha: {error}")

                elif status in ("pending", "processing", "created"):
                    current_percent = min(99, current_percent + increment)
                    _print_progress(current_percent, status)

                else:
                    _clear_progress()
                    raise RuntimeError(f"Status inesperado: {status}")

        except Exception as e:
            _clear_progress()
            raise

        # 8. Download (suporte a imagem apenas — para vídeo, retornar URL)
        if output_url.lower().endswith(('.png', '.jpg', '.jpeg')):
            print("📥 Baixando imagem...")
            img_response = requests.get(output_url, timeout=30)
            img_response.raise_for_status()
            pil_img = Image.open(BytesIO(img_response.content)).convert("RGB")
            image_np = np.array(pil_img).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np)[None,]
            return (image_tensor, request_id, raw_response_str)
        else:
            # Para vídeos, retornar placeholder preto + URL no raw_response
            print(f"🎬 Saída é um vídeo: {output_url}")
            placeholder = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
            return (placeholder, request_id, raw_response_str + f"\n\nVIDEO_URL: {output_url}")

    def _upload_to_wavespeed(self, image_tensor: torch.Tensor, api_key: str, output_format="png"):
        if image_tensor.ndim == 4:
            image_tensor = image_tensor[0]
        img_np = (image_tensor.cpu().numpy() * 255).astype("uint8")
        pil_img = Image.fromarray(img_np, mode="RGB")
        buffer = BytesIO()
        pil_img.save(buffer, format=output_format.upper())
        buffer.seek(0)

        upload_url = "https://api.wavespeed.ai/api/v3/media/upload/binary"
        headers = {"Authorization": f"Bearer {api_key}"}
        files = {"file": (f"img.{output_format}", buffer, f"image/{output_format}")}

        response = requests.post(upload_url, headers=headers, files=files, timeout=30)
        response.raise_for_status()
        data = response.json()
        image_url = data.get("data", {}).get("download_url", "").strip()
        if not image_url.startswith("http"):
            raise ValueError(f"download_url inválida: {data}")
        return image_url