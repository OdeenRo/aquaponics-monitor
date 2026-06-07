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
        #status { padding: 0.5rem 2rem; font-size: 0.75rem; color: #546e7a; }
        .section { padding: 1.5rem 2rem 0.5rem; }
        .section-title { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
        .section-title.real { color: #4ade80; }
        .section-title.real::before { content: ''; display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #4ade80; box-shadow: 0 0 6px #4ade80; animation: pulse 2s infinite; }
        .section-title.dummy { color: #546e7a; }
        .section-title.dummy::before { content: ''; display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #546e7a; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
        .card { background: #162330; border: 1px solid #1e3a4a; border-radius: 8px; padding: 1.2rem; }
        .card .label { font-size: 0.75rem; color: #78909c; text-transform: uppercase; letter-spacing: 0.08em; }
        .card .value { font-size: 2rem; font-weight: 700; color: #4fc3f7; margin: 0.3rem 0; }
        .card .unit { font-size: 0.8rem; color: #78909c; }
        .card .ts { font-size: 0.7rem; color: #546e7a; margin-top: 0.5rem; }
        .card.warning { border-color: #f59e0b; }
        .card.warning .value { color: #f59e0b; }
        .card.critical { border-color: #ef4444; }
        .card.critical .value { color: #ef4444; }
        .card.dummy-card { opacity: 0.5; }
        .divider { margin: 0.5rem 2rem; border: none; border-top: 1px solid #1e3a4a; }
    </style>
</head>
<body>
    <header>
        <h1>APMF</h1>
        <span>Live sensor data</span>
    </header>
    <div id="status">Connecting...</div>
    <div class="section">
        <div class="section-title real">Real data — ESP32</div>
        <div class="grid" id="grid-real"></div>
    </div>
    <hr class="divider">
    <div class="section">
        <div class="section-title dummy">Dummy data — Simulator</div>
        <div class="grid" id="grid-dummy"></div>
    </div>
    <script>
        const REAL_LABELS = {
            temperature_air:  { label: "Air Temp", unit: "°C" },
            humidity:         { label: "Humidity", unit: "%" },
            temperature_water:{ label: "Water Temp", unit: "°C" },
        };

        const DUMMY_LABELS = {
            ph:               { label: "pH", unit: "pH" },
            dissolved_oxygen: { label: "Dissolved O₂", unit: "mg/L" },
            ammonia:          { label: "Ammonia NH₄", unit: "mg/L" },
            nitrite:          { label: "Nitrite NO₂", unit: "mg/L" },
            nitrate:          { label: "Nitrate NO₃", unit: "mg/L" },
            water_level:      { label: "Water Level", unit: "cm" },
        };

        const LABELS = { ...REAL_LABELS, ...DUMMY_LABELS };

        const THRESHOLDS = {
            ph:                { wl: 6.5,  wh: 7.8,   cl: 6.0,  ch: 8.5  },
            temperature_water: { wl: 15.0, wh: 28.0,  cl: 10.0, ch: 32.0 },
            temperature_air:   { wl: null, wh: 35.0,  cl: null, ch: 40.0 },
            dissolved_oxygen:  { wl: 5.0,  wh: null,  cl: 4.0,  ch: null },
            ammonia:           { wl: null, wh: 1.0,   cl: null, ch: 2.0  },
            nitrite:           { wl: null, wh: 1.0,   cl: null, ch: 2.0  },
            nitrate:           { wl: null, wh: 200.0, cl: null, ch: 300.0},
            humidity:          { wl: null, wh: 90.0,  cl: null, ch: 95.0 },
        };

        function alertLevel(key, value) {
            const t = THRESHOLDS[key];
            if (!t) return '';
            if ((t.ch && value >= t.ch) || (t.cl && value <= t.cl)) return 'critical';
            if ((t.wh && value >= t.wh) || (t.wl && value <= t.wl)) return 'warning';
            return '';
        }

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

        function makeCard(key, meta, reading, isDummy) {
            const card = document.createElement('div');
            if (reading) {
                const level = alertLevel(key, reading.value);
                card.className = 'card' + (level ? ' ' + level : '') + (isDummy ? ' dummy-card' : '');
                card.innerHTML = `
                    <div class="label">${meta.label}</div>
                    <div class="value">${reading.value.toFixed(2)}</div>
                    <div class="unit">${meta.unit}</div>
                    <div class="ts">${reading.timestamp}</div>`;
            } else {
                card.className = 'card' + (isDummy ? ' dummy-card' : '');
                card.innerHTML = `
                    <div class="label">${meta.label}</div>
                    <div class="value" style="color:#546e7a">—</div>
                    <div class="unit">${meta.unit}</div>`;
            }
            return card;
        }

        function renderCards(data) {
            const gridReal  = document.getElementById('grid-real');
            const gridDummy = document.getElementById('grid-dummy');
            gridReal.innerHTML = '';
            gridDummy.innerHTML = '';

            for (const [key, meta] of Object.entries(REAL_LABELS))
                gridReal.appendChild(makeCard(key, meta, data[key], false));

            for (const [key, meta] of Object.entries(DUMMY_LABELS))
                gridDummy.appendChild(makeCard(key, meta, data[key], true));
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
