#!/usr/bin/env python3
"""
Test Ollama LLM setup: Connect to local Ollama server, run a prompt, print result.
Requires: requests, gradio (pip install requests gradio)
"""

import requests
import sys
import gradio as gr

OLLAMA_URL = "http://localhost:11434"
PROMPT = "Say hello, Ollama!"

def get_first_model() -> str:
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        models = data.get("models", [])
        if not models:
            raise Exception("No models found in Ollama.")
        return models[0]["name"]
    except Exception as e:
        print(f"Error fetching models: {e}")
        sys.exit(1)

def run_ollama(prompt: str, model: str) -> str:
    payload = {"model": model, "prompt": prompt}
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, stream=True, timeout=30)
        if resp.status_code == 404:
            # Try /api/chat endpoint (newer Ollama)
            chat_payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
            chat_resp = requests.post(f"{OLLAMA_URL}/api/chat", json=chat_payload, stream=True, timeout=30)
            if chat_resp.status_code == 404:
                return "Error: Neither /api/generate nor /api/chat endpoints found. Check your Ollama version."
            chat_resp.raise_for_status()
            output = ""
            for line in chat_resp.iter_lines():
                if not line:
                    continue
                try:
                    import json
                    data = json.loads(line)
                    # /api/chat streams 'message' key with 'content'
                    if "message" in data and "content" in data["message"]:
                        output += data["message"]["content"]
                except Exception:
                    continue
            return output.strip()
        resp.raise_for_status()
        output = ""
        for line in resp.iter_lines():
            if not line:
                continue
            try:
                import json
                data = json.loads(line)
                output += data.get("response", "")
            except Exception:
                continue
        return output.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    # Check if --ui flag is passed
    if "--ui" in sys.argv:
        launch_ui()
    else:
        # CLI mode
        prompt = sys.argv[1] if len(sys.argv) > 1 else PROMPT
        model = get_first_model()
        print(f"Using model: {model}")
        print(f"Sending prompt to Ollama: {prompt}")
        result = run_ollama(prompt, model)
        print("\n--- LLM Response ---\n" + result)

def gradio_chat(prompt: str, model: str) -> str:
    """Wrapper for Gradio interface"""
    if not prompt.strip():
        return "Please enter a prompt."
    result = run_ollama(prompt, model)
    return result

def launch_ui():
    """Launch Gradio web interface"""
    try:
        models = get_available_models()
        model_names = [m["name"] for m in models]
        default_model = model_names[0] if model_names else "llama2"
        
        with gr.Blocks(title="Ollama Chat Interface") as demo:
            gr.Markdown("# 🦙 Ollama Chat Interface")
            gr.Markdown("Chat with your local Ollama LLM models")
            
            with gr.Row():
                model_dropdown = gr.Dropdown(
                    choices=model_names,
                    value=default_model,
                    label="Select Model",
                    interactive=True
                )
            
            with gr.Row():
                prompt_input = gr.Textbox(
                    label="Your Prompt",
                    placeholder="Enter your prompt here...",
                    lines=3
                )
            
            with gr.Row():
                submit_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.Button("Clear")
            
            output = gr.Textbox(
                label="LLM Response",
                lines=10,
                interactive=False
            )
            
            submit_btn.click(
                fn=gradio_chat,
                inputs=[prompt_input, model_dropdown],
                outputs=output
            )
            
            clear_btn.click(
                fn=lambda: ("", ""),
                outputs=[prompt_input, output]
            )
            
            gr.Markdown("---")
            gr.Markdown("💡 **Tip:** Use `python3 ollama_test.py 'your prompt'` for CLI mode")
        
        demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
    
    except Exception as e:
        print(f"Error launching UI: {e}")
        sys.exit(1)

def get_available_models() -> list:
    """Get list of all available models"""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("models", [])
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []

if __name__ == "__main__":
    main()
