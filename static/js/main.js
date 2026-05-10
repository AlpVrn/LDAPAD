// static/js/main.js

function otomatikDoldur() {
    // 1. Kutulardaki verileri al
    var ad = document.getElementById('givenName').value;
    var soyad = document.getElementById('sn').value;

    // 2. CN (Tam Ad) Oluştur: "Ad Soyad"
    // Eğer ad veya soyad boşsa araya boşluk koyma
    var tamAd = ad + (ad && soyad ? ' ' : '') + soyad;
    
    // CN kutusuna yaz
    var cnKutu = document.getElementById('cn');
    if (cnKutu) {
        cnKutu.value = tamAd;
    }

    // 3. Kullanıcı Adı (sAMAccountName) Oluşturma
    // Örn: Mehmet Alp Varna -> mehmet.varna
    
    // Türkçe karakterleri İngilizceye çeviren fonksiyon
    var kullaniciAdi = tamAd.toLowerCase()
        .replace(/ğ/g, 'g')
        .replace(/ü/g, 'u')
        .replace(/ş/g, 's')
        .replace(/ı/g, 'i')
        .replace(/ö/g, 'o')
        .replace(/ç/g, 'c')
        .replace(/\s+/g, '.'); // Boşlukları noktaya çevir

    // Kullanıcı adı kutusuna yaz
    var samKutu = document.getElementById('sAMAccountName');
    if (samKutu) {
        samKutu.value = kullaniciAdi;
    }
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

                // Tablo satırı
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

                // Mobil kart
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

document.addEventListener('DOMContentLoaded', function() {
    refreshUsersTable();
    setInterval(refreshUsersTable, 30000);
});
