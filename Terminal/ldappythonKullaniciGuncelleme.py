from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, MODIFY_ADD
import config

# --- BAĞLANTI BİLGİLERİ (config.py'den alınıyor) ---
ldap_server = config.LDAP_SERVER
username = config.LDAP_USER
password = config.LDAP_PASSWORD
base_dn = config.BASE_DN

# --- 1. GÜNCELLENECEK KULLANICI ---
user_cn = "mehmet Alp Varna"
chosenOu = 'Sirket1'
target_alt_ou = 'IT'

# --- 2. YENİ DEĞERLER (Attributes) ---
user_mail = "malp.varna@sirket1.com.tr"
user_title = "Uzman"
user_description = "Süreç Geliştirme"
user_department = "IT"
user_physicalDeliveryOfficeName = "Sirket2"
user_company = "sirket2"
user_telephoneNumber = "055555"
user_mobile = '055555'
user_streetAddress = "istanbul"
user_l = "İstanbul"

# --- 3. YENİ YÖNETİCİ BİLGİSİ (Manager) ---
manager_cn = "ALP MEHMET" 
manager_ou = "IT"
manager_ana_ou = "Sirket1"

# --- 4. EKLENECEK GRUP BİLGİSİ (HEDEF: Sirket1) ---
group_name = "it-deneme"      # Grubun ADI (CN)
group_ou = "IT"             # Grubun bulunduğu ALT OU
group_ana_ou = "Sirket1"    # Grubun bulunduğu ANA OU 


# --- DN TANIMLAMALARI ---
user_dn = f"CN={user_cn},OU={target_alt_ou},OU={chosenOu},DC=adtest,DC=ss"
manager_dn = f"CN={manager_cn},OU={manager_ou},OU={manager_ana_ou},DC=adtest,DC=ss"

# Hedef Grup DN'i (Sirket1 olarak ayarlandı)
target_group_dn = f"CN={group_name},OU={group_ou},OU={group_ana_ou},DC=adtest,DC=ss"


# --- GÜNCELLEME SÖZLÜĞÜ ---
modifications = {
    'mail' : [(MODIFY_REPLACE, [user_mail])],
    'title' : [(MODIFY_REPLACE, [user_title])],
    'description' : [(MODIFY_REPLACE, [user_description])],
    'department' : [(MODIFY_REPLACE, [user_department])],
    'physicalDeliveryOfficeName' : [(MODIFY_REPLACE, [user_physicalDeliveryOfficeName])],
    'company' : [(MODIFY_REPLACE, [user_company])],
    'telephoneNumber' : [(MODIFY_REPLACE, [user_telephoneNumber])],
    'mobile' : [(MODIFY_REPLACE, [user_mobile])],
    'streetAddress' : [(MODIFY_REPLACE, [user_streetAddress])],
    'l' : [(MODIFY_REPLACE, [user_l])],
    'manager': [(MODIFY_REPLACE, [manager_dn])]
}

# --- LDAP İŞLEMLERİ ---
server = Server(ldap_server, get_info=ALL)
conn = Connection(server, user=username, password=password, auto_bind=True)

print(f"🔄 [{user_cn}] kullanıcısı güncelleniyor...")

# 1. ADIM: Kullanıcı Bilgilerini Güncelle
if conn.modify(user_dn, modifications):
    print(f"✅ Kullanıcı bilgileri ve Manager başarıyla güncellendi.")
else:
    print(f"❌ Kullanıcı güncellenemedi. Hata: {conn.result}")

print("-" * 30)

# 2. ADIM: Kullanıcıyı Gruba Ekle
print(f"🔄 Kullanıcı [{group_name}] grubuna ekleniyor...")
print(f"    Hedef Grup Konumu: {group_ana_ou} > {group_ou}")
print(f"    Grup DN: {target_group_dn}")

try:
    if conn.modify(target_group_dn, {'member': [(MODIFY_ADD, [user_dn])]}):
        print(f"✅ BAŞARILI: Kullanıcı '{group_name}' grubuna eklendi.")
    else:
        hata_kodu = conn.result['description']
        if "AttributeOrValueExists" in hata_kodu:
            print(f"ℹ️  BİLGİ: Kullanıcı ZATEN bu grubun üyesi.")
        elif "noSuchObject" in hata_kodu:
            print(f"❌ HATA: Grup bulunamadı! '{group_ana_ou}' altında '{group_ou}' klasöründe '{group_name}' isminde grup olduğundan emin misin?")
        else:
            print(f"❌ HATA: {conn.result}")

except Exception as e:
    print(f"💥 Kod Hatası: {e}")

conn.unbind()
print("İşlemler tamamlandı.")