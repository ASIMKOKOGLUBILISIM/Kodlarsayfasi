from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import re
import requests

from mailer import send_alert_mail
from firewall import block_ip

app = FastAPI()

alerts = []
ip_counter = {}

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Security Alert Dashboard</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
body { background:#0f172a; color:#e5e7eb; font-family:Arial; padding:20px }
h1 { text-align:center }
.summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px; }
.summary-card { padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; }
.total { background:#1e40af; }
.medium-bg { background:#ca8a04; }
.critical-bg { background:#b91c1c; }
.section { margin-bottom: 30px; }
.card { padding:15px; margin:10px 0; border-radius:10px; background:#1e293b; border-left: 6px solid #64748b; }
.medium { border-left-color: #f59e0b }
.critical { border-left-color: #dc2626 }
#map { height:450px; border-radius:14px; margin-top:10px; border: 2px solid #1e293b; }
</style>
</head>
<body>
<h1>🚨 Security Alert Dashboard</h1>

<div class="summary">
  <div class="summary-card total" id="total">Toplam: 0</div>
  <div class="summary-card medium-bg" id="med_count">MEDIUM: 0</div>
  <div class="summary-card critical-bg" id="crit_count">CRITICAL: 0</div>
</div>

<div class="section">
  <h2>🌍 Saldırı Haritası (Canlı)</h2>
  <div id="map"></div>
</div>

<div class="section">
  <h2>🚩 Son Uyarılar</h2>
  <div id="alerts"></div>
</div>

<script>
let map = L.map('map').setView([39, 35], 5); // Türkiye odaklı başlar
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
let markerGroup = L.layerGroup().addTo(map);
let processedIPs = new Set(); 

async function banIP(ip) {
    if(confirm(ip + " adresini Windows Firewall üzerinden engellemek istediğine emin misin?")) {
        const res = await fetch("/ban/" + ip, { method: 'POST' });
        const data = await res.json();
        alert(data.message);
        load();
    }
}

async function load() {
    const res = await fetch("/alerts");
    const data = await res.json();
    const div = document.getElementById("alerts");
    div.innerHTML = "";
    
    let m = 0, c = 0;

    data.forEach(a => {
        if(a.severity === "CRITICAL") c++; else m++;
        
        const d = document.createElement("div");
        d.className = "card " + (a.severity === "CRITICAL" ? "critical" : "medium");
        d.innerHTML = `<b>${a.type}</b> | ${a.ip || "Sistem"} | ${a.severity} | ${a.time}`;
        div.prepend(d);

        if (a.ip && !processedIPs.has(a.ip)) {
            // Daha hızlı ve stabil olan ip-api servisi
            fetch(`http://ip-api.com/json/${a.ip}`)
            .then(r => r.json())
            .then(loc => {
                if (loc.status === "success") {
                    L.circleMarker([loc.lat, loc.lon], {
                        radius: 12, color: "#ef4444", fillColor: "#ff0000", fillOpacity: 0.9
                    })
                    .addTo(markerGroup)
                    .bindPopup(`<b>IP:</b> ${a.ip}<br><b>Şehir:</b> ${loc.city}<br><br><button onclick="banIP('${a.ip}')" style="background:red; color:white; border:none; padding:5px; cursor:pointer; width:100%">🚫 IP'YI BANLA</button>`);
                    processedIPs.add(a.ip);
                }
            }).catch(e => console.log("Harita hatası:", e));
        }
    });

    document.getElementById("total").innerText = "Toplam: " + data.length;
    document.getElementById("med_count").innerText = "MEDIUM: " + m;
    document.getElementById("crit_count").innerText = "CRITICAL: " + c;
}

load();
setInterval(load, 5000); // 5 saniyede bir günceller
</script>
</body>
</html>
"""

@app.get("/alerts")
def get_alerts():
    return alerts

@app.post("/ban/{ip}")
def manual_ban(ip: str):
    block_ip(ip) # firewall.py'daki fonksiyonu çağırır
    return {"message": f"{ip} başarıyla Windows Firewall'a eklendi."}

@app.post("/logs")
def receive_log(data: dict):
    log = data["log"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "failed password" in log.lower():
        ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', log)
        ip = ip_match.group() if ip_match else None
        
        alerts.append({
            "type": "FAILED_LOGIN",
            "log": log,
            "ip": ip,
            "severity": "MEDIUM",
            "time": time
        })

        if ip:
            ip_counter[ip] = ip_counter.get(ip, 0) + 1
            if ip_counter[ip] >= 3:
                alerts.append({
                    "type": "BRUTE_FORCE",
                    "ip": ip,
                    "severity": "CRITICAL",
                    "time": time
                })
                block_ip(ip)
                send_alert_mail("BRUTE FORCE", "CRITICAL", ip, "Bilinmiyor", ip_counter[ip])
    return {"ok": True}
