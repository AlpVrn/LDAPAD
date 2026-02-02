from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, MODIFY_ADD

# --- BAĞLANTI BİLGİLERİ (SSL YOK) ---
ldap_server = 'serverIP'
username = 'userPrincipalName'
password = 'PASS'

# --- KULLANICI BİLGİLERİ ---
cn = 'Mehmet Alp Varna'
sn = 'Varna'
givenName = 'Alp'
displayName = 'Alp Varna'
sAMAccountName = 'malp.varna' 
userPrincipalName = 'malp.varna@adtest.ss' 
passW = '1'

# --- KONUM BİLGİLERİ ---
chosenOu = 'Sirket1'
target_alt_ou = 'IT'
target_group_cn = 'test-IT'

# --- YÖNETİCİ BİLGİLERİ ---
manager_cn = 'Alp Mehmet'
manager_ou = 'IT'
manager_ana_ou = 'Sirket1'


# --- DN TANIMLAMALARI ---
user_dn = f"CN={cn},OU={target_alt_ou},OU={chosenOu},DC=adtest,DC=ss"
target_group_dn = f"CN={target_group_cn},OU={target_alt_ou},OU={chosenOu},DC=adtest,DC=ss" 


# --- DİNAMİK ATTRIBUTE HAZIRLAMA (MANAGER KONTROLÜ) ---
# Özellikleri sözlüğe atıyoruz
ad_attributes = {
    'cn': cn, 'sn': sn, 'givenName': givenName, 'displayName': displayName,
    'sAMAccountName': sAMAccountName,   
    'c': 'TR', 'co': 'Türkiye', 'countryCode': '792', 'mail': 'malp.varna@sirket1.com', 'company': 'Sirket1', 
    'department': 'Bilgi İşlem', 'description': '', 'homePhone': '1111', 'l': 'İstanbul', 'mobile': '0555 555 55 55',
    'physicalDeliveryOfficeName': 'Sirket Fiziksel', 'st': 'istanvul', 'streetAddress': 'istanbul',
    'telephoneNumber': '0555555', 'title': 'IT UZMAN YARDIMCISI',
    'userAccountControl': ['544'] # Pasif oluşturur
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
    
    # 2. Şifre (NOT: Burası SSL olmadığı için hata veriyor önemsiz)
    print("### 2. Şifre Atanıyor ###")
    conn.modify(user_dn, {'unicodePwd': [(MODIFY_REPLACE, [new_password])]})
    print(f"Şifre Sonucu: {conn.result['description']}") # Burası 'unwillingToPerform' diyo
    print("---")

    # 3. Enable Et (Şifre atanamadığı için burası da hata verebilir)
    print("### 3. Hesap Aktif Ediliyor ###")
    conn.modify(user_dn, {'userAccountControl': [(MODIFY_REPLACE, ['512'])]})
    print(f"Enable Sonucu: {conn.result['description']}")
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