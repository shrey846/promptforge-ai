import sys
import os
import socket
import webbrowser
import uvicorn

def find_available_port(start_port=8000, max_attempts=20):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return start_port

def main():
    host = "127.0.0.1"
    port = find_available_port(8000)
    url = f"http://{host}:{port}"
    
    print("=" * 65)
    print("  PROMPTFORGE AI -- Advanced Prompt Optimizer & Studio")
    print("=" * 65)
    print(f"  -> Local Dashboard:  {url}")
    print(f"  -> API Documentation: {url}/docs")
    print(f"  -> 16+ Metric Evaluation Engine Active")
    print(f"  -> Multi-Model Optimizers: ChatGPT, Gemini, Claude, Universal")
    print("=" * 65)
    print("  Starting server... Press Ctrl+C to stop.\n")
    
    # Auto-open browser
    try:
        webbrowser.open(url)
    except Exception:
        pass

    # Run Uvicorn server
    uvicorn.run("backend.app:app", host=host, port=port, reload=False, log_level="info")

if __name__ == "__main__":
    main()
