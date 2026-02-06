from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, MODIFY_ADD

class LDAPHelper:
    def __init__(self, server, user, password, base_dn):
        self.server = server
        self.user = user
        self.password = password
        self.base_dn = base_dn

    def _connect(self):
        try:
            server = Server(self.server, get_info=ALL, connect_timeout=5)
            conn = Connection(server, user=self.user, password=self.password, auto_bind=True)
            return conn
        except Exception as e:
            print(f"LDAP Bağlantı Hatası: {e}")
            return None

    def list_users(self, attributes=None, search_filter='(objectClass=user)'):
        if attributes is None:
            attributes = ['cn', 'userPrincipalName', 'mail', 'sAMAccountName', 'displayName', 'description']

        conn = self._connect()
        if not conn:
            return []

        try:
            conn.search(search_base=self.base_dn, search_filter=search_filter, attributes=attributes)
            results = []
            for entry in conn.entries:
                row = {}
                for attr in attributes:
                    if attr in entry:
                        val = entry[attr].value
                        if isinstance(val, list):
                            row[attr] = ", ".join(str(x) for x in val)
                        else:
                            row[attr] = str(val) if val is not None else ""
                    else:
                        row[attr] = ""
                row['dn'] = entry.entry_dn
                results.append(row)
            conn.unbind()
            return results
        except Exception as e:
            print(f"Arama Hatası: {e}")
            return []

    def add_user(self, user_dn, object_classes, attributes):
        conn = self._connect()
        ok = conn.add(user_dn, object_classes, attributes)
        result = conn.result
        conn.unbind()
        return {'ok': ok, 'result': result}

    def modify_user(self, user_dn, modifications):
        conn = self._connect()
        ok = conn.modify(user_dn, modifications)
        result = conn.result
        conn.unbind()
        return {'ok': ok, 'result': result}

    def delete_user(self, user_dn):
        conn = self._connect()
        ok = conn.delete(user_dn)
        result = conn.result
        conn.unbind()
        return {'ok': ok, 'result': result}
