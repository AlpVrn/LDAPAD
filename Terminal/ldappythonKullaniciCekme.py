from ldap3 import Server, Connection, ALL
import pandas as pd  # Excel işlemi için gerekli kütüphane
import config

# --- BAĞLANTI BİLGİLERİ (config.py'den alınıyor) ---
ldap_server = config.LDAP_SERVER
username = config.LDAP_USER
password = config.LDAP_PASSWORD
base_dn = config.BASE_DN

# --- İSTEDİĞİN SÜTUNLAR (Sadeleştirilmiş Liste) ---
istenen_alanlar = [
    'cn',                 # Common Name (Genel Ad)
    'userPrincipalName',  # UPN (Mail formatındaki giriş adı - user@domain.com)
    'mail',               # E-posta Adresi
    'sAMAccountName',     # Eski tip Kullanıcı Adı (DOMAIN\user)
    'displayName',        # Görünen Ad
    'description'         # Açıklama
]

# Sunucu bağlantısı
server = Server(ldap_server, get_info=ALL)
conn = Connection(server, user=username, password=password, auto_bind=True)

base_dn = 'dc=acme,dc=mbr'
search_filter = '(objectClass=user)'

print("Kullanıcılar aranıyor...")

# Domaine göre filtreleme
conn.search(search_base=base_dn,
            search_filter=search_filter,
            attributes=istenen_alanlar)

# --- EXCELE AKTARMAK İÇİN ---
if conn.entries:
    excel_verisi = [] 

    for entry in conn.entries:
        satir = {}
        
        for alan in istenen_alanlar:
            if alan in entry:
                deger = entry[alan].value
                
                # AD'den gelen Tarih formatlarını düzeltmek için
                if str(type(deger)) == "<class 'datetime.datetime'>":
                    satir[alan] = str(deger)
                
                # Listeleri birleştir (Bazen description veya mail çoklu olabilir)
                elif isinstance(deger, list):
                    satir[alan] = ", ".join(str(x) for x in deger)
                
                # Normal değerler
                else:
                    satir[alan] = str(deger) if deger is not None else ""
            else:
                # Eğer kullanıcıda o alan boşsa Excel'e boş string bas
                satir[alan] = ""
        
        excel_verisi.append(satir)

    # --- PANDAS İLE EXCEL'E KAYDETME ---
    df = pd.DataFrame(excel_verisi)
    
    df = df[istenen_alanlar]

    dosya_adi = "Kullanici_Listesi.xlsx"
    
    # Excel'e yaz
    df.to_excel(dosya_adi, index=False)
    
    print(f"✅ İşlem tamam! '{dosya_adi}' dosyası oluşturuldu.")
    print(f"Toplam {len(excel_verisi)} kullanıcı raporlandı.")

else:
    print("❌ Kullanıcı bulunamadı.")

conn.unbind()