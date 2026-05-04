from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, MODIFY_ADD
import config

# --- BAĞLANTI BİLGİLERİ (config.py'den alınıyor) ---
ldap_server = config.LDAP_SERVER
username = config.LDAP_USER
password = config.LDAP_PASSWORD
base_dn = config.BASE_DN

# --- KULLANICI BİLGİLERİ ---
cn = 'Mehmet Alp Varna'
sn = 'Varna'
givenName = 'Alp'
displayName = 'Alp Varna'
sAMAccountName = 'malp.varna' 
userPrincipalName = 'malp.varna@map.tech' 
passW = 'P@ssw0rd123!'

# --- KONUM BİLGİLERİ ---
chosenOu = 'Sirket1'
target_alt_ou = 'AltSirket'
target_group_cn = 'test-IT'

# --- YÖNETİCİ BİLGİLERİ ---
manager_cn = ''
manager_ou = ''
manager_ana_ou = ''


# --- DN TANIMLAMALARI ---
user_dn = f"CN={cn},OU={target_alt_ou},OU={chosenOu},DC=map,DC=tech"
target_group_dn = f"CN={target_group_cn},OU={target_alt_ou},OU={chosenOu},DC=map,DC=tech" 


# --- DİNAMİK ATTRIBUTE HAZIRLAMA (MANAGER KONTROLÜ) ---
# Özellikleri sözlüğe atıyoruz
ad_attributes = {
    'cn': cn, 
    'sn': sn, 
    'givenName': givenName, 
    'displayName': displayName,
    'sAMAccountName': sAMAccountName,
    'mail': 'malp.varna@sirket1.com',
    'company': 'Sirket1',
    'department': 'Bilgi İşlem',
    'title': 'IT UZMAN YARDIMCISI',
    'userAccountControl': 544  # Pasif oluşturur (integer olmalı)
}

# KONTROL: Yönetici bilgisi dolu mu?
if manager_cn and "##" not in manager_cn and manager_cn.strip() != "":  
    manager_dn = f"CN={manager_cn},OU={manager_ou},OU={manager_ana_ou},DC=adtest,DC=ss"
    ad_attributes['manager'] = manager_dn
    print(f"Bilgi: Yönetici ({manager_cn}) eklenecek.")
else:
    print("Bilgi: Yönetici bilgisi boş, atama yapılmayacak.")


# Şifre Formatı
new_password = f'"{passW}"'.encode('utf-16-le') 


# --- LDAP İŞLEMLERİ (STANDART BAĞLANTI) ---
if config.LDAP_USE_SSL:
    server = Server(ldap_server, port=config.LDAP_SSL_PORT, use_ssl=True, get_info=ALL)
else:
    server = Server(ldap_server, get_info=ALL)
conn = Connection(server, user=username, password=password, auto_bind=True)

print(f"### 1. Kullanıcı Ekleniyor: {user_dn} ###")

# Kullanıcıyı oluştur
conn.add(user_dn, ['top', 'person', 'organizationalPerson', 'user'], ad_attributes)
print(f"Ekleme Sonucu: {conn.result['description']}")
print("---")

if conn.result['description'] != 'success':
    print(f"HATA: Kullanıcı eklenemedi. Detay: {conn.result}")
    conn.unbind()
else:
    # 1.5. UPN Ekle
    print("### 1.5. userPrincipalName Ekleniyor ###")
    conn.modify(user_dn, {'userPrincipalName': [(MODIFY_REPLACE, [userPrincipalName])]})
    print(f"UPN Sonucu: {conn.result['description']}")
    print("---")
    
    # NOT: Şifre atama ve hesap aktif etme SSL gerektirir. Manuel yapın.
    print("### NOT: Şifre ve hesap aktif etme manuel yapılacak (SSL gerekli) ###")
    print("---")

    # 4. Gruba Ekle
    print(f"### 4. Gruba Ekleniyor: {target_group_dn} ###")
    if conn.modify(target_group_dn, {'member': [(MODIFY_ADD, [user_dn])]}):
         print(f"Gruba Ekleme Sonucu: success")
    else:
         print(f"Gruba Ekleme Uyarısı: {conn.result['description']}") 
    print("---")

    conn.unbind()
    print("İşlem Bitti.")