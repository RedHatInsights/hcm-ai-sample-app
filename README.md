# HCM AI Sample App

A Flask application that provides a unified API interface for different LLM providers through a simplified client architecture, with an integrated Gradio chatbot interface for easy interaction.

## ✨ Features

- **Multi-LLM Provider Support**: OpenAI and LangChain (OpenAI, Ollama) clients
- **Unified Configuration**: Single set of environment variables for all providers
- **LangChain Integration**: Access to multiple providers through LangChain unified interface  
- **Streaming Support**: Real-time response streaming for all providers
- **Gradio Chatbot Interface**: User-friendly web interface for chatting with LLM models

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

The application will be available at `http://localhost:8000` (as configured in `.flaskenv`)

## ⚙️ Configuration

The application uses environment variables for configuration. Set the appropriate variables based on your LLM provider.

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LLM_CLIENT_TYPE` | LLM client type to use. (openai, langchain) | Yes | - |
| `SUMMARY_PROMPT` | System prompt for the assistant | No | `"You are a helpful assistant."` |

#### Unified Inference Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `INFERENCE_API_KEY` | API key for the inference provider | Yes | - |
| `INFERENCE_MODEL_NAME` | Model name to use | No | `"gpt-3.5-turbo"` |
| `INFERENCE_BASE_URL` | Custom base URL for API endpoint | No | - |
| `INFERENCE_TEMPERATURE` | Response randomness (0.0-1.0, 0.0=deterministic) | No | `0.7` |
| `INFERENCE_MAX_TOKENS` | Maximum tokens to generate in response | No | `2048` |

#### LangChain Specific Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LANGCHAIN_PROVIDER` | LangChain provider type (openai, ollama) | When using LangChain | `"openai"` |

#### Legacy OpenAI Configuration (Optional)

| Variable | Description | Required | Used When |
|----------|-------------|----------|-----------|
| `OPENAI_API_KEY` | API key for OpenAI service (fallback) | No* | When `INFERENCE_API_KEY` not set |
| `OPENAI_MODEL_NAME` | Model name (fallback) | No* | When `INFERENCE_MODEL_NAME` not set |
| `OPENAI_BASE_URL` | Custom base URL (fallback) | No* | When `INFERENCE_BASE_URL` not set |

*Note: These are fallback variables. Use `INFERENCE_*` variables for unified configuration.

## 🔧 Provider Configuration

The application supports three different LLM client configurations:

### Option 1: OpenAI Client

```bash
export LLM_CLIENT_TYPE="openai"
export INFERENCE_API_KEY="your-api-key"
export INFERENCE_MODEL_NAME="gpt-4"
export INFERENCE_BASE_URL="https://api.openai.com/v1"  # Optional
export INFERENCE_TEMPERATURE="0.7"  # Optional
export INFERENCE_MAX_TOKENS="2048"  # Optional
export SUMMARY_PROMPT="You are a helpful assistant."
```

**Requirements:**
- OpenAI API key

### Option 2: LangChain with OpenAI

```bash
export LLM_CLIENT_TYPE="langchain"
export LANGCHAIN_PROVIDER="openai"
export INFERENCE_API_KEY="your-openai-api-key"
export INFERENCE_MODEL_NAME="gpt-4"
export INFERENCE_TEMPERATURE="0.7"  # Optional
export INFERENCE_MAX_TOKENS="2048"  # Optional
export SUMMARY_PROMPT="You are a helpful assistant."
```

**Requirements:**
- OpenAI API key

### Option 3: LangChain with Ollama

```bash
export LLM_CLIENT_TYPE="langchain"
export LANGCHAIN_PROVIDER="ollama"
export INFERENCE_MODEL_NAME="llama3.2"
export INFERENCE_BASE_URL="http://localhost:11434"
export INFERENCE_TEMPERATURE="0.7"  # Optional
export SUMMARY_PROMPT="You are a helpful assistant."
```

**Requirements:**
- Ollama running locally or remotely

## 📦 Installation

The application includes all LangChain dependencies by default:

```bash
# Install all dependencies (includes LangChain support)
pip install -e .
```

This includes support for:
- OpenAI through LangChain (`langchain-openai`)
- Ollama through LangChain (`langchain-ollama`)

## 💬 Chatbot Interface

The application includes a Gradio-based chatbot interface that provides a user-friendly way to interact with the LLM API.

### Running the Chatbot

1. **Start the Flask API first**:
   ```bash
   # Set required environment variables
   export LLM_CLIENT_TYPE="openai"
   export INFERENCE_API_KEY="your-api-key"
   
   # Start the API server
   flask run
   ```

2. **Run the chatbot in a separate terminal**:
   ```bash
   python chatbot.py
   ```

3. **Access the chatbot**:
   - Open your browser and go to `http://localhost:7860`
   - Start chatting with your LLM!

### Chatbot Features

- **Streaming Responses**: Real-time response display as the LLM generates text
- **Chat History**: Conversation history is maintained during the session
- **Error Handling**: User-friendly error messages when the API is unavailable
- **Responsive UI**: Modern Gradio interface with chat bubbles and formatting
- **Flagging Options**: Ability to flag responses (Like, Spam, Inappropriate, Other)

### Docker Deployment

You can also run the chatbot using Docker:

```bash
# Build the chatbot image
docker build -f Dockerfile.chatbot -t chatbot .

# Run the chatbot (make sure API is running on port 8000)
docker run -p 7860:7860 \
  -e INFERENCE_BACKEND_HOST="http://host.docker.internal:8000" \
  chatbot
```

**Access points**:
- **Chatbot Interface**: http://localhost:7860
- **Flask API**: http://localhost:8000

