import subprocess
import os
import sys

FRONTEND_DIR = "mluvify_fe"  
BACKEND_DIR = "mluvify_be"
BACKEND_SERVER_FILE = "app/main.py"  

BACKEND_SERVER_FILE_FULL = os.path.join(BACKEND_DIR, BACKEND_SERVER_FILE)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, BACKEND_DIR, ".venv")

if os.name == "nt":
    VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
else:               
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")

def build_frontend():
    print("Building svelte frontend...")
    
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    
    try:
        result = subprocess.run(
            [npm_cmd, "install"],
            cwd=FRONTEND_DIR,
            check=True,
            text=True
        )   
        
        result = subprocess.run(
            [npm_cmd, "run", "build"],
            cwd=FRONTEND_DIR,
            check=True,
            text=True
        )                
        print("Frontend build complete!\n")
    except subprocess.CalledProcessError as e:
        print("Frontend build failed, see the error above")
        sys.exit(1)
    except FileNotFoundError:
        print("Could not find npm, make sure Node.js is installed")
        sys.exit(1)

def start_server():
    print(f"Starting FastAPI server using venv: {VENV_PYTHON}")
    
    if not os.path.exists(VENV_PYTHON):
        print(f"\nError: Could not find virtual environment Python at {VENV_PYTHON}")
        print(f"Please navigate to {BACKEND_DIR} and run: python -m venv .venv")
        sys.exit(1)

    try:
        subprocess.run([
            VENV_PYTHON, 
            "-m", 
            "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ], cwd=BACKEND_DIR)
        
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists(FRONTEND_DIR):
        print(f"Error: Frontend directory '{FRONTEND_DIR}' not found")
        sys.exit(1)        
        
    if not os.path.exists(BACKEND_DIR):
        print(f"Error: Backend directory '{BACKEND_DIR}' not found")
        sys.exit(1)

    if not os.path.exists(BACKEND_SERVER_FILE_FULL):
        print(f"Error: Backend server file '{BACKEND_SERVER_FILE_FULL}' not found")
        sys.exit(1)

    build_frontend()
    start_server()