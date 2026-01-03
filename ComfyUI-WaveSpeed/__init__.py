# __init__.py — wavespeed
from .node_wavespeed_api import WaveSpeedAPINode
from .node_apikey_loader import WaveSpeedAPIKeyLoader
from .node_image_uploader import WaveSpeedImageUploader

NODE_CLASS_MAPPINGS = {
    "WaveSpeedAPI": WaveSpeedAPINode,                      # ← ID genérico
    "WaveSpeedAPIKeyLoader": WaveSpeedAPIKeyLoader,
    "WaveSpeedImageUploader": WaveSpeedImageUploader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WaveSpeedAPI": "WaveSpeed API (Generic)",            # ← nome claro e reutilizável
    "WaveSpeedAPIKeyLoader": "WaveSpeed API Key Loader",
    "WaveSpeedImageUploader": "WaveSpeed Image Uploader (Official)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]