from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, MODIFY_ADD, SUBTREE, BASE

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
            attributes = ['cn', 'userPrincipalName', 'mail', 'sAMAccountName', 'displayName', 'description', 'title', 'userAccountControl', 'department', 'telephoneNumber', 'mobile', 'co', 'c', 'countryCode', 'l', 'manager']

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

    def list_ous(self):
        conn = self._connect()
        if not conn:
            return []

        try:
            conn.search(search_base=self.base_dn, search_filter='(objectClass=organizationalUnit)', search_scope=SUBTREE, attributes=[])
            ous = [entry.entry_dn for entry in conn.entries]
            conn.unbind()
            return ous
        except Exception as e:
            print(f"OU Arama Hatası: {e}")
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

    def list_groups(self):
        conn = self._connect()
        if not conn:
            return []
        try:
            conn.search(search_base=self.base_dn, search_filter='(objectClass=group)', search_scope=SUBTREE,
                        attributes=['cn', 'sAMAccountName'])
            results = []
            for entry in conn.entries:
                results.append({'cn': entry.cn.value, 'dn': entry.entry_dn})
            conn.unbind()
            return sorted(results, key=lambda x: x['cn'])
        except Exception as e:
            print(f"Grup Arama Hatası: {e}")
            return []

    def list_group_members(self, group_dn):
        conn = self._connect()
        if not conn:
            return []
        try:
            conn.search(search_base=group_dn, search_filter='(objectClass=*)', search_scope=BASE,
                        attributes=['member'])
            if not conn.entries:
                conn.unbind()
                return []
            members_dns = conn.entries[0].member.values if conn.entries[0].member else []
            if not members_dns:
                conn.unbind()
                return []
            results = []
            for member_dn in members_dns:
                conn.search(search_base=member_dn, search_filter='(objectClass=user)', search_scope=BASE,
                            attributes=['cn', 'sAMAccountName', 'displayName'])
                if conn.entries:
                    e = conn.entries[0]
                    results.append({
                        'cn': e.cn.value if e.cn else '',
                        'dn': e.entry_dn,
                        'displayName': e.displayName.value if e.displayName else ''
                    })
            conn.unbind()
            return sorted(results, key=lambda x: x['cn'])
        except Exception as e:
            print(f"Üye Arama Hatası: {e}")
            return []
