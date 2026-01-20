# sockets/download_socket.py
from fastapi import WebSocket
from backend.src.core.download_manager import download_manager
connections = []

async def connect(ws: WebSocket):
    await ws.accept()
    connections.append(ws)

async def broadcast(data):
    for ws in connections:
        await ws.send_json(data)
