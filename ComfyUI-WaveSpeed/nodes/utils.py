# utils.py — versão final e funcional (comprovada por você)
import requests
from PIL import Image
from io import BytesIO

def image_to_temp_url(image_tensor, output_format="jpeg"):
    if image_tensor.ndim == 4:
        image_tensor = image_tensor[0]

    img_np = (image_tensor.cpu().numpy() * 255).astype("uint8")
    pil_img = Image.fromarray(img_np, mode="RGB")

    buffer = BytesIO()
    pil_img.save(buffer, format=output_format.upper())
    buffer.seek(0)

    try:
        # ✅ Funcionando: temp.sh + User-Agent válido
        response = requests.post(
            "https://temp.sh/upload",
            files={"file": (f"img.{output_format}", buffer, f"image/{output_format}")},
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        response.raise_for_status()
        url = response.text.strip()
        if not url.startswith("http"):
            raise ValueError(f"URL inválida: {url}")
        return url
    except Exception as e:
        raise RuntimeError(f"Falha ao fazer upload da imagem: {e}")