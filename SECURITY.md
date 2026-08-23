# Güvenlik Politikası

## Desteklenen sürüm

Yalnız güncel `main` sürümü güvenlik düzeltmeleri alır.

## Bildirim

Hassas sorunları herkese açık issue yerine GitHub **Security → Report a vulnerability** üzerinden
bildirin. Gerçek zararlı örnek, kimlik bilgisi, token veya kişisel veri yüklemeyin. Sorunu inert ve en
küçük yerel örnekle yeniden üretin.

## Tehdit modeli

Girdi dosyası ve JSONL iz güvenilmez kabul edilir. Proje küçük eğitim örneklerine yöneliktir; 8 MiB
dosya ve 1000 olay sınırları güvenlik sözleşmesidir. Araç malware çalıştırmaz ve gerçek sandbox,
antivirüs ya da EDR değildir. “Bulgu yok” sonucu güvenlik garantisi sayılmaz.

