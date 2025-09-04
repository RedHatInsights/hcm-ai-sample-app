import os
import gradio as gr
import requests
import json

inference_backend = os.getenv("INFERENCE_BACKEND_HOST", "http://localhost:8000")
app_name = os.getenv("APP_NAME", "{{ cookiecutter.project_name }}")

def ask(message, history):
    """
    Send a message to the LLM API and stream the response.
    
    Args:
        message (str): The user's message to send to the LLM
        history: Chat history (not used in current implementation)
        
    Yields:
        str: Streamed response chunks from the LLM
    """
    try:
        # Prepare the request payload
        payload = {
            "prompt": message,
            "enable_stream": "True"
        }
        
        # Make the POST request with streaming enabled
        response = requests.post(
            f"{inference_backend}/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            stream=True,
            timeout=30
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Process the streaming response
        accumulated_response = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    # Parse the JSON chunk
                    chunk_data = json.loads(line)
                    content = chunk_data.get("content", "")
                    
                    # Check for errors in the chunk
                    if "error" in chunk_data:
                        error_msg = chunk_data["error"]
                        yield f"Error: {error_msg}"
                        return
                    
                    # Accumulate and yield the response
                    accumulated_response += content
                    yield accumulated_response
                    
                except json.JSONDecodeError:
                    # Skip malformed JSON lines
                    continue
                    
    except requests.exceptions.ConnectionError as e:
        yield f"❌ Cannot connect to the LLM API server at {inference_backend}\n\nPlease make sure the Flask API is running:\n1. Open a terminal\n2. Navigate to the project directory\n3. Run: flask run\n\nThe server should start on port 8000."
    except requests.exceptions.RequestException as e:
        yield f"❌ Request error: {str(e)}"
    except Exception as e:
        yield f"❌ Unexpected error: {str(e)}"

# Load custom CSS from file
def load_css():
    """Load custom CSS styles from external file"""
    import os
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(script_dir, "chatbot_styles.css")
    
    try:
        with open(css_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback CSS if file is not found
        return """
        .primary {
            background: linear-gradient(135deg, #EE0000 0%, #CC0000 100%) !important;
            border: none !important;
            color: white !important;
            border-radius: 4px !important;
        }
        .primary:hover {
            background: linear-gradient(135deg, #CC0000 0%, #AA0000 100%) !important;
            transform: translateY(-1px) !important;
        }
        """

custom_css = load_css()

demo = gr.ChatInterface(
    ask,
    type="messages",
    flagging_mode="manual",
    flagging_options=["👍 Like", "🚫 Spam", "⚠️ Inappropriate", "📝 Other"],
    save_history=True,
    css=custom_css,
    title=f"🔴 {app_name}",
    description="Enterprise-grade AI assistant powered by Red Hat's advanced language models and infrastructure",
)

if __name__ == "__main__":
    # Get server configuration from environment variables
    server_name = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    
    demo.launch(
        server_name=server_name,
        server_port=server_port,
        share=False
    )
