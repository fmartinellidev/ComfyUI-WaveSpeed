# node_image_uploader.py
import requests
import torch
import numpy as np
from PIL import Image
from io import BytesIO
import os

class WaveSpeedImageUploader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "ou defina WAVESPEED_API_KEY"
                }),
                "output_format": (["png", "jpeg"], {"default": "png"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_url",)
    FUNCTION = "upload"
    CATEGORY = "api node/image/WaveSpeed"
    DISPLAY_NAME = "WaveSpeed Image Uploader (Official)"
    NODE_ID = "WaveSpeedImageUploader"

    def upload(self, image: torch.Tensor, api_key: str, output_format: str):
        final_api_key = api_key.strip() or os.getenv("WAVESPEED_API_KEY", "").strip()
        if not final_api_key:
            raise ValueError("API key não fornecida.")

        if image.ndim == 4:
            image = image[0]

        img_np = (image.cpu().numpy() * 255).astype("uint8")
        pil_img = Image.fromarray(img_np, mode="RGB")

        buffer = BytesIO()
        if output_format == "png":
            pil_img.save(buffer, format="PNG")
        else:
            pil_img.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)

        upload_url = "https://api.wavespeed.ai/api/v3/media/upload/binary"
        headers = {"Authorization": f"Bearer {final_api_key}"}
        files = {"file": (f"image.{output_format}", buffer, f"image/{output_format}")}

        try:
            print("📤 Upload oficial no WaveSpeed...")
            response = requests.post(upload_url, headers=headers, files=files, timeout=30)
            response.raise_for_status()
            data = response.json()

            # ✅ Extrai download_url de data e remove espaços
            image_url = data.get("data", {}).get("download_url", "").strip()
            if not image_url.startswith("http"):
                raise ValueError(f"download_url não encontrada. Resposta: {data}")

            print(f"✅ URL oficial do WaveSpeed: {image_url}")
            return (image_url,)

        except Exception as e:
            raise RuntimeError(f"Falha no upload: {e}")