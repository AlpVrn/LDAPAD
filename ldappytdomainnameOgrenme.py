from ldap3 import Server, Connection, ALL
from config import LDAP_SERVER, LDAP_USER, LDAP_PASSWORD
ldap_server = LDAP_SERVER
username = LDAP_USER
password = LDAP_PASSWORD
server = Server(ldap_server, get_info=ALL)
conn = Connection(server, user=username, password=password, auto_bind=True)

# Base DN'leri yazdır
print("Naming Contexts:", server.info.naming_contexts)

# İlk eleman genellikle senin gerçek Base DN'ındır
if server.info.naming_contexts:
    print("Base DN:", server.info.naming_contexts[0])
else:
    print("Base DN alınamadı.")
