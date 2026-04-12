from flask import Flask, render_template, request, redirect, url_for, flash
import config
from ldap_helpers import LDAPHelper

app = Flask(__name__)
app.secret_key = '3131'

ldap = LDAPHelper(config.LDAP_SERVER, config.LDAP_USER, config.LDAP_PASSWORD, config.BASE_DN)

@app.route('/')
def index():
    users = ldap.list_users()
    if not users and config.LDAP_SERVER == 'serverIP':
        flash('Lütfen config.py dosyasındaki LDAP_SERVER ayarını güncelleyin!', 'warning')
    elif not users:
        flash('Kullanıcı listesi alınamadı veya LDAP sunucusuna bağlanılamadı.', 'danger')
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Basit örnek: form üzerinden CN, OU ve birkaç attribute alıyoruz
        cn = request.form.get('cn')
        ou_select = request.form.get('ou_select')
        ou_text = request.form.get('ou_text')
        sam = request.form.get('sAMAccountName')
        mail = request.form.get('mail')

        if not cn or not sam or not (ou_select or ou_text):
            flash('CN, OU ve sAMAccountName gerekli. OU seçin veya yazın.', 'warning')
            return redirect(url_for('add_user'))

        ou_value = ou_select.strip() if ou_select else ou_text.strip()
        if ou_value.upper().startswith('DC='):
            parent_dn = ou_value
        elif ou_value.upper().startswith('OU='):
            parent_dn = ou_value
        else:
            parts = [p.strip() for p in ou_value.split(',') if p.strip()]
            parent_dn = ','.join(f"OU={part}" if not part.upper().startswith('OU=') else part for part in parts)

        if parent_dn:
            user_dn = f"CN={cn},{parent_dn}" if 'DC=' in parent_dn.upper() else f"CN={cn},{parent_dn},{config.BASE_DN}"
        else:
            user_dn = f"CN={cn},{config.BASE_DN}"

        object_classes = ['top', 'person', 'organizationalPerson', 'user']
        attributes = {
            'cn': cn,
            'sAMAccountName': sam,
            'displayName': cn,
        }
        if mail:
            attributes['mail'] = mail

        res = ldap.add_user(user_dn, object_classes, attributes)
        if res['ok']:
            flash('Kullanıcı eklendi.', 'success')
        else:
            flash(f"Hata: {res['result']}", 'danger')

        return redirect(url_for('index'))

    ous = ldap.list_ous()
    return render_template('form_user.html', action='add', ous=ous)

@app.route('/delete', methods=['POST'])
def delete_user():
    dn = request.form.get('dn')
    if not dn:
        flash('DN belirtilmedi.', 'warning')
        return redirect(url_for('index'))

    res = ldap.delete_user(dn)
    if res['ok']:
        flash('Kullanıcı silindi.', 'success')
    else:
        flash(f"Silme hatası: {res['result']}", 'danger')

    return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        dn = request.form.get('dn')
        mail = request.form.get('mail')
        title = request.form.get('title')

        if not dn:
            flash('DN gerekli.', 'warning')
            return redirect(url_for('index'))

        mods = {}
        if mail:
            mods['mail'] = [(MODIFY_REPLACE := 'MODIFY_REPLACE', [mail])]
        if title:
            mods['title'] = [(MODIFY_REPLACE, [title])]

        # ldap_helpers expects LDAP-style modifications dict
        # but above we used placeholder constants; convert to MODIFY_REPLACE
        # For simplicity, build in-place using ldap3 constant values
        from ldap3 import MODIFY_REPLACE
        modifications = {}
        if mail:
            modifications['mail'] = [(MODIFY_REPLACE, [mail])]
        if title:
            modifications['title'] = [(MODIFY_REPLACE, [title])]

        if not modifications:
            flash('Güncellenecek alan yok.', 'info')
            return redirect(url_for('index'))

        res = ldap.modify_user(dn, modifications)
        if res['ok']:
            flash('Kullanıcı güncellendi.', 'success')
        else:
            flash(f"Güncelleme hatası: {res['result']}", 'danger')

        return redirect(url_for('index'))

    # GET ile gelirse query param 'dn' ile formu doldur
    dn = request.args.get('dn')
    return render_template('form_user.html', action='update', dn=dn)

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG)
