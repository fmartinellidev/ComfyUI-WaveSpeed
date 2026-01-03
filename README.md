# 🌊 ComfyUI-WaveSpeed

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Custom%20Node-blueviolet)](https://github.com/comfyanonymous/ComfyUI)

A **generic, flexible node** to integrate **any [WaveSpeed](https://wavespeed.ai) model** into ComfyUI — including **Nano Banana Pro**, **Wan 2.1**, **Flux**, **Kling**, **Veo**, and more.

✅ Direct upload to WaveSpeed CDN (`cloudfront.net`)  
✅ Terminal progress bar (just like KSampler)  
✅ Image & video output support  
✅ Fully configurable via `endpoint_url` — just paste from WaveSpeed Playground!  
✅ Batch prompt management with `Prompt Snippet Extractor`  
✅ Example workflow included 🎁

---

## 📦 Installation

From your `ComfyUI/custom_nodes` folder:

```bash
git clone https://github.com/fmartinellidev/ComfyUI-WaveSpeed.git
```

Or download the ZIP and extract into `ComfyUI/custom_nodes/ComfyUI-WaveSpeed`.

Restart ComfyUI.

---

## 🧩 Included Nodes

| Node | Description |
|------|-------------|
| **WaveSpeed API (Generic)** | Run any WaveSpeed endpoint (`nano-banana-pro`, `wan-2.1`, `flux-dev`, etc.) |
| **WaveSpeed API Key Loader** | Inject API key without environment variables |
| **WaveSpeed Image Uploader** | Upload directly to WaveSpeed CDN (official `cloudfront.net` URLs) |
| **Prompt Snippet Extractor** | Manage batch prompts (e.g. `001_smile\n...\n---\n002_serious\n...`) |
| **Prompt Variable Extractor** | Extract `key='value'` pairs from text (e.g. `seed='123'`) |

---

## 🛠️ `WaveSpeed API (Generic)` — Inputs & Outputs

### 🔤 Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | `STRING` | ✅ | Main prompt for generation |
| `endpoint_url` | `STRING` | ✅ | Full API endpoint (e.g. `https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit`) |
| `poll_interval` | `INT` | ✅ | Seconds between status checks (default: `3`) |
| `image` | `IMAGE` | ❌ | Input image tensor (auto-uploaded to WaveSpeed CDN) |
| `image_url` | `STRING` | ❌ | Direct image URL (overrides `image`) |
| `api_key` | `STRING` | ❌ | API key (overrides `WAVESPEED_API_KEY` env var) |
| `extra_payload` | `STRING` | ❌ | Additional JSON payload (see below) |

### 📤 Outputs

| Output | Type | Description |
|--------|------|-------------|
| `image` | `IMAGE` | Generated image (512×512 black placeholder for video) |
| `request_id` | `STRING` | WaveSpeed job ID (e.g. `a1b2c3...`) |
| `raw_response` | `STRING` | Full JSON response (useful for debugging or video URLs) |

---

## ⚙️ How to Use

### 1. **Get your API key**
Go to [WaveSpeed Dashboard → API Keys](https://wavespeed.ai/dashboard/api-keys) and copy your key.

### 2. **Find the endpoint**
In [WaveSpeed Playground](https://wavespeed.ai/playground), open DevTools (**F12 → Network tab**), run a generation, and copy the `POST` URL.

| Model | Example `endpoint_url` |
|-------|------------------------|
| **Nano Banana Pro** | `https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` |
| **Wan 2.1 + LoRA** | `https://api.wavespeed.ai/api/v3/models/wan-2.1/i2v-720p-lora` |
| **Flux Dev (T2I)** | `https://api.wavespeed.ai/api/v3/models/flux-dev/t2i` |
| **Kling V2.1 (T2V)** | `https://api.wavespeed.ai/api/v3/models/kling/v2.1/video` |

### 3. **Configure `extra_payload` (JSON)**

This field lets you send **any additional parameters** the endpoint expects.

#### 🔹 Nano Banana Pro (recommended)
```json
{
  "resolution": "2k",
  "output_format": "png"
}
```

#### 🔹 Wan 2.1 with LoRA
```json
{
  "resolution": "1080p",
  "lora_weights": [
    {
      "lora": "nano-banana-pro",
      "weight": 1.0
    }
  ]
}
```

#### 🔹 Flux Dev
```json
{
  "aspect_ratio": "16:9",
  "output_format": "png",
  "steps": 20
}
```

> 💡 Tip: Copy the payload directly from the **Request Payload** in DevTools!

---

## 🎁 Example Workflow Included

A ready-to-run workflow (`example_workflow.json`) is included in the repository — demonstrating:

- `LoadImage` → `WaveSpeed Image Uploader`  
- `Prompt Snippet Extractor` for batch expressions  
- `WaveSpeed API (Generic)` with Nano Banana Pro  
- `SaveImage` using `filename` from snippet extractor  

👉 Just load `example_workflow.json` in ComfyUI and run!

---

## 🤝 Contributions

PRs are welcome! For major changes, please open an issue first.

---

Made with ❤️ by [fmartinellidev](https://github.com/fmartinellidev) to FP8 Studio.  
Inspired by [WaveSpeed AI](https://wavespeed.ai)
```
