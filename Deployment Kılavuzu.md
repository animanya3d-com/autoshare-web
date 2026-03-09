# 🚀 AutoShare - Vercel Deployment Kılavuzu

**animanya3d.com/autoshare** adresinde AutoShare'i yayınlama rehberi

---

## 📋 Gereksinimler

- ✅ GitHub hesabı
- ✅ Vercel hesabı (ücretsiz)
- ✅ Domain: animanya3d.com (mevcut)

---

## 🎯 Adım 1: GitHub Repository Oluşturun

### 1.1. GitHub'da Yeni Repo Oluşturun

1. [GitHub](https://github.com) → "New Repository"
2. Repository adı: **autoshare-web**
3. Public veya Private (tercihinize göre)
4. "Create repository"

### 1.2. Dosyaları GitHub'a Yükleyin

```bash
# Terminal'de web klasörüne gidin
cd /path/to/autoshare/web

# Git başlatın
git init

# Dosyaları ekleyin
git add .

# Commit yapın
git commit -m "Initial commit: AutoShare web interface"

# GitHub repo'nuza bağlayın (URL'i kendi repo'nuzla değiştirin)
git remote add origin https://github.com/YOUR_USERNAME/autoshare-web.git

# Push yapın
git branch -M main
git push -u origin main
```

✅ **Tamamlandı!** Dosyalarınız GitHub'da.

---

## 🌐 Adım 2: Vercel'de Deploy Edin

### 2.1. Vercel Hesabı Oluşturun

1. [Vercel](https://vercel.com) → "Sign Up"
2. "Continue with GitHub" seçin
3. GitHub hesabınızla giriş yapın

### 2.2. Yeni Proje Oluşturun

1. Vercel Dashboard → **"Add New..."** → **"Project"**
2. **"Import Git Repository"** bölümünde **autoshare-web** repo'nuzu seçin
3. **"Import"** butonuna tıklayın

### 2.3. Proje Ayarları

**Framework Preset:** None (Static HTML seçilecek)

**Build & Output Settings:**
- Build Command: (boş bırakın)
- Output Directory: `.` (nokta)
- Install Command: (boş bırakın)

**Root Directory:** `./` (varsayılan)

### 2.4. Deploy

**"Deploy"** butonuna tıklayın!

⏳ 30-60 saniye içinde deploy tamamlanır.

✅ **Tamamlandı!** Vercel size bir URL verecek: `https://autoshare-web-xxx.vercel.app`

---

## 🔗 Adım 3: Domain Bağlayın (animanya3d.com/autoshare)

### Seçenek A: Subdomain Kullanın (Önerilen - Daha Kolay)

#### 1. Vercel'de Subdomain Ekleyin

1. Vercel Project → **"Settings"** → **"Domains"**
2. **"Add"** butonuna tıklayın
3. Şunu yazın: **`autoshare.animanya3d.com`**
4. **"Add"** tıklayın

#### 2. DNS Ayarları Yapın

Vercel size DNS kayıtları gösterecek. Domain sağlayıcınızda (GoDaddy, Namecheap, Cloudflare vb.) şu kaydı ekleyin:

**CNAME Kaydı:**
```
Type: CNAME
Name: autoshare
Value: cname.vercel-dns.com
```

**veya A Kaydı:**
```
Type: A
Name: autoshare
Value: 76.76.21.21 (Vercel'in gösterdiği IP)
```

#### 3. Bekleyin

DNS yayılımı 5-60 dakika sürebilir. Sonra şu adresle erişebilirsiniz:

✅ **`https://autoshare.animanya3d.com`**

---

### Seçenek B: Path-Based Deployment (animanya3d.com/autoshare)

⚠️ **Not:** Path-based deployment için mevcut `animanya3d.com` sitenizin Vercel'de host edilmesi gerekir.

#### Eğer Ana Domain Vercel'de Değilse:

1. **Reverse Proxy Kullanın** (nginx, Cloudflare Workers)
2. **Subdomain Kullanın** (Seçenek A - Daha kolay!)

#### Eğer Ana Domain Vercel'de İse:

`vercel.json` dosyası zaten path routing destekliyor:

```json
{
  "rewrites": [
    {
      "source": "/autoshare",
      "destination": "/index.html"
    }
  ]
}
```

Bu durumda `animanya3d.com/autoshare` otomatik çalışır.

---

## 🎨 Adım 4: CREAO Backend Entegrasyonu (Opsiyonel)

### Demo Mode'dan Production'a Geçiş

Şu an `app.js` dosyasında **DEMO_MODE: true** var. Gerçek backend için:

#### 1. CREAO Backend Hazırlayın

CREAO workspace'inizde bir API endpoint oluşturun:
- Python FastAPI veya Flask backend
- AutoShare workflow'unu çalıştıran endpoint

Örnek endpoint: `https://your-creao-workspace.com/api/autoshare`

#### 2. `app.js`'i Güncelleyin

```javascript
const CONFIG = {
    CREAO_ENDPOINT: 'https://your-creao-workspace.com/api/autoshare',
    DEMO_MODE: false, // Production moduna geç
};
```

#### 3. GitHub'a Push ve Vercel'de Otomatik Deploy

```bash
git add app.js
git commit -m "Update: CREAO backend integration"
git push origin main
```

Vercel otomatik olarak yeni versiyonu deploy eder! 🚀

---

## ✅ Test Edin

### 1. Siteyi Açın

`https://autoshare.animanya3d.com` veya Vercel URL'iniz

### 2. Demo Test

- YouTube URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Video Başlığı: "Test Video"
- Instagram Reels: ✅ seçili
- **"Videoyu İşle"** butonuna tıklayın

Demo mode'da 5-6 saniye simülasyon çalışır ve sonuç gösterilir.

---

## 🐛 Sorun Giderme

### Domain Bağlanmıyor

**Çözüm:**
1. DNS ayarlarını kontrol edin (doğru CNAME/A kaydı var mı?)
2. DNS yayılımını bekleyin (5-60 dakika)
3. Vercel'de "Domains" bölümünde "Verify" butonuna tıklayın

### Vercel Deploy Hatası

**Çözüm:**
1. GitHub repo'sunuzun public olduğundan emin olun
2. Vercel'de "Root Directory" ayarını `.` olarak bırakın
3. Build Command'ı boş bırakın

### CORS Hatası (CREAO Backend)

**Çözüm:**
CREAO backend'inizde CORS headers ekleyin:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://autoshare.animanya3d.com"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

---

## 📁 Dosya Yapısı

```
web/
├── index.html          # Ana sayfa
├── styles.css          # Stil dosyası
├── app.js             # JavaScript logic + CREAO entegrasyonu
├── vercel.json        # Vercel konfigürasyonu
├── package.json       # Project metadata
├── .gitignore         # Git ignore dosyası
└── DEPLOYMENT_GUIDE.md # Bu dosya
```

---

## 🎯 Özet: Hızlı Kurulum

```bash
# 1. GitHub'a yükle
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/autoshare-web.git
git push -u origin main

# 2. Vercel'de deploy et
# - vercel.com → Import Git Repository → autoshare-web seçin
# - Deploy butonuna tıklayın

# 3. Domain bağla
# - Vercel → Settings → Domains
# - autoshare.animanya3d.com ekleyin
# - DNS'te CNAME kaydı: autoshare → cname.vercel-dns.com

# 4. Test et
# https://autoshare.animanya3d.com
```

---

## 💡 İpuçları

1. **SSL Otomatik:** Vercel otomatik HTTPS sağlar
2. **Ücretsiz:** Vercel Hobby planı yeterli (ücretsiz)
3. **Otomatik Deploy:** GitHub'a her push'ta Vercel otomatik deploy yapar
4. **Analytics:** Vercel → Analytics bölümünden ziyaretçi istatistikleri

---

## 📧 Destek

Sorun yaşarsanız:
- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- support@animanya3d.com

---

**AutoShare - animanya3d.com/autoshare adresinde canlı! 🎉**
