import os
import re
import sys
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_PATH = shutil.which("ffmpeg")

import yt_dlp
import instaloader


class InstagramDownloader:
    """
    Free and modular Instagram downloader supporting Reels, Videos,
    Single Photos, and Multi-slide Carousels.
    """

    def __init__(self, output_dir: str = "insta_videos_downloads", browser_cookies: Optional[str] = None):
        """
        :param output_dir: Folder where media will be saved.
        :param browser_cookies: Optional browser name to extract session cookies from (e.g. 'chrome', 'edge', 'firefox').
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.browser_cookies = browser_cookies
        self._init_instaloader()

    def _init_instaloader(self):
        self.loader = instaloader.Instaloader(
            dirname_pattern=str(self.output_dir / "{target}"),
            filename_pattern="{date_utc:%Y%m%d_%H%M%S}_{shortcode}",
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            post_metadata_txt_pattern="{caption}"
        )

    @staticmethod
    def extract_shortcode(url: str) -> Optional[str]:
        """Extract Instagram shortcode from URL."""
        patterns = [
            r"instagram\.com/(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)",
            r"instagram\.com/share/(?:reel|p)/([A-Za-z0-9_-]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def is_reel_or_tv(url: str) -> bool:
        """Check if URL is explicitly a Reel or TV video."""
        return bool(re.search(r"instagram\.com/(?:reel|reels|tv)/", url, re.IGNORECASE))

    def download_with_ytdlp(self, url: str) -> Dict[str, Any]:
        """
        Download using yt-dlp (best for Reels & single videos).
        """
        ydl_opts = {
            "outtmpl": str(self.output_dir / "%(upload_date>%Y%m%d)s_%(id)s.%(ext)s"),
            "format": "bestvideo+bestaudio/best",
            "quiet": False,
            "no_warnings": False,
        }

        if FFMPEG_PATH and os.path.exists(FFMPEG_PATH):
            ydl_opts["ffmpeg_location"] = FFMPEG_PATH

        if self.browser_cookies:
            ydl_opts["cookiesfrombrowser"] = (self.browser_cookies,)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return {
                "success": True,
                "title": info.get("title", "Instagram Video"),
                "file": filename,
                "engine": "yt-dlp",
            }

    def download_with_instaloader(self, shortcode: str) -> Dict[str, Any]:
        """
        Download using Instaloader (best for carousels, photo posts, captions).
        """
        post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
        target_dir_name = f"post_{shortcode}"
        self.loader.dirname_pattern = str(self.output_dir / target_dir_name)
        self.loader.download_post(post, target=target_dir_name)

        return {
            "success": True,
            "title": post.caption[:40] if post.caption else "Instagram Post",
            "is_video": post.is_video,
            "mediacount": post.mediacount,
            "engine": "instaloader",
            "directory": str(self.output_dir / target_dir_name),
        }

    def download(self, url: str) -> Dict[str, Any]:
        """
        Unified download method. Tries appropriate engine based on URL type,
        with automatic fallback.
        """
        cleaned_url = url.strip().split("?")[0].rstrip("/") + "/"
        shortcode = self.extract_shortcode(cleaned_url)

        if not shortcode:
            raise ValueError(f"Could not extract a valid Instagram shortcode from URL: {url}")

        is_video_hint = self.is_reel_or_tv(cleaned_url)

        # Strategy:
        # If it's a Reel/TV, try yt-dlp first. If it fails, fallback to instaloader.
        # If it's a Post (/p/), try instaloader first (handles carousels & photos). If it fails, fallback to yt-dlp.
        errors = []

        if is_video_hint:
            try:
                return self.download_with_ytdlp(cleaned_url)
            except Exception as e:
                errors.append(f"yt-dlp: {e}")
                try:
                    return self.download_with_instaloader(shortcode)
                except Exception as e2:
                    errors.append(f"instaloader: {e2}")
        else:
            try:
                return self.download_with_instaloader(shortcode)
            except Exception as e:
                errors.append(f"instaloader: {e}")
                try:
                    return self.download_with_ytdlp(cleaned_url)
                except Exception as e2:
                    errors.append(f"yt-dlp: {e2}")

        raise RuntimeError(f"Download failed with both engines:\n" + "\n".join(errors))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Free Instagram Reels and Posts Downloader")
    parser.add_argument("url", nargs="?", help="Instagram post/reel URL to download")
    parser.add_argument("--batch", "-b", help="Path to text file containing URLs")
    parser.add_argument("--output", "-o", default="insta_videos_downloads", help="Output directory")
    parser.add_argument("--cookies", "-c", help="Browser to import cookies from (e.g. chrome, edge, firefox)")
    args = parser.parse_args()

    downloader = InstagramDownloader(output_dir=args.output, browser_cookies=args.cookies)

    if args.url:
        target_url = args.url.strip()
    elif args.batch:
        batch_path = Path(args.batch)
        if batch_path.exists():
            with open(batch_path, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            for idx, u in enumerate(urls, 1):
                print(f"\n--- Downloading [{idx}/{len(urls)}]: {u} ---")
                try:
                    res = downloader.download(u)
                    print(f"[✓] Saved: {res.get('file') or res.get('directory')}")
                except Exception as err:
                    print(f"[✗] Failed: {err}")
            sys.exit(0)
        else:
            print(f"[!] File not found: {args.batch}")
            sys.exit(1)
    else:
        print("=" * 60)
        print("      📸 INSTAGRAM DOWNLOADER (Direct Mode)      ")
        print("=" * 60)
        target_url = input("Paste Instagram URL: ").strip()

    if target_url:
        print(f"\n[+] Processing: {target_url}")
        try:
            result = downloader.download(target_url)
            print("[✓] Download successful!")
            print(f"    - Engine: {result.get('engine')}")
            print(f"    - Location: {result.get('file') or result.get('directory')}")
        except Exception as e:
            print(f"[✗] Error: {e}")


