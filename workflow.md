
# Mini Slack Chat — WebSocket Workflow Documentation

This app is a minimal Slack-style chatroom using **FastAPI** and **vanilla JavaScript WebSockets**.


## Overview

* Frontend: HTML + JavaScript in `static/index.html`
* Backend: FastAPI server in `main.py`
* Real-time: Achieved using WebSockets via FastAPI’s `WebSocket` class


## Workflow: Step-by-Step Execution

### 1. Browser Requests HTML

* Browser loads: `GET /`

  * `main.py` → `get()` → `HTMLResponse(open("static/index.html").read())`

### 2. JS Code in `<script>` Executes

```js
const socket = new WebSocket("ws://" + window.location.host + "/ws");
```

* Triggers a **WebSocket Upgrade request** from browser to:

  * `GET /ws` with headers:

    * `Upgrade: websocket`
    * `Connection: Upgrade`



### 3. FastAPI Handles `/ws`

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
```

* `websocket.accept()` is called → handshake complete
* Connection added to `active_connections`



### 4. WebSocket Events in JS

```js
socket.onopen = () => logWithTime("✅ WebSocket connection established");
```

* JS confirms connection is open
* UI logs show connection is ready


### 5. User Sends Message

```js
socket.send(user + ": " + message);
```

* Triggered by clicking the “Send” button
* Formatted as: `Username: MessageText`


### 6. Backend Receives Message

```python
data = await websocket.receive_text()
timestamp = datetime.now().strftime("%H:%M:%S")
await manager.broadcast(f"[{timestamp}] {data}")
```

* Timestamped and broadcasted to all clients


### 7. Clients Receive Message

```js
socket.onmessage = function(event) {
  const text = event.data;
  // Format and append to #chatlog
}
```

* Messages are parsed and styled per user
* `hashColor(user)` gives each user a unique color



## 🔁 ASCII Sequence Diagram

```text
Client Browser           FastAPI Server              Other Clients
     |                         |                           |
     |--- HTTP GET / -------->|                           |
     |<--- index.html --------|                           |
     |                         |                           |
     |--- WS Upgrade /ws ---->|                           |
     |<-- 101 Switching ------|                           |
     |                         |                           |
     |--- send("User: Hi") -->|                           |
     |                         |--- broadcast() ---------->|
     |                         |--- broadcast() ---------->|
     |<---- [timestamp] -------|                           |
     |                         |                           |
```



## Files Involved

### static/index.html

* JS WebSocket logic
* Message formatting
* Event handlers (`onopen`, `onmessage`, etc.)

### main.py

* FastAPI app
* `ConnectionManager` for tracking clients
* `/` → serves HTML
* `/ws` → handles WebSocket upgrades + message relay



## Dev Notes

* Uses `WebSocket` class from FastAPI.
* No DB, all data is ephemeral and in-memory.
* Logs are printed on server console for debugging.

![alt text](<Screenshot 2025-05-05 at 3.34.06 PM.jpg>)