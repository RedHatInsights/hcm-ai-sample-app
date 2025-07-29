# HCM AI Sample App

A Flask application that provides a unified API interface for different LLM providers through a simplified client architecture.

## 🚀 Quick Start

### Installation

1. Create a virtual environment:

```bash
uv venv
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate
```

3. Install dependencies
```bash
uv pip install -e .
```

### Run the Application

```bash
flask run
```

The application will be available at `http://localhost:5000`

## ⚙️ Configuration

The application uses environment variables for configuration. Set the appropriate variables based on your LLM provider.

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LLM_CLIENT_TYPE` | LLM client type to use. (openai, llama_stack) | Yes | - |
| `SUMMARY_PROMPT` | System prompt for the assistant | No | `"You are a helpful assistant."` |

#### Llama Stack Specific Variables

| Variable | Description | Required | Used When |
|----------|-------------|----------|-----------|
| `ENABLE_OLLAMA` | Enable Ollama provider | When using local | `LLM_CLIENT_TYPE=llama_stack` |
| `SAFETY_MODEL` | Ollama model name | When using Ollama | `ENABLE_OLLAMA=ollama` |
| `ENABLE_VLLM` | Enable remote VLLM provider | When using remote | `LLM_CLIENT_TYPE=llama_stack` |
| `VLLM_URL` | Remote VLLM endpoint URL | When using VLLM | `ENABLE_VLLM=remote-vllm` |
| `VLLM_API_TOKEN` | API token for VLLM endpoint | When using VLLM | `ENABLE_VLLM=remote-vllm` |
| `VLLM_INFERENCE_MODEL` | Model name for VLLM inference | When using VLLM | `ENABLE_VLLM=remote-vllm` |

#### OpenAI Compatible Providers

| Variable | Description | Required | Used When |
|----------|-------------|----------|-----------|
| `OPENAI_API_KEY` | API key for OpenAI-compatible service | Yes | `LLM_CLIENT_TYPE=openai` |
| `OPENAI_MODEL_NAME` | Model name to use | Yes | `LLM_CLIENT_TYPE=openai` |
| `OPENAI_BASE_URL` | Custom base URL for API endpoint | No | `LLM_CLIENT_TYPE=openai` |

## 🔧 Provider Configuration

The application supports three different LLM client configurations:

### Option 1: Llama Stack with Local Ollama

```bash
export LLM_CLIENT_TYPE="llama_stack"
export ENABLE_OLLAMA="ollama"
export SAFETY_MODEL="llama3.2:3b-instruct-fp16"
export SUMMARY_PROMPT="You are a helpful assistant."
```

**Requirements:**
- Ollama must be installed and running locally
- The specified model must be available in Ollama

### Option 2: Llama Stack with Remote VLLM

```bash
export LLM_CLIENT_TYPE="llama_stack"
export ENABLE_VLLM="remote-vllm"
export VLLM_URL="https://your-vllm-endpoint.com:443/v1"
export VLLM_API_TOKEN="your-api-token"
export VLLM_INFERENCE_MODEL="mistral-small-24b-w8a8"
export SUMMARY_PROMPT="You are a helpful assistant."
```

**Requirements:**
- Access to a remote VLLM service
- Valid API token for the service

### Option 3: OpenAI-Compatible Service

```bash
export LLM_CLIENT_TYPE="openai"
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL_NAME="mistral-small-24b-w8a8"
export OPENAI_BASE_URL="https://your-custom-endpoint.com:443/v1"
export SUMMARY_PROMPT="You are a helpful assistant."
```

**Requirements:**
- Access to OpenAI-compatible API service
- Valid API key for the service

**Note:** For standard OpenAI service, omit `OPENAI_BASE_URL` or set it to `https://api.openai.com/v1`

## 📡 API Endpoints

### Health Check

Check if the application is running:

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "message": "HCM AI Sample App is running!"
}
```

### Chat API

#### Non-Streaming Chat

Send a message and get a complete response:

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is artificial intelligence?",
    "enable_stream": "False"
  }'
```

**Response:**
```json
{
  "result": "Artificial intelligence (AI) is a branch of computer science..."
}
```

#### Streaming Chat

Send a message and get a streamed response:

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short story about space exploration",
    "enable_stream": "True"
  }'
```

**Response:** Stream of JSON objects:
```json
{"content": "In"}
{"content": " the"}
{"content": " year"}
{"content": " 2150..."}
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The message to send to the LLM |
| `enable_stream` | string | Yes | `"True"` for streaming, `"False"` for complete response |

## 🛠️ Architecture

The application uses a unified client architecture that abstracts different LLM providers:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask API     │    │    LLM Client   │    │   LLM Provider  │
│                 │    │                 │    │                 │
│  ┌─────────────┐│    │  ┌─────────────┐│    │  ┌─────────────┐│
│  │ ChatApi     ││────│  │ llm.client  ││────│  │ Llama Stack ││
│  └─────────────┘│    │  └─────────────┘│    │  │ + Ollama    ││
└─────────────────┘    └─────────────────┘    │  │ + VLLM      ││
                                              │  │ OpenAI API  ││
                                              │  └─────────────┘│
                                              └─────────────────┘
```

### Key Components

- **Flask API**: Handles HTTP requests and responses via ChatApi
- **LLM Client**: Unified interface (`llm.client`) for different LLM providers
- **LLM Providers**: Support for Llama Stack (with Ollama/VLLM) and OpenAI-compatible APIs

### Features

- ✅ **Unified Interface**: Same API regardless of LLM provider type
- ✅ **Streaming Support**: Real-time response streaming for all providers
- ✅ **Multiple Client Types**: Llama Stack (local/remote) and OpenAI-compatible
- ✅ **Flexible Model Support**: Local models via Ollama, remote models via VLLM/API
- ✅ **Error Handling**: Comprehensive error handling and validation
- ✅ **Environment-based Config**: Easy configuration through environment variables

## 🧪 Testing

### Test with curl

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test chat endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?", "enable_stream": "False"}'
```

## 🚨 Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid parameters)
- `500`: Internal Server Error (LLM provider error)

### Error Response Format

```json
{
  "error": "Error description here"
}
```

## 🔍 Configuration Tips

### Selecting the Right Client Type

- **Use Llama Stack + Ollama** when:
  - You want to run models locally
  - You have sufficient hardware resources
  - You need offline capability

- **Use Llama Stack + VLLM** when:
  - You have access to a hosted VLLM service
  - You need high-performance inference
  - You want to use custom model deployments

- **Use OpenAI-Compatible** when:
  - You want to use OpenAI, Azure OpenAI, or similar services
  - You need to integrate with existing OpenAI-compatible APIs
  - You want the simplest setup for cloud-based models

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.