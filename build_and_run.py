import subprocess
import os
import sys

FRONTEND_DIR = "mluvify_fe"  
BACKEND_DIR = "mluvify_be"
BACKEND_SERVER_FILE = "app/main.py"  

BACKEND_SERVER_FILE_FULL = os.path.join(BACKEND_DIR, BACKEND_SERVER_FILE)

# 1. Define the path to the virtual environment
VENV_DIR = os.path.join(BACKEND_DIR, ".venv")

# 2. Get the correct Python executable path depending on the OS
if os.name == "nt":  # Windows
    VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
else:                # Mac/Linux
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")

def build_frontend():
    print("Building svelte frontend...")
    
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    
    try:
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
    
    # Ensure the virtual environment actually exists before trying to use it
    if not os.path.exists(VENV_PYTHON):
        print(f"\nError: Could not find virtual environment Python at {VENV_PYTHON}")
        print(f"Please navigate to {BACKEND_DIR} and run: python -m venv .venv")
        sys.exit(1)

    try:
        # 3. Use the VENV_PYTHON instead of sys.executable
        subprocess.run([VENV_PYTHON, BACKEND_SERVER_FILE_FULL])
        
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