# CTF Virus Lab

CTF Virus Lab, küçük dosya örneklerini **çalıştırmadan** inceleyen ve yalnız sentetik olay kayıtlarını
tekrar oynatan çevrimdışı bir malware araştırma laboratuvarıdır. Amaç; statik triage, IOC çıkarımı,
davranış zaman çizelgesi ve MITRE ATT&CK ilişkilendirmesini güvenli bir eğitim ortamında öğretmektir.

> Bu sürüm ajan, reverse shell veya zararlı yazılım değildir. Socket açmaz, C2'ye bağlanmaz, komut
> çalıştırmaz, süreç başlatmaz, dosya taşımaz/silmez ve anti-VM/anti-debug kaçınması yapmaz. Eski
> `agent.py` yalnız yeni güvenli CLI için uyumluluk sarmalayıcısıdır.

## Temel özellikler

- En fazla 8 MiB normal dosyada salt-okunur statik triage
- SHA-256/SHA-1, dosya türü, Shannon entropisi ve yüksek entropi bölgeleri
- Sınırlı ASCII ve UTF-16LE dize çıkarımı
- URL, domain, IPv4, e-posta, SHA-256, kayıt anahtarı ve dosya yolu IOC adayları
- Açıklanabilir yerleşik kurallar ve MITRE ATT&CK teknik eşleştirmeleri
- Text, JSON, JSONL, SARIF 2.1.0 ve STIX 2.1 çıktıları
- Türkçe CLI ve isteğe bağlı PyQt5 GUI

## İleri özellikler

### 1. Sentetik davranış replay ve zaman çizelgesi

En fazla 1000 JSONL olay; zaman sırası doğrulanarak, işletim sistemine hiçbir işlem uygulanmadan
tekrar oynatılır. Kalıcılık, kimlik bilgisi erişimi, yedek silme, savunmadan kaçınma, betik
yorumlayıcısı, ağ niyeti ve toplu yeniden adlandırma sinyalleri açıklanır.

Örnek bir inert olay:

```json
{"timestamp":"2026-01-01T00:00:00Z","type":"file-read","process":"demo","target":"sample.txt"}
```

### 2. IOC ilişki grafiği ve STIX 2.1

Örnek ile çıkarılan IOC adayları arasında küçük ve kullanıcı verisini çalıştırmayan Mermaid grafiği
üretilir. `--format stix`, IOC'leri deterministik kimliklerle STIX 2.1 bundle olarak verir. Her IOC
**needs-validation** etiketi taşır; pasif çıkarım doğrulanmış kötü niyet anlamına gelmez.

### 3. Açıklanabilir risk + MITRE ATT&CK

Her bulgu; kural kimliği, önem, puan katkısı, kanıt, gerekçe, öneri ve varsa ATT&CK tekniğini içerir.
0–100 puan yalnız inceleme önceliğidir; malware hükmü değildir.

### 4. Baseline karşılaştırması

İki örneğin hash, tür, entropi, risk, kural ve IOC farkları çıkarılır. Böylece aynı laboratuvar
örneğinin iki sürümü arasında neyin değiştiği görülebilir.

### 5. Karantina planı simülasyonu

`quarantine-plan`, önerilen hash tabanlı ad, nedenler ve doğrulama token'ı üretir. Kaynak dosyayı
kopyalamaz, taşımaz, silmez veya izinlerini değiştirmez.

## Güvenlik sözleşmesi

- Örnek dosya en fazla 8 MiB, olay izi en fazla 1 MiB/1000 olaydır.
- Yalnız normal dosyalar okunur; son bileşende symlink, FIFO, socket, device ve dizin reddedilir.
- Dize sayısı 200, IOC sayısı 256, graf düğümü 64 ve text zaman çizelgesi 100 olayla sınırlıdır.
- Örnek hiçbir biçimde import edilmez, ayrıştırıcıya yüklenmez veya çalıştırılmaz.
- Arşiv açma, macro çalıştırma, disassembly, emülasyon, sandbox başlatma ve ağ sorgusu yoktur.
- Karantina ve olay replay yalnız rapordur; dosya sistemi/registry/süreç/ağ değişikliği yapmaz.
- Testler DNS, socket ve yaygın subprocess yollarını otomatik olarak engeller.

## Kurulum

Python 3.10–3.13 desteklenir:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

Çekirdek CLI çalışma zamanında üçüncü taraf bağımlılık kullanmaz. GUI yalnız istenirse kurulabilir:

```bash
python -m pip install -e '.[gui]'
```

## Kullanım

```bash
ctf-virus-lab triage tests/fixtures/harmless.txt
ctf-virus-lab triage tests/fixtures/harmless.txt --format json
ctf-virus-lab triage tests/fixtures/harmless.txt --format sarif > report.sarif
ctf-virus-lab triage tests/fixtures/harmless.txt --format stix > indicators.stix.json

ctf-virus-lab replay tests/fixtures/synthetic_trace.jsonl
ctf-virus-lab compare left.sample right.sample --format json
ctf-virus-lab quarantine-plan tests/fixtures/harmless.txt
```

GUI:

```bash
ctf-virus-lab-gui
```

Eski giriş noktası yalnız CLI sarmalayıcısıdır:

```bash
python agent.py --help
```

## Tek komutlu doğrulama

Bootstrap tamamlandıktan sonra şu komut ağsız çalışır:

```bash
QT_QPA_PLATFORM=offscreen make verify PYTHON=.venv/bin/python
```

Ruff, strict mypy, pytest, compileall, `python -m build --no-isolation`, wheel/sdist içerik denetimi
ve smoke testlerini çalıştırır. GitHub Actions, Python 3.10–3.13 matrisinde aynı hedefi çağırır.

## Etik kullanım

Yalnız sahibi olduğunuz veya açıkça inceleme izni aldığınız örnekleri kullanın. Gerçek zararlı
örnekleri günlük sisteme indirmeyin; bu araç izolasyonun yerine geçmez. Bulgular ve IOC adayları insan
doğrulaması gerektirir.

## Lisans

[MIT](LICENSE)

