# DeepLog (DerinGünlük)

Bu proje, ağ trafiğini izlemek ve güvenlik ihlallerini tespit etmek amacıyla geliştirilmiş bir güvenlik panelidir.

## 🛠️ Bileşenler ve Dosya Yapısı

### 1. Ana Kontrol Merkezi (`ana.py`)
* **FastAPI** tabanlıdır.
* Güvenlik uyarılarını ve istatistikleri bir dashboard üzerinden sunar.
* Gelen istekleri (`/`) HTML formatında görselleştirir.

### 2. Takip Modülü (`ajan.py`)
* Arka planda çalışan ve sistem hareketlerini izleyen ana casus yazılımdır.
* Şüpheli aktiviteleri tespit ederek veritabanına veya log dosyasına işler.

### 3. Güvenlik ve Bildirim (`güvenlik duvarı.py` & `posta gönderici.py`)
* **Güvenlik Duvarı:** Belirli IP adreslerini engellemek ve erişim kurallarını yönetmek için kullanılır.
* **Posta Gönderici:** Kritik bir ihlal durumunda yöneticiye anlık e-posta uyarıları iletir.

## 🚀 Kurulum ve Çalıştırma

1. Gerekli kütüphaneleri kurun:
   `pip install fastapi requests`
   
2. Sistemi başlatın:
   `python ana.py`

---
*Bu proje eğitim ve güvenlik testleri amacıyla geliştirilmiştir.*
