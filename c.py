import requests
import pandas as pd
import os
from datetime import datetime
import sqlite3


def veri_cek(j):
    r_list = []
    base_url = "https://api.binance.com/api/v3/ticker/price?symbol="
    try:    
        for coin in j:
            final_url = base_url + coin
            response=requests.get(final_url,timeout=20)
            if response.status_code == 200:
                r_list.append(response.json())
            else:
                print(f"Hata: {coin} verisi çekilemedi.")

    except Exception as e:
        print("API hatası:\n", e)
        return None
    
    return r_list

def coin_cek(dosya_adi="coins.json"):

    if not os.path.exists(dosya_adi):
        print(f"UYARI: {dosya_adi} bulunamadı! Varsayılan liste kullanılıyor.")
        return ["BTCUSDT", "ETHUSDT"]
    try:
        df=pd.read_json(dosya_adi)
        return df["coins"].tolist()
    except Exception as e:
        print("json hatası")
        return ["BTCUSDT", "ETHUSDT"]
    
   

def veri_temizle(v):
    if not v:
        return None
    data = []
    zaman=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for val in v:
        data.append({"coin":val.get("symbol"),"price":val.get("price"),"time":zaman})
    return data
   
        
def csv_kaydet(data):
    if not data:
        print("Kaydedilecek veri yok!")
        return
    df = pd.DataFrame(data)

    df.to_csv("veriler.csv",index=False,mode="a",header=not os.path.exists("veriler.csv"))

def create_database():
    conn = sqlite3.connect("kripto.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS fiyatlar
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   coin TEXT,
                   price REAL,
                   time TEXT)''')
    conn.commit()
    conn.close()
def database_kaydet(data):
    if not data:
        return
    conn = sqlite3.connect("kripto.db")
    cursor = conn.cursor()
    for satir in data:
        cursor.execute("INSERT INTO fiyatlar(coin, price, time) VALUES (?, ?, ?)",
                      (satir["coin"], satir["price"], satir["time"]))
    conn.commit()
    conn.close()
    print(f"✓ SQL'e Kaydedildi: {data[0]['time']}")

        

if __name__ == "__main__":
    create_database()  # İlk çalıştırmada tablo oluştur
    j = coin_cek()
    ham = veri_cek(j)
    temiz_veri = veri_temizle(ham)
    if temiz_veri:
        database_kaydet(temiz_veri)
        csv_kaydet(temiz_veri)