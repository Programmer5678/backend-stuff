import subprocess
import signal

p1 = subprocess.Popen([
    "python",
    "-m",
    "uvicorn",
    "api.main:app",
    "--app-dir",
    "code/backend",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
])

p2 = subprocess.Popen([
    "python",
    "-m",
    "http.server",
    "8080",
    "--directory",
    "code/frontend"
])

def cleanup_and_exit():

    p1.terminate()
    p2.terminate()
    p1.wait()
    p2.wait()

# Register the handler for common termination signals
signal.signal(signal.SIGINT, cleanup_and_exit)   # Handle Ctrl+C
signal.signal(signal.SIGTERM, cleanup_and_exit)  # Handle 'kill' command

p1.wait()
p2.wait()




