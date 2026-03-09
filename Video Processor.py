"""
AutoShare Video Processor
YouTube video indirme ve format dönüştürme modülü
"""

import subprocess
import os
import sys
from pathlib import Path


class VideoProcessor:
    """YouTube videolarını indirir ve sosyal medya platformları için formatlar"""

    def __init__(self, output_dir="downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def download_youtube_video(self, youtube_url, output_filename="video"):
        """
        YouTube'dan video indirir

        Args:
            youtube_url: YouTube video URL'i
            output_filename: Çıktı dosya adı (uzantısız)

        Returns:
            str: İndirilen videonun tam yolu
        """
        output_path = self.output_dir / f"{output_filename}.mp4"

        # yt-dlp ile YouTube videosu indir (en iyi kalite)
        cmd = [
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", str(output_path),
            youtube_url
        ]

        print(f"📥 YouTube'dan video indiriliyor: {youtube_url}")
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ Video indirildi: {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            print(f"❌ Video indirme hatası: {e.stderr}")
            raise Exception(f"YouTube video indirilemedi: {e.stderr}")

    def convert_to_vertical(self, input_video, output_filename="vertical_video"):
        """
        Yatay videoyu dikey formata (9:16) dönüştürür
        Instagram Reels ve TikTok için optimize edilmiştir

        Args:
            input_video: Kaynak video yolu
            output_filename: Çıktı dosya adı (uzantısız)

        Returns:
            str: Dönüştürülmüş videonun tam yolu
        """
        output_path = self.output_dir / f"{output_filename}_9x16.mp4"

        # FFmpeg ile 9:16 (1080x1920) formatına dönüştür
        # Ortadan kırp (center crop) ve ölçeklendir
        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-vf", "crop=ih*9/16:ih,scale=1080:1920",
            "-c:v", "libx264",
            "-preset", "medium",
            "-profile:v", "high",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            str(output_path)
        ]

        print(f"🎬 Video dikey formata dönüştürülüyor (9:16)...")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ Dikey video oluşturuldu: {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            print(f"❌ Video dönüştürme hatası: {e.stderr}")
            raise Exception(f"Video formatlanamadı: {e.stderr}")

    def get_video_info(self, video_path):
        """
        Video hakkında bilgi döndürür (süre, boyut, format)

        Args:
            video_path: Video dosya yolu

        Returns:
            dict: Video bilgileri
        """
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            import json
            data = json.loads(result.stdout)

            # Video stream'ini bul
            video_stream = next(
                (s for s in data.get('streams', []) if s.get('codec_type') == 'video'),
                None
            )

            if not video_stream:
                return {"error": "Video stream bulunamadı"}

            file_size_mb = float(data['format']['size']) / (1024 * 1024)
            duration = float(data['format']['duration'])

            return {
                "duration_seconds": round(duration, 2),
                "file_size_mb": round(file_size_mb, 2),
                "width": video_stream.get('width'),
                "height": video_stream.get('height'),
                "codec": video_stream.get('codec_name'),
                "format": data['format']['format_name']
            }
        except Exception as e:
            return {"error": str(e)}


def main():
    """Test fonksiyonu - komut satırından çalıştırılabilir"""
    if len(sys.argv) < 2:
        print("Kullanım: python video_processor.py <YOUTUBE_URL>")
        sys.exit(1)

    youtube_url = sys.argv[1]

    processor = VideoProcessor()

    # 1. YouTube'dan indir
    original_video = processor.download_youtube_video(youtube_url, "youtube_original")

    # 2. Video bilgilerini göster
    info = processor.get_video_info(original_video)
    print(f"\n📊 Video Bilgileri:")
    print(f"   Süre: {info.get('duration_seconds')} saniye")
    print(f"   Boyut: {info.get('file_size_mb')} MB")
    print(f"   Çözünürlük: {info.get('width')}x{info.get('height')}")

    # 3. Dikey formata dönüştür (Instagram & TikTok için)
    vertical_video = processor.convert_to_vertical(original_video, "instagram_tiktok")

    # 4. Dikey video bilgileri
    vertical_info = processor.get_video_info(vertical_video)
    print(f"\n📊 Dikey Video Bilgileri:")
    print(f"   Boyut: {vertical_info.get('file_size_mb')} MB")
    print(f"   Çözünürlük: {vertical_info.get('width')}x{vertical_info.get('height')}")

    print(f"\n✅ Tamamlandı!")
    print(f"   Orijinal video: {original_video}")
    print(f"   Instagram/TikTok videosu: {vertical_video}")


if __name__ == "__main__":
    main()
