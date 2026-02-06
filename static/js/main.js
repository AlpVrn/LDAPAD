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