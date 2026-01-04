#!/bin/bash

echo "ANLIK KRİPTO VERİLERİ"

dosya=$(pwd)

cleanup() {
    echo ""
    echo "Kapatılıyor..."
    kill $!
    echo "Arka plan işlemi ($!) sonlandırıldı. ! Kontrol etmek icin|=> ps aux | grep 'bash' kullanın"
    exit
}
# EXIT sinyali gelince cleanup fonksiyonunu çalışır
trap cleanup SIGINT EXIT

(
while true;do
    python3 $dosya/c.py
    sleep 5
done
) &
if [ ! -f "$dosya/veriler.csv" ]; then
    sleep 5
fi

echo " Çıkmak için Ctrl+C"
echo "------------------------------------------------"
tail -f $dosya/veriler.csv 