# LDAP Web Arayüz (Flask)

Basit bir Flask arayüzü: LDAP kullanıcılarını listeleme, ekleme, güncelleme ve silme.

Çalıştırma:

1. `config.py` içindeki LDAP ayarlarını düzenleyin (`LDAP_SERVER`, `LDAP_USER`, `LDAP_PASSWORD`, `BASE_DN`).
2. Gerekli paketleri yükleyin:

```bash
python3 -m pip install -r requirements.txt
```

3. Uygulamayı başlatın:

```bash
python3 web_ui.py
```

Varsayılan olarak `http://localhost:5000` adresinde çalışır.

Not: Gerçek LDAP sunucunuzda SSL/AD şifre ayarları vb. gerekebilir. Bu örnek temel bir iskelet sunar; güvenlik ve hata kontrolleri üretimde güçlendirilmeli.
