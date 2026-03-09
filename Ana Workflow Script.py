"""
AutoShare - Ana Workflow
YouTube → Instagram Reels ve TikTok otomasyonu
"""

import os
import sys
from pathlib import Path
from video_processor import VideoProcessor
from tiktok_uploader import TikTokUploader


class AutoShare:
    """AutoShare ana sınıfı - Tüm workflow'u yönetir"""

    def __init__(self, tiktok_access_token=None):
        self.video_processor = VideoProcessor(output_dir="autoshare_videos")
        self.tiktok_uploader = TikTokUploader(tiktok_access_token) if tiktok_access_token else None

    def process_youtube_video(self, youtube_url, video_title, video_description="",
                              upload_to_tiktok=True, prepare_for_instagram=True):
        """
        YouTube videosunu işler ve sosyal medyaya hazırlar/yükler

        Args:
            youtube_url: YouTube video URL'i
            video_title: Video başlığı (TikTok için)
            video_description: Video açıklaması
            upload_to_tiktok: TikTok'a otomatik yükle (True/False)
            prepare_for_instagram: Instagram için hazırla (True/False)

        Returns:
            dict: İşlem sonuçları
        """
        results = {
            "youtube_download": None,
            "instagram_ready": None,
            "tiktok_upload": None
        }

        try:
            # 1. YouTube'dan videoyu indir
            print("\n" + "="*60)
            print("🚀 AUTOSHARE BAŞLADI")
            print("="*60)

            original_video = self.video_processor.download_youtube_video(
                youtube_url,
                "youtube_original"
            )
            results["youtube_download"] = {
                "success": True,
                "path": original_video
            }

            # Video bilgilerini al
            video_info = self.video_processor.get_video_info(original_video)
            print(f"\n📊 Video Bilgileri:")
            print(f"   Süre: {video_info.get('duration_seconds')} saniye")
            print(f"   Boyut: {video_info.get('file_size_mb')} MB")
            print(f"   Çözünürlük: {video_info.get('width')}x{video_info.get('height')}")

            # 2. Instagram Reels için hazırla
            if prepare_for_instagram:
                print("\n" + "-"*60)
                print("📱 INSTAGRAM REELS İÇİN HAZIRLANIYOR")
                print("-"*60)

                instagram_video = self.video_processor.convert_to_vertical(
                    original_video,
                    "instagram_reels"
                )

                instagram_info = self.video_processor.get_video_info(instagram_video)

                results["instagram_ready"] = {
                    "success": True,
                    "path": instagram_video,
                    "size_mb": instagram_info.get('file_size_mb'),
                    "resolution": f"{instagram_info.get('width')}x{instagram_info.get('height')}",
                    "message": "Instagram Reels videosu hazır! Manuel olarak yükleyebilirsiniz."
                }

                print(f"\n✅ Instagram Reels videosu hazır:")
                print(f"   Dosya: {instagram_video}")
                print(f"   Boyut: {instagram_info.get('file_size_mb')} MB")
                print(f"   Çözünürlük: {instagram_info.get('width')}x{instagram_info.get('height')}")
                print(f"\n   ℹ️  Bu videoyu Instagram uygulaması ile manuel yükleyebilirsiniz.")

            # 3. TikTok'a yükle (eğer istenmişse)
            if upload_to_tiktok:
                print("\n" + "-"*60)
                print("🎵 TIKTOK'A YÜKLENIYOR")
                print("-"*60)

                if not self.tiktok_uploader:
                    print("⚠️  TikTok access token bulunamadı!")
                    print("   TikTok yüklemesi atlandı.")
                    results["tiktok_upload"] = {
                        "success": False,
                        "error": "Access token yok"
                    }
                else:
                    # Dikey videoyu TikTok için kullan
                    tiktok_video = instagram_video if prepare_for_instagram else self.video_processor.convert_to_vertical(
                        original_video,
                        "tiktok_video"
                    )

                    tiktok_result = self.tiktok_uploader.upload_video(
                        tiktok_video,
                        title=video_title,
                        description=video_description,
                        privacy_level="PUBLIC_TO_EVERYONE"
                    )

                    results["tiktok_upload"] = tiktok_result

                    if tiktok_result.get("success"):
                        print(f"\n✅ TikTok'a başarıyla yüklendi!")
                        print(f"   Publish ID: {tiktok_result.get('publish_id')}")
                        print(f"\n   ⚠️  Not: Doğrulanmamış uygulamalar için video 'private' kalır.")
                        print(f"   TikTok'ta uygulamanızı doğrulatarak public yapabilirsiniz.")

            # 4. Özet
            print("\n" + "="*60)
            print("✅ AUTOSHARE TAMAMLANDI")
            print("="*60)
            print(f"\n📂 Tüm dosyalar: {self.video_processor.output_dir}")

            return results

        except Exception as e:
            print(f"\n❌ HATA: {str(e)}")
            return {
                "error": str(e),
                "results": results
            }


def main():
    """Komut satırı kullanımı"""
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║          AutoShare - YouTube to Social Media             ║")
    print("║       Instagram Reels & TikTok Automation Tool           ║")
    print("╚═══════════════════════════════════════════════════════════╝")

    if len(sys.argv) < 2:
        print("\n❌ Kullanım hatası!")
        print("\n📖 Kullanım:")
        print("   python autoshare_workflow.py <YOUTUBE_URL> [BAŞLIK] [AÇIKLAMA]")
        print("\n📝 Örnek:")
        print("   python autoshare_workflow.py 'https://youtube.com/watch?v=xxxxx' 'Harika Video' 'Açıklama'")
        print("\n🔑 TikTok için:")
        print("   export TIKTOK_ACCESS_TOKEN='your_token_here'")
        sys.exit(1)

    youtube_url = sys.argv[1]
    video_title = sys.argv[2] if len(sys.argv) > 2 else "AutoShare Video"
    video_description = sys.argv[3] if len(sys.argv) > 3 else ""

    # TikTok access token'ı environment variable'dan al
    tiktok_token = os.getenv("TIKTOK_ACCESS_TOKEN")

    if not tiktok_token:
        print("\n⚠️  UYARI: TIKTOK_ACCESS_TOKEN bulunamadı!")
        print("   TikTok yüklemesi yapılamayacak.")
        print("   Sadece Instagram Reels videosu hazırlanacak.\n")

    # AutoShare workflow'u başlat
    autoshare = AutoShare(tiktok_access_token=tiktok_token)

    results = autoshare.process_youtube_video(
        youtube_url=youtube_url,
        video_title=video_title,
        video_description=video_description,
        upload_to_tiktok=bool(tiktok_token),  # Token varsa TikTok'a yükle
        prepare_for_instagram=True  # Her zaman Instagram için hazırla
    )

    # Sonuçları JSON olarak da kaydet
    import json
    results_file = Path("autoshare_videos") / "last_run_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Sonuçlar kaydedildi: {results_file}")


if __name__ == "__main__":
    main()
