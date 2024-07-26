import uvicorn

def run_server():
    """
    Runs the FastAPI server.

    This function starts the FastAPI server using the Uvicorn ASGI server.
    It binds the server to the localhost (127.0.0.1) on port 4000 and enables auto-reloading.

    Usage:
        python run.py

    """
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)

# Run the server
if __name__ == '__main__':
    run_server()
