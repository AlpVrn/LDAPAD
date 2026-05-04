from ldap3 import Server, Connection, ALL
import config

# --- BAĞLANTI BİLGİLERİ (config.py'den alınıyor) ---
ldap_server = config.LDAP_SERVER
username = config.LDAP_USER
password = config.LDAP_PASSWORD
base_dn = config.BASE_DN

# 📌 SİLİNECEK KULLANICI BİLGİLERİ (DİNAMİK) ---
user_cn = "Mehmet Alp"  # Silmek istediğin kullanıcının tam CN'i (Adı)
chosenOu = 'Sirket1'            # Üst OU (Örn: 'Sirkets1')
# 👇 KULLANICININ GERÇEKTEN BULUNDUĞU ALT OU'yu buraya yaz
# Örnek: 'IT' veya 'Pazarlama'
target_alt_ou = 'IT'          


# Kullanıcının tam yolu: CN=İsim,OU=AltOU,OU=AnaOU,DC=Domain,DC=ss
user_dn = f"CN={user_cn},OU={target_alt_ou},OU={chosenOu},DC=adtest,DC=ss" 


# Sunucuya bağlan
server = Server(ldap_server, get_info=ALL)
conn = Connection(server, user=username, password=password, auto_bind=True)

print(f"[{user_dn}] adresi silinmeye çalışılıyor...")

# Kullanıcıyı sil
if conn.delete(user_dn):
    print("✅ Kullanici basariyla silindi.")
else:
    print("❌ Kullanici silinemedi:")
    # Hata durumunda detaylı LDAP sonucunu yazdırır (noSuchObject vs.)
    print(conn.result)

# Bağlantıyı kapat
conn.unbind()