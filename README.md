# LDAPAD - LDAP Yönetim Arayüzü (Flask)

Bu proje, LDAP (Lightweight Directory Access Protocol) sunucularını yönetmek için geliştirilmiş bir Python tabanlı web uygulamasıdır. Flask framework'ü kullanarak basit ve kullanıcı dostu bir arayüz sağlar. LDAP kullanıcılarını listeleme, ekleme, güncelleme ve silme işlemlerini web üzerinden gerçekleştirebilirsiniz.

## Özellikler

- **Kullanıcı Listeleme**: LDAP dizinindeki kullanıcıları görüntüleme
- **Kullanıcı Ekleme**: Yeni kullanıcı oluşturma
- **Kullanıcı Güncelleme**: Mevcut kullanıcı bilgilerini düzenleme
- **Kullanıcı Silme**: Kullanıcıları LDAP dizininden kaldırma
- **Domain Bilgisi Öğrenme**: LDAP sunucusunun domain bilgilerini alma
- **Sunucu Bağlantı Kontrolü**: LDAP sunucusuna bağlantı testi
- **Web Arayüzü**: Kolay kullanım için Flask tabanlı web uygulaması

## Gereksinimler

- Python 3.6+
- LDAP sunucusu ( Active Directory, OpenLDAP)
- Gerekli Python paketleri (requirements.txt dosyasında listelenmiştir)

## Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın veya İndirin

Bu projeyi bilgisayarınıza indirin veya klonlayın.

### 2. Yapılandırma Dosyasını Hazırlayın

`config.py.example` dosyasını `config.py` olarak kopyalayın ve LDAP sunucunuzun bilgilerini düzenleyin:

```bash
cp config.py.example config.py
```

`config.py` dosyasında aşağıdaki ayarları yapın:
- `LDAP_SERVER`: LDAP sunucusunun adresi (örneğin: `ldap://your-ldap-server.com`)
- `LDAP_USER`: LDAP sunucusuna bağlanmak için kullanılan kullanıcı adı (örneğin: `cn=admin,dc=example,dc=com`)
- `LDAP_PASSWORD`: LDAP kullanıcısının şifresi
- `BASE_DN`: LDAP dizininin temel ayrıştırılmış adı (örneğin: `dc=example,dc=com`)

**Not**: Güvenlik için gerçek LDAP sunucunuzda SSL/TLS kullanın ve şifreleri güvenli bir şekilde saklayın.

### 3. Gerekli Paketleri Yükleyin

Proje bağımlılıklarını yüklemek için terminalde aşağıdaki komutu çalıştırın:

```bash
pip install -r requirements.txt
```

Bu komut, aşağıdaki paketleri yükleyecektir:
- Flask: Web framework
- ldap3: LDAP protokolü için Python kütüphanesi
- Diğer gerekli bağımlılıklar

### 4. Uygulamayı Başlatın

Web uygulamasını başlatmak için:

```bash
python web_ui.py
```

Uygulama varsayılan olarak `http://localhost:5000` adresinde çalışacaktır. Tarayıcınızda bu adrese giderek arayüzü kullanabilirsiniz.

## Kullanım

- Ana sayfada mevcut kullanıcıları listeleyebilirsiniz.
- "Kullanıcı Ekle" formu ile yeni kullanıcı oluşturabilirsiniz.
- Kullanıcı listesinde "Düzenle" ve "Sil" butonları ile işlemleri gerçekleştirebilirsiniz.

## Ek Scriptler

Proje klasöründe ayrıca bağımsız scriptler bulunmaktadır:
- `ldappytdomainnameOgrenme.py`: Domain bilgilerini öğrenme
- `ldappythonKullaniciCekme.py`: Kullanıcı bilgilerini çekme
- `ldappythonKullaniciEkleme.py`: Kullanıcı ekleme
- `ldappythonKullaniciGuncelleme.py`: Kullanıcı güncelleme
- `ldappythonKullaniciSilme.py`: Kullanıcı silme
- `LDAPSERVERGIREBBILIYORMU.py`: LDAP sunucu bağlantı testi

Bu scriptleri komut satırından çalıştırabilirsiniz (örneğin: `python ldappythonKullaniciCekme.py`).

## Güvenlik Notları

- Bu uygulama temel bir örnek olarak geliştirilmiştir.
  - SSL/TLS sertifikaları kullanın
  - Şifreleri güvenli şekilde saklayın (örneğin environment variables)
  - Giriş doğrulama ve yetkilendirme ekleyin
  - Hata mesajlarını kullanıcı dostu hale getirin
  - LDAP bağlantılarını güvenli hale getirin

## Katkıda Bulunma

Bu projeye katkıda bulunmak için pull request gönderebilirsiniz

## Lisans

Bu proje açık kaynak kodludur. Detaylar için lisans dosyasına bakın.
