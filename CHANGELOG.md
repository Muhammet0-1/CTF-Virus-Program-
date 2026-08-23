# Değişiklik Günlüğü

## 3.0.0 - 2026-08-23

### Eklendi

- Kurulabilir `src/` paketi, Türkçe CLI ve isteğe bağlı PyQt5 GUI.
- Salt-okunur hash, tür, entropi, bölgesel entropi ve dize triage'ı.
- Sınırlı IOC çıkarımı, Mermaid ilişki grafiği ve STIX 2.1 bundle.
- Sentetik JSONL olay replay'ı, zaman çizelgesi ve davranış grafiği.
- Açıklanabilir risk puanları ve MITRE ATT&CK eşleştirmeleri.
- Baseline karşılaştırması ve eylemsiz karantina planı.
- Text, JSON, JSONL ve SARIF raporları.
- Ağ/süreç engelleyici testler, Python 3.10–3.13 CI ve ağsız `make verify`.

### Kaldırıldı

- Reverse shell ve C2 socket bağlantısı.
- `shell=True` komut çalıştırma ve uzaktan komut döngüsü.
- Anti-VM, anti-debug ve analizden kaçınma davranışları.
- Sistem/host bilgisini uzak tarafa gönderme.

