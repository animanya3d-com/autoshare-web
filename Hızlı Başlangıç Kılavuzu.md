# 🚀 AutoShare - Hızlı Başlangıç Kılavuzu

**5 dakikada AutoShare'i kullanmaya başlayın!**

---

## 📦 Kurulum (2 Dakika)

### 1. Python Paketlerini Kurun

```bash
pip install yt-dlp requests
```

### 2. FFmpeg Kurun

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
[FFmpeg İndir](https://ffmpeg.org/download.html) ve PATH'e ekleyin

---

## 🎬 İlk Kullanım (1 Dakika)

### Sadece Instagram için Video Hazırla

```bash
python autoshare_workflow.py "https://www.youtube.com/watch?v=XXXXX"
```

**Ne olur?**
1. ✅ YouTube'dan video indirilir
2. ✅ Instagram Reels formatına (9:16) dönüştürülür
3. 📂 `autoshare_videos/instagram_reels_9x16.mp4` dosyası oluşturulur

**Instagram'a yükle:**
- Dosyayı telefonunuza gönderin
- Instagram → Reels → Videoyu seçin → Paylaş!

---

## 🎵 TikTok'a Otomatik Yükleme (Opsiyonel)

### 1. TikTok Access Token Alın

1. [TikTok for Developers](https://developers.tiktok.com/) → Hesap oluşturun
2. "Create App" → **AutoShare** adını verin
3. "Content Posting API" seçin
4. `video.upload` scope'unu işaretleyin
5. Access Token'ı kopyalayın

### 2. Token'ı Ayarlayın

```bash
export TIKTOK_ACCESS_TOKEN='your_token_here'
```

### 3. Kullanın

```bash
python autoshare_workflow.py "https://youtube.com/watch?v=XXXXX" "Başlık" "#fyp #viral"
```

**Ne olur?**
1. ✅ YouTube'dan video indirilir
2. ✅ Instagram formatına dönüştürülür
3. ✅ TikTok'a otomatik yüklenir
4. 📂 Tüm dosyalar `autoshare_videos/` klasöründe

---

## ⚡ Hızlı Komutlar

### Tek Video İşle
```bash
python autoshare_workflow.py "YOUTUBE_URL"
```

### Başlık ve Açıklama Ekle
```bash
python autoshare_workflow.py "YOUTUBE_URL" "Video Başlığı" "#hashtag açıklama"
```

### Birden Fazla Video
```bash
python autoshare_workflow.py "URL1" "Video 1"
python autoshare_workflow.py "URL2" "Video 2"
python autoshare_workflow.py "URL3" "Video 3"
```

---

## 📂 Dosya Konumları

Tüm çıktılar `autoshare_videos/` klasöründe:

```
autoshare_videos/
├── youtube_original.mp4          # YouTube videosu
├── instagram_reels_9x16.mp4      # Instagram için hazır
└── last_run_results.json         # Son sonuçlar
```

---

## ❓ Sık Sorulan Sorular

### Q: TikTok videosu neden 'private' kalıyor?
**A:** Doğrulanmamış uygulamalar için TikTok API tüm videoları private yapar. TikTok'ta uygulamanızı doğrulatın veya manuel olarak public yapın.

### Q: Instagram API desteği yok mu?
**A:** Instagram Reels için resmi yükleme API'si yok. AutoShare videoyu hazırlar, siz manuel yüklersiniz.

### Q: FFmpeg hatası alıyorum
**A:** FFmpeg kurulu değil. Kurulum komutlarına bakın (yukarıda).

### Q: YouTube video indirilmiyor
**A:** yt-dlp güncel değil olabilir:
```bash
pip install --upgrade yt-dlp
```

---

## 🎯 İlk Kullanım Örneği

```bash
# 1. YouTube'dan video indir ve Instagram için hazırla
python autoshare_workflow.py "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Çıktı:
# ✅ Video indirildi: autoshare_videos/youtube_original.mp4
# ✅ Instagram Reels videosu hazır: autoshare_videos/instagram_reels_9x16.mp4
# ℹ️  Bu videoyu Instagram uygulaması ile manuel yükleyebilirsiniz.

# 2. Instagram'a yükle (Manuel)
# - autoshare_videos/instagram_reels_9x16.mp4 dosyasını telefonunuza gönderin
# - Instagram → + → Reels → Videoyu seçin → Paylaş
```

---

## 📚 Daha Fazla Bilgi

- **Tam Dokümantasyon:** `README.md` dosyasına bakın
- **Sorun mu yaşıyorsunuz?** README.md → "Sorun Giderme" bölümü
- **TikTok API:** [TikTok Developer Docs](https://developers.tiktok.com/doc/content-posting-api-get-started)

---

**AutoShare ile videolarınızı kolayca paylaşın!** 🚀
