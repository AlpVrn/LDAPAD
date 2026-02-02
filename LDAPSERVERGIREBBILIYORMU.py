import pyodbc

# Senin ayarların
SQL_CONN_STR = (
    "DRIVER={SQL Server};"
    "SERVER=SERVERIP"
    "DATABASE=Sirket1;"
    "UID=alp.varna;"
    "PWD=PASS;"
)

print("⏳ Bağlantı deneniyor...")

try:
    conn = pyodbc.connect(SQL_CONN_STR, timeout=5)
    cursor = conn.cursor()
    
    # 1. Test: Veritabanı versiyonunu sor (Okuma testi)
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print(f"✅ BAŞARILI! Sunucuya bağlandın. Versiyon: {row[0][:50]}...")
    
    # 2. Test: Tabloyu okuyabiliyor muyuz? (Tablo yetkisi testi)
    try:
        cursor.execute("SELECT TOP 1 * AD")
        print("✅ Tablo okuma yetkisi VAR.")
    except Exception as e:
        print(f"⚠️ Tabloya erişim YOK: {e}")

    conn.close()

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print("\n❌ BAĞLANTI BAŞARISIZ!")
    print(f"Hata Kodu: {sqlstate}")
    
    if "28000" in str(sqlstate) or "18456" in str(ex):
        print("🔴 SEBEP: Kullanıcı adı veya şifre yanlış (Login Failed).")
    elif "08001" in str(sqlstate):
        print("🔴 SEBEP: Sunucuya ulaşılamıyor (IP yanlış, Firewall engelliyor veya SQL Servisi kapalı).")
    elif "4060" in str(sqlstate):
        print("🔴 SEBEP: Kullanıcı doğru ama 'Sirket1' veritabanına giriş yetkisi yok.")
    else:
        print(f"🔴 Detay: {ex}")