# 🚀 AutoShare - YouTube to Social Media

**YouTube videolarınızı otomatik olarak Instagram Reels ve TikTok'a paylaşın!**

## ✨ Özellikler

✅ **YouTube Video İndirme** - En iyi kalitede otomatik indirme
✅ **Otomatik Format Dönüşümü** - Yatay videoları dikey formata (9:16) çevirir
✅ **Instagram Reels Hazırlama** - 1080x1920 çözünürlükte hazır video
✅ **TikTok Otomatik Yükleme** - Resmi API ile güvenli yükleme
✅ **Güvenli** - Şifre istemiyor, sadece OAuth yetkilendirme
✅ **Onay Mekanizması** - Her platform için kontrol sizde

---

## 📋 Gereksinimler

### 1. Sistem Gereksinimleri

- **Python 3.10+** (Python 3.9 desteği kaldırıldı)
- **FFmpeg** (video işleme için)
- **FFprobe** (FFmpeg ile birlikte gelir)

### 2. FFmpeg Kurulumu

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- [FFmpeg İndir](https://ffmpeg.org/download.html)
- PATH'e ekleyin

**Kontrol:**
```bash
ffmpeg -version
ffprobe -version
```

---

## 🔧 Kurulum

### 1. Python Paketlerini Kurun

```bash
pip install -r requirements.txt
```

Bu şunları kurar:
- `yt-dlp` - YouTube video downloader
- `requests` - TikTok API istekleri için

### 2. TikTok API Kurulumu (Opsiyonel - TikTok yüklemesi için gerekli)

#### a) TikTok Developer Hesabı Oluşturun
1. [TikTok for Developers](https://developers.tiktok.com/) adresine gidin
2. Hesap oluşturun ve giriş yapın

#### b) Uygulama Oluşturun
1. "My Apps" → "Create an App"
2. Uygulama adı: **AutoShare**
3. Kategori: **Content Creation**
4. "Content Posting API" seçeneğini işaretleyin

#### c) OAuth 2.0 Yetkilendirmesi
1. **Redirect URI** ayarlayın: `http://localhost:8000/callback`
2. **Scopes** bölümünde `video.upload` seçeneğini işaretleyin
3. Access Token alın

#### d) Access Token'ı Kaydedin

**Linux/macOS:**
```bash
export TIKTOK_ACCESS_TOKEN='your_access_token_here'
```

**Windows:**
```cmd
set TIKTOK_ACCESS_TOKEN=your_access_token_here
```

**Kalıcı Kayıt (.bashrc veya .zshrc):**
```bash
echo 'export TIKTOK_ACCESS_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

⚠️ **Önemli:** Access token'lar genelde 24 saat geçerlidir. Refresh token ile yenilenebilir.

---

## 🎬 Kullanım

### Temel Kullanım (Sadece Instagram için hazırla)

```bash
python autoshare_workflow.py "https://www.youtube.com/watch?v=XXXXX"
```

**Sonuç:**
- ✅ YouTube'dan video indirilir
- ✅ Instagram Reels için dikey video (9:16) oluşturulur
- ℹ️ TikTok yüklemesi yapılmaz (token yok)

### TikTok'a da Yükle

```bash
# Önce token'ı ayarlayın
export TIKTOK_ACCESS_TOKEN='your_token_here'

# Sonra çalıştırın
python autoshare_workflow.py "https://www.youtube.com/watch?v=XXXXX" "Video Başlığı" "Video açıklaması"
```

**Sonuç:**
- ✅ YouTube'dan video indirilir
- ✅ Instagram Reels için dikey video oluşturulur
- ✅ TikTok'a otomatik yüklenir

### Parametre Açıklaması

```bash
python autoshare_workflow.py <YOUTUBE_URL> [BAŞLIK] [AÇIKLAMA]
```

- `YOUTUBE_URL` **(zorunlu)**: YouTube video linki
- `BAŞLIK` (opsiyonel): TikTok başlığı (varsayılan: "AutoShare Video")
- `AÇIKLAMA` (opsiyonel): TikTok açıklaması

---

## 📂 Çıktı Dosyaları

Tüm videolar `autoshare_videos/` klasörüne kaydedilir:

```
autoshare_videos/
├── youtube_original.mp4          # Orijinal YouTube videosu
├── instagram_reels_9x16.mp4      # Instagram Reels için hazır video
└── last_run_results.json         # Son çalıştırma sonuçları
```

### Instagram'a Manuel Yükleme

1. `autoshare_videos/instagram_reels_9x16.mp4` dosyasını telefonunuza gönderin
2. Instagram uygulamasını açın
3. "+" → "Reels" → Videoyu seçin
4. Paylaş!

---

## 🎯 Örnek Senaryolar

### Senaryo 1: Sadece Instagram için Hazırla (En Güvenli)

```bash
python autoshare_workflow.py "https://youtube.com/watch?v=abc123"
```

**Ne yapar:**
- YouTube'dan videoyu indirir
- Instagram Reels formatına çevirir (1080x1920)
- Dosyayı kaydeder
- Siz manuel yüklersiniz

### Senaryo 2: TikTok'a Otomatik Yükle

```bash
export TIKTOK_ACCESS_TOKEN='eyJhbGciOiJIUzI1Ni...'
python autoshare_workflow.py "https://youtube.com/watch?v=abc123" "Harika Video!" "#fyp #viral"
```

**Ne yapar:**
- YouTube'dan videoyu indirir
- Hem Instagram hem TikTok için formatlar
- TikTok'a otomatik yükler
- Instagram için hazır dosya bırakır

### Senaryo 3: Birden Fazla Video İşle

```bash
#!/bin/bash
# process_multiple.sh

VIDEOS=(
    "https://youtube.com/watch?v=abc123"
    "https://youtube.com/watch?v=def456"
    "https://youtube.com/watch?v=ghi789"
)

for video in "${VIDEOS[@]}"; do
    python autoshare_workflow.py "$video" "Auto Video" "#content"
    echo "✅ Video işlendi: $video"
    sleep 5  # API rate limiting için bekle
done
```

---

## ⚠️ Önemli Notlar

### TikTok API Kısıtlamaları

1. **Private Mode:** Doğrulanmamış uygulamalar için yüklenen videolar **private (gizli)** kalır
   - Çözüm: TikTok'ta uygulamanızı doğrulatın
   - Alternatif: Manual olarak public yapın

2. **Rate Limiting:** TikTok API'sinin hız limitleri var
   - Çok fazla video ardarda yüklerseniz geçici bloklanabilirsiniz
   - Videolar arasında 5-10 saniye bekleyin

3. **Video Gereksinimleri:**
   - Format: MP4, MOV, WEBM
   - Codec: H.264 veya H.265
   - Maksimum boyut: 4 GB
   - Maksimum süre: 10 dakika (doğrulanmış hesaplar için daha uzun)
   - Çözünürlük: 1080x1920 (9:16) önerilir

### Instagram Kısıtlamaları

1. **Manuel Yükleme:** Instagram Reels için resmi API yok
   - AutoShare videoyu **hazırlar**, yükleme manuel

2. **Video Gereksinimleri:**
   - Format: MP4
   - Codec: H.264
   - Maksimum boyut: 300 MB
   - Maksimum süre: 90 saniye (Reels için)
   - Çözünürlük: 1080x1920 (9:16)

### Güvenlik

- ❌ **Asla GitHub'a token yüklemeyin**
- ✅ Environment variables kullanın
- ✅ `.env` dosyasını `.gitignore`'a ekleyin
- ✅ Token'ları düzenli olarak yenileyin

---

## 🐛 Sorun Giderme

### Hata: `yt-dlp: command not found`

**Çözüm:**
```bash
pip install --upgrade yt-dlp
```

### Hata: `ffmpeg: command not found`

**Çözüm:**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Hata: `TikTok upload failed: Invalid access token`

**Çözüm:**
1. Token'ın doğru kopyalandığını kontrol edin
2. Token'ın süresi dolmuş olabilir, yeni token alın
3. Scope'ların doğru olduğunu kontrol edin (`video.upload`)

### Hata: `Video too large for TikTok`

**Çözüm:**
TikTok maksimum 4 GB kabul eder. Videoyu sıkıştırın:
```bash
ffmpeg -i input.mp4 -b:v 2M -b:a 128k output.mp4
```

---

## 📚 Kaynaklar

- [TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Instagram Reels Specs](https://www.facebook.com/business/help/instagram-reels/get-started/reels-technical-requirements)

---

## 📄 Lisans

Bu proje kişisel kullanım içindir. Ticari kullanım için TikTok API Terms of Service'i inceleyin.

---

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add some amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📧 İletişim

Sorularınız için issue açabilirsiniz!

**AutoShare** - YouTube'dan sosyal medyaya en kolay yol 🚀
