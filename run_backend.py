"""
Entry point for backend on Windows.
Must set WindowsSelectorEventLoopPolicy BEFORE uvicorn creates its event loop,
because uvicorn.setup_event_loop() runs before importing the app module.
"""
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, loop="none")
