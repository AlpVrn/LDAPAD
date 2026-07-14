# LDAPAD

Active Directory / LDAP kullanıcılarını web arayüzünden yönetmek için geliştirilmiş Flask tabanlı yönetim paneli.

## Özellikler

- Kullanıcı listeleme (tablo ve mobil kart görünümü)
- Kullanıcı ekleme (OU seçimi veya manuel entry)
- Kullanıcı düzenleme (mail, ünvan, açıklama, departman, ülke, şehir, hesap durumu, manager)
- Kullanıcı silme
- Ülke seçimi (ISO 3166-1 dropdown, otomatik countryCode doldurma)
- Manager seçimi (grup bazlı cascade dropdown)
- Aktif / Pasif filtreleme
- İşlem logları (`audit.log`)
- Ayarları web'den düzenleme
- Kullanıcı listesinin otomatik yenilenmesi (30 saniye)
- Mobil uyumlu responsive tasarım (Bootstrap 5)

## Proje Yapısı

```
LDAPAD/
├── web_ui.py                 # Flask web uygulaması (ana dosya)
├── ldap_helpers.py            # LDAP bağlantı ve işlem fonksiyonları
├── countries_data.py          # Ülke listesi (ISO 3166-1)
├── config.py                  # LDAP ve Flask ayarları (repo'da yok)
├── config.py.example          # Ayarlar şablonu
├── requirements.txt           # Python bağımlılıkları
├── audit.log                  # İşlem logları
├── templates/
│   ├── index.html             # Ana sayfa (kullanıcı listesi)
│   ├── add_user.html          # Kullanıcı ekleme formu
│   ├── edit_user.html         # Kullanıcı düzenleme formu
│   ├── logs.html              # Log görüntüleme
│   └── settings.html          # Ayarlar sayfası
├── static/
│   └── js/main.js             # Frontend JavaScript
└── Terminal/
    ├── ldappythonKullaniciCekme.py
    ├── ldappythonKullaniciEkleme.py
    ├── ldappythonKullaniciGuncelleme.py
    ├── ldappythonKullaniciSilme.py
    └── ldappytdomainnameOgrenme.py
```

## Gereksinimler

- Python 3.8 veya üzeri
- Active Directory veya OpenLDAP sunucusu
- Python paketleri: `flask`, `ldap3`

## Kurulum

```bash
git clone https://github.com/AlpVrn/LDAPAD.git
cd LDAPAD
python -m venv venv
source venv/bin/activate        # Linux/Mac
pip install -r requirements.txt
```

### Ayarlar

`config.py.example` dosyasını `config.py` olarak kopyalayıp kendi LDAP sunucu bilgilerinle düzenle:

```python
LDAP_SERVER = '192.168.1.100'       # LDAP sunucu IP adresi veya hostname
LDAP_USER = 'admin@domain.local'    # Bind kullanıcı DN'i veya UPN
LDAP_PASSWORD = 'sifre'             # Bind şifresi
BASE_DN = 'dc=domain,dc=local'      # Arama yapılacak base DN

FLASK_DEBUG = True
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
```

### Çalıştırma

```bash
python web_ui.py
```

Tarayıcıda `http://localhost:5000` adresine git.

## Terminal Scriptleri

`Terminal/` klasöründeki bağımsız Python scriptleri. Her biri kendi içinde çalışır, config.py'yi kullanır.

| Script | İşlev |
|---|---|
| `ldappythonKullaniciCekme.py` | Tüm kullanıcıları LDAP'dan çeker ve listeler |
| `ldappythonKullaniciEkleme.py` | Yeni kullanıcı oluşturur, gruba ekler |
| `ldappythonKullaniciGuncelleme.py` | Kullanıcı bilgilerini ve manager'ını günceller |
| `ldappythonKullaniciSilme.py` | Kullanıcıyı LDAP'dan siler |
| `ldappytdomainnameOgrenme.py` | Domain ve sunucu bilgilerini öğrenir |

## Güvenlik

- `config.py` `.gitignore` ile korunur, repo'ya eklenmez
- Production ortamında `FLASK_DEBUG = False` yapılmalıdır
- LDAP bağlantısı için SSL/TLS kullanılması önerilir
- Web arayüzüne erişim LDAP kimlik doğrulaması gerektirmez (sadece config'deki bind hesabı kullanılır)

## Lisans

Açık kaynak.