### Configuration

The chatbot can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `INFERENCE_BACKEND_HOST` | URL of the Flask API | `http://localhost:8000` |
| `GRADIO_SERVER_NAME` | Gradio server bind address | `127.0.0.1` |
| `GRADIO_SERVER_PORT` | Gradio server port | `7860` |

## Bonfire Deployment

The application is prepared to deploy on ephemeral cluster through bonfire.

### Deployment on Ephemeral Environment

For deploying on ephemeral environments, use the provided `deploy_on_ephemeral.sh` script:

```bash
./deploy_on_ephemeral.sh <API_KEY> <NAMESPACE>
```

**Example:**
```bash
./deploy_on_ephemeral.sh "your-api-key-here" "my-ephemeral-namespace"
```

#### Namespace Management

Before deploying, you need to obtain a namespace. You have two options:

1. **Reserve a new namespace:**
   ```bash
   bonfire namespace reserve
   ```

2. **Use an existing reserved namespace:**
   ```bash
   # List your available namespaces
   bonfire namespace list
   
   # Use one of the listed namespaces in the deployment command
   ./deploy_on_ephemeral.sh "your-api-key" "existing-namespace-name"
   ```

#### Security Features

The `deploy_on_ephemeral.sh` script includes important security measures:

- **🔒 Secure Secret Management**: The script automatically creates the necessary secrets in the Kubernetes cluster
- **🛡️ No Credentials in Repository**: Prevents potential security vulnerabilities by keeping API keys and sensitive credentials out of the repository
- **✅ Safe Deployment**: Ensures credentials are handled securely during the deployment process

## 🚢 OpenShift Deployment

The application includes an OpenShift template for easy deployment with configurable parameters.

### Template Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `MEMORY_REQUEST` | Memory request for the API pods | `"512Mi"` |
| `MEMORY_LIMIT` | Memory limit for the API pods | `"1Gi"` |
| `CPU_REQUEST` | CPU request for the API pods | `"250m"` |
| `CPU_LIMIT` | CPU limit for the API pods | `"500m"` |
| `LLM_CLIENT_TYPE` | Type of LLM client (openai, langchain) | `"langchain"` |
| `LANGCHAIN_PROVIDER` | LangChain provider (openai, ollama) | `"openai"` |
| `INFERENCE_MODEL_NAME` | Model name for inference | `"mistral-small-24b-w8a8"` |
| `INFERENCE_BASE_URL` | Base URL for inference API | Custom endpoint |
| `INFERENCE_TEMPERATURE` | Response randomness (0.0-1.0) | `"0.7"` |
| `INFERENCE_MAX_TOKENS` | Maximum tokens to generate | `"2048"` |
| `SUMMARY_PROMPT` | System prompt for the AI assistant | `"You are a helpful assistant."` |

### Monitoring and Health Checks

The deployment includes:
- **Liveness Probe**: Checks `/health` endpoint every 10 seconds
- **Readiness Probe**: Checks `/health` endpoint every 5 seconds
- **Resource Limits**: Configurable CPU and memory limits
- **Security Context**: Runs as non-root user

### Accessing the Application

After deployment, the application will be available through the OpenShift route:

```bash
# Get the route URL
oc get route {{cookiecutter.projectName}} -o jsonpath='{.spec.host}'

# Test the health endpoint
curl https://$(oc get route {{cookiecutter.projectName}} -o jsonpath='{.spec.host}')/health

# Test the chat endpoint
curl -X POST https://$(oc get route {{cookiecutter.projectName}} -o jsonpath='{.spec.host}')/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?", "enable_stream": "False"}'
```

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
│  │ ChatApi     ││────│  │ llm.client  ││────│  │ OpenAI      ││
│  └─────────────┘│    │  └─────────────┘│    │  │ LangChain   ││
└─────────────────┘    └─────────────────┘    │  │ ├─OpenAI   ││
                                              │  │ └─Ollama   ││
                                              │  └─────────────┘│
                                              └─────────────────┘
```

### Key Components

- **Flask API**: Handles HTTP requests and responses via ChatApi
- **LLM Client**: Unified interface (`llm.client`) for different LLM providers
- **LLM Providers**: Support for OpenAI and LangChain (OpenAI/Ollama)
- **Gradio Chatbot**: Web-based chat interface that connects to the Flask API

### Features

- ✅ **Unified Interface**: Same API regardless of LLM provider type
- ✅ **Unified Configuration**: Single set of environment variables across providers
- ✅ **Streaming Support**: Real-time response streaming for all providers
- ✅ **Multiple Client Types**: OpenAI and LangChain (multi-provider)
- ✅ **LangChain Integration**: Access to OpenAI, Ollama through LangChain
- ✅ **Flexible Model Support**: Local models via Ollama, cloud models via APIs
- ✅ **Error Handling**: Comprehensive error handling and validation
- ✅ **User-Friendly Interface**: Gradio chatbot for easy interaction

## 🧪 Testing

### Test the Flask API with curl

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint (non-streaming)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?", "enable_stream": "False"}'

# Test chat endpoint (streaming)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a short story", "enable_stream": "True"}'
```

### Test the Chatbot Interface

1. **Start both services**:
   ```bash
   # Terminal 1: Start Flask API
   export LLM_CLIENT_TYPE="openai"
   export INFERENCE_API_KEY="your-api-key"
   flask run
   
   # Terminal 2: Start Chatbot
   python chatbot.py
   ```

2. **Access the chatbot**: Open `http://localhost:7860` in your browser

3. **Test features**:
   - Send a message and verify streaming response
   - Check error handling by stopping the Flask API
   - Test conversation history
   - Try the flagging options

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

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.