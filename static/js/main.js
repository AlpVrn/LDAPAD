function autoFill() {
    var ad = document.getElementById('givenName').value;
    var soyad = document.getElementById('sn').value;
    var tamAd = ad + (ad && soyad ? ' ' : '') + soyad;

    var cnKutu = document.getElementById('cn');
    if (cnKutu) cnKutu.value = tamAd;

    var kullaniciAdi = tamAd.toLowerCase()
        .replace(/ğ/g, 'g')
        .replace(/ü/g, 'u')
        .replace(/ş/g, 's')
        .replace(/ı/g, 'i')
        .replace(/ö/g, 'o')
        .replace(/ç/g, 'c')
        .replace(/\s+/g, '.');

    var samKutu = document.getElementById('sAMAccountName');
    if (samKutu) samKutu.value = kullaniciAdi;
}

let currentFilter = 'all';

function setFilter(filter) {
    currentFilter = filter;
    document.querySelectorAll('.filter-card').forEach(c => c.style.opacity = c.dataset.filter === filter ? '1' : '0.5');
    refreshUsersTable();
}

function refreshUsersTable() {
    fetch('/users')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('table tbody');
            const cardContainer = document.getElementById('user-cards');
            const totalCounter = document.getElementById('total-count');
            const activeCounter = document.getElementById('active-count');
            const passiveCounter = document.getElementById('passive-count');

            let totalCount = 0;
            let activeCount = 0;
            let passiveCount = 0;

            const badge = (isActive) =>
                isActive
                    ? '<span class="badge bg-success">Aktif</span>'
                    : '<span class="badge bg-danger">Pasif</span>';

            const actionBtns = (u) => `
                <div class="d-flex gap-1">
                    <form method="post" action="/delete" onsubmit="return confirm('Silmek istediğinize emin misiniz?');">
                        <input type="hidden" name="dn" value="${u.dn || ''}">
                        <button class="btn btn-sm btn-danger" type="submit">Sil</button>
                    </form>
                    <a class="btn btn-sm btn-secondary" href="/update?dn=${encodeURIComponent(u.dn || '')}">Güncelle</a>
                </div>
            `;

            if (tbody) tbody.innerHTML = '';
            if (cardContainer) cardContainer.innerHTML = '';

            data.forEach(u => {
                const uac = parseInt(u.userAccountControl) || 0;
                const isDisabled = (uac & 2);
                const isActive = !isDisabled;

                totalCount++;
                if (isActive) activeCount++; else passiveCount++;

                if (currentFilter === 'active' && !isActive) return;
                if (currentFilter === 'passive' && isActive) return;

                if (tbody) {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${u.cn || ''}</td>
                        <td class="d-none d-lg-table-cell">${u.userPrincipalName || ''}</td>
                        <td class="d-none d-md-table-cell">${u.mail || ''}</td>
                        <td>${u.sAMAccountName || ''}</td>
                        <td>${badge(isActive)}</td>
                        <td>${actionBtns(u)}</td>
                    `;
                    tbody.appendChild(tr);
                }

                if (cardContainer) {
                    const skipKeys = ['dn', 'userAccountControl', 'objectClass', 'distinguishedName', 'cn'];
                    let detailsHtml = '';
                    for (const [key, val] of Object.entries(u)) {
                        if (!skipKeys.includes(key)) {
                            detailsHtml += `<div>${key}: ${val || 'none'}</div>`;
                        }
                    }

                    const col = document.createElement('div');
                    col.className = 'col-12';
                    col.innerHTML = `
                        <div class="card shadow-sm">
                            <div class="card-body py-2 px-3">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div class="fw-bold">${u.cn || ''}</div>
                                    ${badge(isActive)}
                                </div>
                                <div class="small text-muted mt-1">${detailsHtml}</div>
                                <div class="d-flex gap-1 mt-2">${actionBtns(u)}</div>
                            </div>
                        </div>
                    `;
                    cardContainer.appendChild(col);
                }
            });

            if (totalCounter) totalCounter.innerText = totalCount;
            if (activeCounter) activeCounter.innerText = activeCount;
            if (passiveCounter) passiveCounter.innerText = passiveCount;
        })
        .catch(err => console.error('Kullanıcı listesi yenilenirken hata:', err));
}

const countries = [
    {ad:"Türkiye",kod:"TR",num:"792"},
    {ad:"Almanya",kod:"DE",num:"276"},
    {ad:"Amerika Birleşik Devletleri",kod:"US",num:"840"},
    {ad:"Avustralya",kod:"AU",num:"036"},
    {ad:"Avusturya",kod:"AT",num:"040"},
    {ad:"Belçika",kod:"BE",num:"056"},
    {ad:"Birleşik Arap Emirlikleri",kod:"AE",num:"784"},
    {ad:"Birleşik Krallık",kod:"GB",num:"826"},
    {ad:"Brezilya",kod:"BR",num:"076"},
    {ad:"Bulgaristan",kod:"BG",num:"100"},
    {ad:"Çek Cumhuriyeti",kod:"CZ",num:"203"},
    {ad:"Çin",kod:"CN",num:"156"},
    {ad:"Danimarka",kod:"DK",num:"208"},
    {ad:"Endonezya",kod:"ID",num:"360"},
    {ad:"Estonya",kod:"EE",num:"233"},
    {ad:"Fas",kod:"MA",num:"504"},
    {ad:"Finlandiya",kod:"FI",num:"246"},
    {ad:"Fransa",kod:"FR",num:"250"},
    {ad:"Güney Kore",kod:"KR",num:"410"},
    {ad:"Hindistan",kod:"IN",num:"356"},
    {ad:"Hollanda",kod:"NL",num:"528"},
    {ad:"İngiltere",kod:"GB",num:"826"},
    {ad:"İrlanda",kod:"IE",num:"372"},
    {ad:"İspanya",kod:"ES",num:"724"},
    {ad:"İsveç",kod:"SE",num:"752"},
    {ad:"İsviçre",kod:"CH",num:"756"},
    {ad:"İtalya",kod:"IT",num:"380"},
    {ad:"Japonya",kod:"JP",num:"392"},
    {ad:"Kanada",kod:"CA",num:"124"},
    {ad:"Kolombiya",kod:"CO",num:"170"},
    {ad:"Letonya",kod:"LV",num:"428"},
    {ad:"Litvanya",kod:"LT",num:"440"},
    {ad:"Lüksemburg",kod:"LU",num:"442"},
    {ad:"Macaristan",kod:"HU",num:"348"},
    {ad:"Makedonya",kod:"MK",num:"807"},
    {ad:"Meksika",kod:"MX",num:"484"},
    {ad:"Mısır",kod:"EG",num:"818"},
    {ad:"Norveç",kod:"NO",num:"578"},
    {ad:"Pakistan",kod:"PK",num:"586"},
    {ad:"Polonya",kod:"PL",num:"616"},
    {ad:"Portekiz",kod:"PT",num:"620"},
    {ad:"Romanya",kod:"RO",num:"642"},
    {ad:"Rusya",kod:"RU",num:"643"},
    {ad:"Suudi Arabistan",kod:"SA",num:"682"},
    {ad:"Sırbistan",kod:"RS",num:"688"},
    {ad:"Slovakya",kod:"SK",num:"703"},
    {ad:"Slovenya",kod:"SI",num:"705"},
    {ad:"Şili",kod:"CL",num:"152"},
    {ad:"Tayland",kod:"TH",num:"764"},
    {ad:"Tunus",kod:"TN",num:"788"},
    {ad:"Ukrayna",kod:"UA",num:"804"},
    {ad:"Yunanistan",kod:"GR",num:"300"},
    {ad:"Yeni Zelanda",kod:"NZ",num:"554"}
];

function selectCountry(selectEl) {
    const match = countries.find(u => u.ad === selectEl.value);
    if (match) {
        document.getElementById('co').value = match.ad;
        document.getElementById('c').value = match.kod;
        document.getElementById('countryCode').value = match.num;
    } else {
        document.getElementById('co').value = '';
        document.getElementById('c').value = '';
        document.getElementById('countryCode').value = '';
    }
}

function initCountrySelect() {
    const current = document.getElementById('c') ? document.getElementById('c').value : '';
    const select = document.getElementById('ulke_select');
    if (select && current) {
        const match = countries.find(u => u.kod === current);
        if (match) select.value = match.ad;
    }
}

function onGroupChange(selectEl) {
    const userSelect = document.getElementById('manager_kullanici');
    const managerDnInput = document.getElementById('manager_dn');

    if (!selectEl.value) {
        userSelect.innerHTML = '<option value="">-- Önce grup seçin --</option>';
        userSelect.disabled = true;
        managerDnInput.value = '';
        return;
    }

    userSelect.innerHTML = '<option value="">Yükleniyor...</option>';
    userSelect.disabled = true;

    fetch('/api/groups/members?group_dn=' + encodeURIComponent(selectEl.value))
        .then(r => r.json())
        .then(data => {
            userSelect.innerHTML = '<option value="">-- Kullanıcı seçin --</option>';
            data.forEach(u => {
                const opt = document.createElement('option');
                opt.value = u.dn;
                opt.textContent = u.cn + (u.displayName ? ' (' + u.displayName + ')' : '');
                userSelect.appendChild(opt);
            });
            userSelect.disabled = false;
            userSelect.onchange = function() {
                managerDnInput.value = this.value;
                document.getElementById('manager_clear').value = '';
                document.getElementById('mevcut_manager').textContent = this.value || 'Tanımsız';
            };
        })
        .catch(err => {
            userSelect.innerHTML = '<option value="">Hata oluştu</option>';
            console.error('Grup üyeleri yüklenirken hata:', err);
        });
}

function clearManager() {
    document.getElementById('manager_dn').value = '';
    document.getElementById('manager_clear').value = '1';
    document.getElementById('manager_grup').value = '';
    document.getElementById('manager_kullanici').innerHTML = '<option value="">-- Önce grup seçin --</option>';
    document.getElementById('manager_kullanici').disabled = true;
    document.getElementById('mevcut_manager').textContent = 'Tanımsız';
}

function initManagerSelect() {
    const managerDn = document.getElementById('manager_dn') ? document.getElementById('manager_dn').value : '';
    if (!managerDn) return;
    const userSelect = document.getElementById('manager_kullanici');
    const opt = document.createElement('option');
    opt.value = managerDn;
    opt.textContent = managerDn;
    opt.selected = true;
    userSelect.innerHTML = '';
    userSelect.appendChild(opt);
    userSelect.disabled = false;
}

document.addEventListener('DOMContentLoaded', function() {
    refreshUsersTable();
    setInterval(refreshUsersTable, 30000);
    initCountrySelect();
    initManagerSelect();
});
