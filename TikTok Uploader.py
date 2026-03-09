"""
AutoShare TikTok Uploader
TikTok Content Posting API entegrasyonu
"""

import requests
import os
import json
from pathlib import Path


class TikTokUploader:
    """TikTok'a video yükler (Content Posting API)"""

    def __init__(self, access_token):
        """
        Args:
            access_token: TikTok OAuth 2.0 access token
        """
        self.access_token = access_token
        self.base_url = "https://open.tiktokapis.com/v2/post/publish"

    def upload_video(self, video_path, title, description="", privacy_level="PUBLIC_TO_EVERYONE"):
        """
        TikTok'a video yükler

        Args:
            video_path: Yüklenecek video dosyası yolu
            title: Video başlığı
            description: Video açıklaması (opsiyonel)
            privacy_level: Gizlilik seviyesi (PUBLIC_TO_EVERYONE, MUTUAL_FOLLOW_FRIENDS, SELF_ONLY)

        Returns:
            dict: Upload sonucu ve publish_id
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video dosyası bulunamadı: {video_path}")

        # Dosya boyutunu kontrol et (TikTok limiti genelde 4GB)
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        if file_size > 4000:
            raise ValueError(f"Video çok büyük: {file_size:.2f} MB (Maksimum: 4000 MB)")

        print(f"📤 TikTok'a video yükleniyor: {title}")
        print(f"   Dosya: {video_path} ({file_size:.2f} MB)")

        # 1. Video yükleme isteği başlat
        init_response = self._initialize_upload(title, description, privacy_level)

        if "error" in init_response:
            raise Exception(f"TikTok upload başlatılamadı: {init_response['error']}")

        publish_id = init_response.get("publish_id")
        upload_url = init_response.get("upload_url")

        if not upload_url:
            raise Exception("TikTok upload URL'i alınamadı")

        # 2. Video dosyasını yükle
        upload_result = self._upload_file(upload_url, video_path)

        if upload_result.get("success"):
            print(f"✅ Video TikTok'a yüklendi!")
            print(f"   Publish ID: {publish_id}")
            print(f"   ⚠️  Not: Doğrulanmamış uygulamalar için video 'private' kalır.")
            return {
                "success": True,
                "publish_id": publish_id,
                "message": "Video başarıyla yüklendi (private mode)"
            }
        else:
            raise Exception(f"Video yüklenemedi: {upload_result.get('error')}")

    def _initialize_upload(self, title, description, privacy_level):
        """
        TikTok upload'ı başlatır ve upload URL'i alır

        Returns:
            dict: publish_id ve upload_url içeren response
        """
        url = f"{self.base_url}/video/init/"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=UTF-8"
        }

        payload = {
            "post_info": {
                "title": title,
                "description": description,
                "privacy_level": privacy_level,
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000
            },
            "source_info": {
                "source": "FILE_UPLOAD"
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("error"):
                return {"error": data["error"]}

            return data.get("data", {})

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def _upload_file(self, upload_url, video_path):
        """
        Video dosyasını TikTok'un verdiği URL'e yükler

        Args:
            upload_url: TikTok'tan alınan upload URL'i
            video_path: Yüklenecek video dosyası

        Returns:
            dict: Upload sonucu
        """
        try:
            with open(video_path, 'rb') as video_file:
                headers = {
                    "Content-Type": "video/mp4"
                }

                response = requests.put(
                    upload_url,
                    data=video_file,
                    headers=headers,
                    timeout=300  # 5 dakika timeout (büyük dosyalar için)
                )

                if response.status_code in [200, 201]:
                    return {"success": True}
                else:
                    return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_upload_status(self, publish_id):
        """
        Video yükleme durumunu kontrol eder

        Args:
            publish_id: Upload sırasında alınan publish_id

        Returns:
            dict: Upload durumu (PUBLISH_COMPLETE, PROCESSING_DOWNLOAD, FAILED, etc.)
        """
        url = f"{self.base_url}/status/fetch/"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=UTF-8"
        }

        payload = {
            "publish_id": publish_id
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            return data.get("data", {})

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


def main():
    """Test fonksiyonu - gerçek kullanım için access token gereklidir"""
    print("TikTok Uploader - Test Modu")
    print("=" * 50)
    print("\n⚠️  Bu script'i kullanmak için:")
    print("1. TikTok Developers'da bir uygulama oluşturun")
    print("2. OAuth 2.0 ile kullanıcı yetkilendirmesi yapın")
    print("3. Access token alın (video.upload scope'u gerekli)")
    print("4. Access token'ı environment variable olarak ayarlayın:")
    print("   export TIKTOK_ACCESS_TOKEN='your_token_here'")
    print("\nKaynak: https://developers.tiktok.com/doc/content-posting-api-get-started")


if __name__ == "__main__":
    main()
