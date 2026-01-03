# node_apikey_loader.py

class WaveSpeedAPIKeyLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False, "default": "", "placeholder": "ex: ws_sk_xxxxxxxx"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("api_key",)
    FUNCTION = "load"
    CATEGORY = "api node/utility/WaveSpeed"
    DISPLAY_NAME = "WaveSpeed API Key Loader"
    NODE_ID = "WaveSpeedAPIKeyLoader"

    def load(self, api_key):
        key = api_key.strip()
        if not key:
            raise ValueError("API key não pode estar vazia.")
        #if not key.startswith("ws_sk_"):
            # Apenas aviso — não impede (algumas chaves podem não seguir padrão)
            #print("⚠️ Aviso: sua chave não começa com 'ws_sk_' — verifique se está correta.")
        return (key,)