from ldap3 import Server, Connection, ALL

ldap_server = 'ldap://172.16.66.17'
username = 'alp.varna@acme.mbr'
password = 'Aa12345.'
server = Server(ldap_server, get_info=ALL)
conn = Connection(server, user=username, password=password, auto_bind=True)

# Base DN'leri yazdır
print("Naming Contexts:", server.info.naming_contexts)

# İlk eleman genellikle senin gerçek Base DN'ındır
if server.info.naming_contexts:
    print("Base DN:", server.info.naming_contexts[0])
else:
    print("Base DN alınamadı.")
