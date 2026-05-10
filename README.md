# LDAPAD — LDAP Yönetim Arayüzü

Flask tabanlı web arayüzü ile Active Directory / LDAP kullanıcılarını yönetin.

## Özellikler

- **Kullanıcı Listeleme** — Tüm kullanıcıları tablo/kart görünümünde görüntüleme
- **Aktif/Pasif Filtreleme** — Toplam/Aktif/Pasif kartlarına tıklayarak listeyi filtreleme
- **Kullanıcı Ekleme** — Yeni kullanıcı oluşturma (OU seçme veya manuel girme)
- **Kullanıcı Güncelleme** — Mail, ünvan, hesap durumu düzenleme + tüm bilgileri görüntüleme
- **Kullanıcı Silme** — Kullanıcıları LDAP dizininden kaldırma
- **Mobil Uyumlu** — Bootstrap ile responsive tasarım, mobilde kart görünümü
- **İşlem Logları** — Tüm ekleme/silme/güncelleme işlemleri `audit.log` dosyasına kaydedilir
- **Web'den Ayarlar** — LDAP sunucu bilgilerini arayüzden düzenleme
- **Otomatik Yenileme** — Kullanıcı listesi 30 saniyede bir otomatik güncellenir

## Gereksinimler

- Python 3.6+
- Active Directory veya OpenLDAP sunucusu
- `pip install flask ldap3`

## Hızlı Başlangıç

```bash
git clone https://github.com/AlpVrn/LDAPAD.git
cd LDAPAD
cp config.py.example config.py
# config.py dosyasını kendi LDAP bilgilerinle düzenle
pip install -r requirements.txt
python web_ui.py
```

Tarayıcında `http://localhost:5000` adresine git.

## Ek Scriptler

Proje klasöründe bağımsız CLI scriptleri de bulunur:

| Script | İşlev |
|---|---|
| `ldappythonKullaniciCekme.py` | Kullanıcıları listele |
| `ldappythonKullaniciEkleme.py` | Yeni kullanıcı ekle |
| `ldappythonKullaniciGuncelleme.py` | Kullanıcı güncelle |
| `ldappythonKullaniciSilme.py` | Kullanıcı sil |
| `LDAPSERVERGIREBBILIYORMU.py` | Sunucu bağlantı testi |
| `ldappytdomainnameOgrenme.py` | Domain bilgisi öğren |

## Güvenlik

- `config.py` (şifre vb.) `.gitignore` ile korunur, repo'ya eklenmez
- SSL/TLS kullanılması önerilir
- Production ortamında `FLASK_DEBUG = False` yapılmalıdır

## Lisans

Açık kaynak.
