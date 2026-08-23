# Katkıda Bulunma

Katkılar salt-okunur, çevrimdışı ve savunma odaklı kalmalıdır.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
make bootstrap PYTHON=.venv/bin/python
QT_QPA_PLATFORM=offscreen make verify PYTHON=.venv/bin/python
```

## Kabul edilmeyen katkılar

- C2, reverse/bind shell, listener veya gerçek ağ bağlantısı
- Komut çalıştırma, süreç enjeksiyonu, kalıcılık ya da kimlik bilgisi toplama
- Anti-VM, anti-debug, gizleme veya güvenlik ürünü atlatma
- Gerçek karantina taşıma/silme ya da sistem yapılandırması değiştirme
- Örnek import etme, çalıştırma, emüle etme veya macro yürütme
- Sınırsız arşiv, regex, olay, dize, IOC veya çıktı işleme
- Gerçek token, parola, kişisel veri veya aktif hedef

Yeni kurallar inert sentetik olaylarla, yanlış pozitif açıklamasıyla ve regresyon testiyle gelmelidir.

