from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import config
from ldap_helpers import LDAPHelper
from datetime import datetime
import os
import re

LOG_FILE = 'audit.log'

def log_action(action, detail):
    ip = request.remote_addr or 'unknown'
    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {ip} | {action} | {detail}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line)

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

@app.route('/users')
def users_json():
    users = ldap.list_users()
    return jsonify(users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        cn = request.form.get('cn')
        ou_select = request.form.get('ou_select')
        ou_text = request.form.get('ou_text')
        sam = request.form.get('sAMAccountName')
        mail = request.form.get('mail')
        account_status = request.form.get('account_status', '544')

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
            'userAccountControl': int(account_status),
        }
        if mail:
            attributes['mail'] = mail

        res = ldap.add_user(user_dn, object_classes, attributes)
        if res['ok']:
            flash('Kullanıcı eklendi.', 'success')
            log_action('ADD', f"dn={user_dn} sAMAccountName={sam} mail={mail or 'none'}")
        else:
            flash(f"Hata: {res['result']}", 'danger')
            log_action('ADD_FAILED', f"dn={user_dn} sAMAccountName={sam} error={res['result']}")

        return redirect(url_for('index'))

    ous = ldap.list_ous()
    return render_template('add_user.html', ous=ous)

@app.route('/delete', methods=['POST'])
def delete_user():
    dn = request.form.get('dn')
    if not dn:
        flash('DN belirtilmedi.', 'warning')
        return redirect(url_for('index'))

    res = ldap.delete_user(dn)
    if res['ok']:
        flash('Kullanıcı silindi.', 'success')
        log_action('DELETE', f"dn={dn}")
    else:
        flash(f"Silme hatası: {res['result']}", 'danger')
        log_action('DELETE_FAILED', f"dn={dn} error={res['result']}")

    return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        dn = request.form.get('dn')
        mail = request.form.get('mail')
        title = request.form.get('title')
        account_status = request.form.get('account_status')

        if not dn:
            flash('DN gerekli.', 'warning')
            return redirect(url_for('index'))

        from ldap3 import MODIFY_REPLACE
        modifications = {}
        if mail:
            modifications['mail'] = [(MODIFY_REPLACE, [mail])]
        if title:
            modifications['title'] = [(MODIFY_REPLACE, [title])]
        if account_status:
            modifications['userAccountControl'] = [(MODIFY_REPLACE, [int(account_status)])]

        if not modifications:
            flash('Güncellenecek alan yok.', 'info')
            return redirect(url_for('index'))

        res = ldap.modify_user(dn, modifications)
        if res['ok']:
            flash('Kullanıcı güncellendi.', 'success')
            changed = []
            if mail: changed.append(f"mail={mail}")
            if title: changed.append(f"title={title}")
            if account_status: changed.append(f"account_status={account_status}")
            log_action('UPDATE', f"dn={dn} changed={', '.join(changed)}")
        else:
            flash(f"Güncelleme hatası: {res['result']}", 'danger')
            log_action('UPDATE_FAILED', f"dn={dn} error={res['result']}")

        return redirect(url_for('index'))

    # GET ile gelirse query param 'dn' ile formu doldur
    dn = request.args.get('dn')
    if dn:
        # Kullanıcının mevcut bilgilerini çek
        user_info = ldap.list_users(search_filter=f"(distinguishedName={dn})")
        user = user_info[0] if user_info else {}
    else:
        user = {}
    return render_template('edit_user.html', dn=dn, user=user)

@app.route('/logs')
def view_logs():
    lines = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    return render_template('logs.html', lines=reversed(lines))

CONFIG_FILE = 'config.py'

CONFIG_FIELDS = {
    'LDAP_SERVER': 'text',
    'LDAP_USER': 'text',
    'LDAP_PASSWORD': 'password',
    'BASE_DN': 'text',
    'FLASK_DEBUG': 'checkbox',
    'FLASK_HOST': 'text',
    'FLASK_PORT': 'number',
}

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        vals = {}
        for key in CONFIG_FIELDS:
            if CONFIG_FIELDS[key] == 'checkbox':
                vals[key] = request.form.get(key) == 'on'
            elif CONFIG_FIELDS[key] == 'number':
                try:
                    vals[key] = int(request.form.get(key, 0))
                except ValueError:
                    vals[key] = 0
            else:
                vals[key] = request.form.get(key, '')

        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        for key, value in vals.items():
            if isinstance(value, bool):
                content = re.sub(rf'^{key}\s*=\s*.*?(?=\n|$)', f"{key} = {str(value)}", content, flags=re.MULTILINE)
            elif isinstance(value, int):
                content = re.sub(rf'^{key}\s*=\s*.*?(?=\n|$)', f"{key} = {value}", content, flags=re.MULTILINE)
            else:
                escaped = value.replace('\\', '\\\\').replace("'", "\\'")
                content = re.sub(rf'^{key}\s*=\s*.*?(?=\n|$)', f"{key} = '{escaped}'", content, flags=re.MULTILINE)

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

        flash('Ayarlar kaydedildi. Bazı değişiklikler için uygulamayı yeniden başlatmanız gerekebilir.', 'success')
        log_action('SETTINGS_UPDATE', f"değişenler: {', '.join(vals.keys())}")
        return redirect(url_for('settings'))

    cfg = {}
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    for key in CONFIG_FIELDS:
        m = re.search(rf'^{key}\s*=\s*(.*?)$', content, re.MULTILINE)
        if m:
            raw = m.group(1).strip()
            if raw.lower() in ('true', 'false'):
                cfg[key] = raw.lower() == 'true'
            elif raw.isdigit() or (raw.startswith('-') and raw[1:].isdigit()):
                cfg[key] = int(raw)
            else:
                cfg[key] = raw.strip("'\"")
        else:
            cfg[key] = '' if CONFIG_FIELDS[key] != 'checkbox' else False
    return render_template('settings.html', cfg=cfg, fields=CONFIG_FIELDS)

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG)
