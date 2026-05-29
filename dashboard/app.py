import json
import os

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Aquaponics Dashboard")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APMF</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; background: #0f1923; color: #e0e0e0; }
        header { padding: 1.5rem 2rem; background: #162330; border-bottom: 1px solid #1e3a4a; }
        header h1 { font-size: 1.4rem; color: #4fc3f7; letter-spacing: 0.05em; }
        header span { font-size: 0.8rem; color: #78909c; }
        #grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; padding: 2rem; }
        .card { background: #162330; border: 1px solid #1e3a4a; border-radius: 8px; padding: 1.2rem; }
        .card .label { font-size: 0.75rem; color: #78909c; text-transform: uppercase; letter-spacing: 0.08em; }
        .card .value { font-size: 2rem; font-weight: 700; color: #4fc3f7; margin: 0.3rem 0; }
        .card .unit { font-size: 0.8rem; color: #78909c; }
        .card .ts { font-size: 0.7rem; color: #546e7a; margin-top: 0.5rem; }
        .card.warning { border-color: #f59e0b; }
        .card.warning .value { color: #f59e0b; }
        .card.critical { border-color: #ef4444; }
        .card.critical .value { color: #ef4444; }
        #status { padding: 0.5rem 2rem; font-size: 0.75rem; color: #546e7a; }
    </style>
</head>
<body>
    <header>
        <h1>APMF</h1>
        <span>Live sensor data</span>
    </header>
    <div id="status">Connecting...</div>
    <div id="grid"></div>
    <script>
        const LABELS = {
            ph: { label: "pH", unit: "pH" },
            temperature_water: { label: "Water Temp", unit: "°C" },
            temperature_air: { label: "Air Temp", unit: "°C" },
            humidity: { label: "Humidity", unit: "%" },
            dissolved_oxygen: { label: "Dissolved O₂", unit: "mg/L" },
            ammonia: { label: "Ammonia NH₄", unit: "mg/L" },
            nitrite: { label: "Nitrite NO₂", unit: "mg/L" },
            nitrate: { label: "Nitrate NO₃", unit: "mg/L" },
            water_level: { label: "Water Level", unit: "cm" },
        };

        async function fetchData() {
            try {
                const res = await fetch('/api/sensors');
                const data = await res.json();
                renderCards(data);
                document.getElementById('status').textContent =
                    'Last update: ' + new Date().toLocaleTimeString();
            } catch (e) {
                document.getElementById('status').textContent = 'Backend unreachable';
            }
        }

        function renderCards(data) {
            const grid = document.getElementById('grid');
            grid.innerHTML = '';
            for (const [key, meta] of Object.entries(LABELS)) {
                const reading = data[key];
                const card = document.createElement('div');
                card.className = 'card';
                if (reading) {
                    card.innerHTML = `
                        <div class="label">${meta.label}</div>
                        <div class="value">${reading.value.toFixed(2)}</div>
                        <div class="unit">${meta.unit}</div>
                        <div class="ts">${reading.timestamp}</div>`;
                } else {
                    card.innerHTML = `
                        <div class="label">${meta.label}</div>
                        <div class="value" style="color:#546e7a">—</div>
                        <div class="unit">${meta.unit}</div>`;
                }
                grid.appendChild(card);
            }
        }

        fetchData();
        setInterval(fetchData, 5000);
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def dashboard() -> HTMLResponse:
    return HTMLResponse(content=HTML)


@app.get("/api/sensors")
async def proxy_sensors() -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BACKEND_URL}/sensors")
    from fastapi.responses import JSONResponse
    return JSONResponse(content=resp.json(), headers={"Cache-Control": "no-store"})


@app.post("/api/test-alert")
async def proxy_test_alert() -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BACKEND_URL}/test-alert")
        return resp.json()
