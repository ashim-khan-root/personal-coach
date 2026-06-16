# Free AI Model Providers — Configuration Guide

## Quick Reference

| Provider | Free Tier | Models | Sign Up |
|----------|-----------|--------|---------|
| **Ollama** (local) | Unlimited | llama3.2, qwen, deepseek | Already installed |
| **Ollama Cloud** | Light usage, no CC | gpt-oss:20b/120b, qwen3-coder:480b | ollama.com |
| **NVIDIA NIM** | 46 models, 40 RPM, no CC | MiniMax M2.7, Llama 4, Qwen3 Coder | build.nvidia.com |
| **Google Gemini** | 1,500 req/day, 10 RPM, no CC | Gemini 2.5 Flash | ai.google.dev |
| **Groq** | 1,000 req/day, 30 RPM, no CC | Llama 3.1 70B, Mixtral | console.groq.com |
| **Cerebras** | 1M tokens/day, no CC | gpt-oss-120b, zai-glm-4.7 | cloud.cerebras.ai |
| **OpenRouter** | ~28 free models, no CC | DeepSeek R1, Qwen3, Gemma 3 | openrouter.ai |

---

## Option 1: Ollama (Already Set Up)

Already installed in the coach. No API key needed.

```bash
# List installed models
ollama list

# Run a local model
ollama run llama3.2

# Run a cloud model (free tier, needs ollama.com account)
ollama signin      # link your account
ollama run qwen3-coder:480b-cloud
```

**Best for:** Privacy, offline use, zero cost.

---

## Option 2: NVIDIA NIM (46 Free Models, No Credit Card)

1. Go to https://build.nvidia.com
2. Sign in (GitHub/Google account)
3. Open any model → click **Get API Key**
4. Copy your `nvapi-...` key

**OpenAI-compatible endpoint:**
```
https://integrate.api.nvidia.com/v1
```

**Test:**
```bash
curl -s "https://integrate.api.nvidia.com/v1/chat/completions" ^
  -H "Authorization: Bearer nvapi-<your-key>" ^
  -H "Content-Type: application/json" ^
  -d "{\"model\":\"meta/llama-4-maverick\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}"
```

**Best models:** `meta/llama-4-maverick` (general), `minmax/minimax-m2-7` (coding), `qwen/qwen3-coder-480b` (agentic coding).

---

## Option 3: Google Gemini (No Credit Card)

1. Go to https://aistudio.google.com
2. Click **Get API Key** → create key
3. Copy your key

**Endpoint:**
```
https://generativelanguage.googleapis.com/v1beta/openai/
```

**Note:** Free tier is 1,500 req/day, 10 RPM. No credit card required.

---

## Option 4: Groq (No Credit Card, Fastest)

1. Go to https://console.groq.com
2. Sign up → **API Keys** → create key
3. Copy your `gsk_...` key

**Endpoint:**
```
https://api.groq.com/openai/v1
```

**Best for:** Speed (315 tok/sec on Llama 70B). 1,000 req/day free.

---

## Option 5: OpenRouter (One Key, 28+ Free Models)

1. Go to https://openrouter.ai
2. Sign up → **Keys** → create key
3. Add $10 once to unlock 1,000 req/day (still free models, no ongoing cost)

**Endpoint:**
```
https://openrouter.ai/api/v1
```

**Best for:** A single key that routes to any model provider. Free models include DeepSeek R1, Llama 3.3 70B, Qwen3 Coder.

---

## Configuring OpenCode to Use a Different Model

OpenCode uses the model configured in its own settings. To switch:

### Option A: Environment Variables

```bash
# For OpenAI-compatible providers (NVIDIA, Groq, OpenRouter, Gemini)
set OPENAI_API_KEY=nvapi-<your-key>
set OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1

# Then run opencode in the same terminal
opencode
```

### Option B: OpenCode Config File

Edit `~/.config/opencode/config.json` (or `%USERPROFILE%\.config\opencode\config.json` on Windows):

```json
{
  "provider": "openai",
  "apiKey": "nvapi-<your-key>",
  "baseUrl": "https://integrate.api.nvidia.com/v1",
  "model": "meta/llama-4-maverick"
}
```

---

## Coach-Specific Notes

- **Ollama** is already configured for local inference (`llama3.2:3b`)
- **LightRAG** uses Ollama for embeddings — no cloud dependency
- **All coach tools** (seo_audit, task_manager, site_survey, etc.) are pure Python — they work with any model or none
- **MCP server** (`mcp_server.py`) exposes all tools over stdio — any AI agent that speaks MCP can use it
- **Understand-Anything** and **Prompt Master** are skills that work regardless of the underlying model

---

## Stacking Strategy (Maximize Free Usage)

1. **Default:** Ollama local or Ollama Cloud free tier
2. **Heavy tasks:** NVIDIA NIM (46 models, 40 RPM)
3. **Speed-critical:** Groq (fastest inference)
4. **Fallback:** OpenRouter (one key, many free models)

All use OpenAI-compatible APIs — swap the endpoint and key, everything else stays the same.
