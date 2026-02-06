# LDAP yapılandırma - çalışma ortamına göre düzenle
LDAP_SERVER = '192.168.1.1' #Sunucu IP 
LDAP_USER = '.' #UPN gelecek
LDAP_PASSWORD = 'Alp12345.' #Admin şifresi
BASE_DN = 'DC=map,DC=tech' #DN ler gelecek

# Web uygulaması ayarları
FLASK_DEBUG = True
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
