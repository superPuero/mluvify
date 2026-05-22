import subprocess
import os
import sys

FRONTEND_DIR = "mluvify_fe"  
BACKEND_DIR = "mluvify_be"
BACKEND_SERVER_FILE = "server.py"  

BACKEND_SERVER_FILE_FULL = os.path.join(BACKEND_DIR, BACKEND_SERVER_FILE);

def build_frontend():
    print("Building svelte frontend")
    
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    
    try:
        result = subprocess.run(
            [npm_cmd, "run", "build"],
            cwd=FRONTEND_DIR,
            check=True,
            text=True
        )                
        print("Frontend build complete")
    except subprocess.CalledProcessError as e:
        print("Frontend build failed, see the error above")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Could not find npm, make sure Node.js is installed")
        sys.exit(1)

def start_server():
    print("Starting FastAPI server")
    
    try:
        subprocess.run([sys.executable, BACKEND_SERVER_FILE_FULL])
        
    except KeyboardInterrupt:
        print("Server stopped.")
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists(FRONTEND_DIR):
        print(f"Error: Frontend directory '{FRONTEND_DIR}' not found")
        sys.exit(1)        
        
    if not os.path.exists(BACKEND_DIR):
        print(f"Error: Frontend directory '{FRONTEND_DIR}' not found")
        sys.exit(1)

    if not os.path.exists(BACKEND_SERVER_FILE_FULL):
        print(f"Error: Frontend directory '{BACKEND_SERVER_FILE_FULL}' not found")
        sys.exit(1)

    build_frontend()
    start_server()