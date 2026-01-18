# 🦠 Advanced Malware Research Agent

![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Security-Red%20Team-red?style=for-the-badge)

Bu proje, modern zararlı yazılımların (malware) analizden kaçınmak için kullandığı teknikleri (Evasion Techniques) simüle eden, eğitim amaçlı bir **Red Team Ajanı**dır.

Klasik reverse shell scriptlerinin aksine, bu ajan çalıştığı ortamı analiz eder ve eğer bir tehdit (Debugger veya Sandbox) algılarsa davranışını değiştirir.

## 🛡️ Teknik Özellikler

### 1. Anti-Analysis (Analizden Kaçınma)
* **Anti-Debugging (Timing Check):** Kodun çalışması sırasında mikrosaniyelik gecikmeleri ölçerek bir debugger tarafından adım adım izlenip izlenmediğini tespit eder.
* **Anti-VM (MAC OUI Check):** Sistem MAC adresini analiz ederek VMware, VirtualBox veya Hyper-V gibi sanallaştırma platformlarında çalışıp çalışmadığını anlar.

### 2. Güvenli Mod (Safe Mode)
* Varsayılan olarak `SAFE_MODE = True` ile gelir.
* Bu modda, sunucudan gelen komutlar **asla sistemde çalıştırılmaz**. Sadece simüle edilir ve loglanır. Bu sayede kazara zarar verme riski ortadan kaldırılır.

## 🚀 Kurulum ve Test

1. **Dinleyiciyi Başlatın (Netcat veya Metasploit):**
   ```bash
   nc -lvnp 4444
   
2. Ajanı Çalıştırın:
    Bash

    python agent.py

    Gözlemleyin: Terminalde ortam analiz raporunu ve bağlantı durumunu göreceksiniz.

⚠️ Yasal Uyarı

Bu yazılım sadece eğitim ve araştırma amaçlıdır. Zararlı yazılımların nasıl çalıştığını anlamak ve savunma mekanizmalarını geliştirmek için tasarlanmıştır. İzinsiz sistemlerde kullanmak suçtur.
