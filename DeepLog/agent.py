import requests
import time

URL = "http://127.0.0.1:8000/logs"

# 3 Farklı ülkeden simüle edilmiş IP adresleri
attack_scenarios = [
    {"country": "Turkiye", "ip": "176.236.0.1", "count": 3},
    {"country": "Hollanda", "ip": "145.15.20.10", "count": 3},
    {"country": "ABD", "ip": "66.249.66.1", "count": 3}
]

print("Saldırı simülasyonu başlatılıyor...")

for scenario in attack_scenarios:
    print(f"--- {scenario['country']} konumlu loglar gönderiliyor ({scenario['ip']}) ---")
    
    for i in range(scenario['count']):
        log_message = f"Failed password for admin from {scenario['ip']}"
        try:
            response = requests.post(URL, json={"log": log_message})
            if response.status_code == 200:
                print(f"[OK] Log gönderildi: {i+1}/3")
            else:
                print(f"[HATA] Sunucu yanıtı: {response.status_code}")
        except:
            print("[HATA] Sunucuya bağlanılamadı! FastAPI'nin çalıştığından emin ol.")
        
        time.sleep(1) # Daha hızlı test için süreyi biraz kısalttım

print("\nTüm loglar gönderildi. Dashboard'u kontrol edebilirsin.")