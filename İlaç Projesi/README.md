# HealthTrack - İlaç ve Randevu Takip Asistanı

## Proje Hakkında
HealthTrack, yaşlı bireyler ve hasta yakınları için geliştirilmiş, komut satırı üzerinden çalışan bir ilaç ve randevu takip asistanıdır. Kullanıcı dostu arayüzü ile ilaç saatlerini, doktor randevularını ve medikal notları kolayca yönetmenizi sağlar.

## Özellikler
- 👤 Kullanıcı yönetimi (ekleme, düzenleme, silme)
- 💊 İlaç takibi ve hatırlatmaları
- 📅 Randevu yönetimi
- 🔔 Günlük hatırlatmalar
- 📊 Detaylı raporlama
- 💾 Otomatik veri yedekleme (JSON formatında)

## Kurulum
```bash
# Projeyi klonlayın
git clone https://github.com/kullaniciadi/healthtrack.git
cd healthtrack

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
python main.py
```

## Kullanım
```bash
# Normal başlatma
python main.py

# Sadece bugünkü görevleri görüntüleme
python main.py --today

# Rapor çıktısı alma
python main.py --export
```

## Komutlar
- `1` - Kullanıcı Ekle/Düzenle
- `2` - Randevu Yönetimi
- `3` - İlaç Takibi
- `4` - Günlük Özet
- `5` - Rapor Oluştur
- `6` - Ayarlar
- `q` - Çıkış

## Gereksinimler
- Python 3.8+
- inquirer
- rich
- typer

## Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

## İletişim
Sorularınız ve önerileriniz için Issues bölümünü kullanabilirsiniz. 