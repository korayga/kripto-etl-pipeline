import streamlit as st
import pandas as pd
import sqlite3
import time

st.set_page_config(page_title="SQL Kripto Dashboard", layout="wide")
st.title("Canlı Veritabanı Akışı")

def verileri_sql_ile_getir():
    try:
        # Veritabanına bağlan
        conn = sqlite3.connect('kripto.db')
        
        # SQL Sorgusu: Tüm verileri getir
        query = "SELECT * FROM fiyatlar ORDER BY time DESC LIMIT 1000"
        
        # Pandas ile SQL sonucunu al
        df = pd.read_sql(query, conn)
        conn.close()
        
        if df.empty:
            return df
        
        # Zamanı güncelle
        df['time'] = pd.to_datetime(df['time'])
        return df
    
    except Exception as e:
        st.error(f"Veritabanı hatası: {e}")
        return pd.DataFrame()  # Hata varsa boş dön

placeholder = st.empty()

while True:
    df = verileri_sql_ile_getir()
    
    if not df.empty:
        with placeholder.container(): 
            grafik_tablosu = df.pivot_table(index='time', columns='coin', values='price', aggfunc='last')
            
            st.subheader("📈 Veritabanından Canlı Grafik")
            st.line_chart(grafik_tablosu)
            
            # Son fiyatlar tablosu
            st.subheader("💰 Son Fiyatlar")
            son_fiyatlar = df.sort_values('time', ascending=False).drop_duplicates('coin')[['coin', 'price', 'time']]
            st.dataframe(son_fiyatlar, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"Toplam Veri: {len(df)}")
            with col2:
                son_zaman = df['time'].max()
                st.success(f"Son Güncelleme: {son_zaman}")
            with col3:
                st.metric("Coin Sayısı", df['coin'].nunique())

        time.sleep(2)
    else:
        st.warning("⏳ Veritabanı bekleniyor...")
        time.sleep(2)