import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from typing import List

# Setup logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

app = FastAPI()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
logging.info("📁 Static files mounted at /static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        logging.info("🚀 ConnectionManager initialized")

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logging.info(f"🔌 Client connected: {websocket.client} | Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logging.info(f"❌ Client disconnected: {websocket.client} | Remaining connections: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        logging.info(f"📣 Broadcasting message to {len(self.active_connections)} clients: {message}")
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get():
    logging.info("📄 Serving index.html")
    return HTMLResponse(open("static/index.html").read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logging.info(f"🌐 WebSocket handshake from {websocket.client}")
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            timestamp = datetime.now().strftime("%H:%M:%S")
            logging.info(f"💬 Received: {data}")
            await manager.broadcast(f"[{timestamp}] {data}")
    except WebSocketDisconnect:
        logging.warning(f"⚠️ WebSocket disconnected: {websocket.client}")
        manager.disconnect(websocket)
