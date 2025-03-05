from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Serve static files (CSS, JS if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize database
conn = sqlite3.connect("iot.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS led (id INTEGER PRIMARY KEY, state INTEGER)")
cursor.execute("INSERT OR IGNORE INTO led (id, state) VALUES (1, 0), (2, 0), (3, 0)")
conn.commit()

# Model for LED state
class LEDState(BaseModel):
    state: int

@app.get("/led/{led_id}")
async def get_led_state(led_id: int):
    cursor.execute("SELECT state FROM led WHERE id = ?", (led_id,))
    state = cursor.fetchone()
    if state:
        return {"id": led_id, "state": state[0]}
    return {"error": "LED not found"}

@app.post("/led/{led_id}")
async def set_led_state(led_id: int, led: LEDState):
    cursor.execute("UPDATE led SET state = ? WHERE id = ?", (led.state, led_id))
    conn.commit()
    return {"message": f"LED {led_id} state updated", "state": led.state}

@app.get("/led")
async def get_all_led_states():
    """Fetch states of all 3 LEDs"""
    cursor.execute("SELECT id, state FROM led")
    leds = [{"id": row[0], "state": row[1]} for row in cursor.fetchall()]
    return {"leds": leds}

# HTML page for LED control
@app.get("/", response_class=HTMLResponse)
async def led_control_page():
    with open("static/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

