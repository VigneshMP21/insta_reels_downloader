import os
import sys
import argparse
from pathlib import Path
from insta_downloader import InstagramDownloader


def print_banner():
    print("=" * 60)
    print("      📸 INSTAGRAM REELS & POSTS DOWNLOADER (FREE)      ")
    print("=" * 60)
    print("Supports: Reels, Videos, Photos, and Multi-slide Carousels")
    print("Output directory: ./insta_videos_downloads")
    print("=" * 60)


def download_single(downloader: InstagramDownloader, url: str):
    url = url.strip()
    if not url:
        return
    print(f"\n[+] Processing: {url}")
    try:
        result = downloader.download(url)
        print(f"[✓] Success!")
        print(f"    - Engine used: {result.get('engine')}")
        if "file" in result:
            print(f"    - Saved file: {result['file']}")
        if "directory" in result:
            print(f"    - Saved to folder: {result['directory']}")
            print(f"    - Items: {result.get('mediacount', 1)}")
    except Exception as e:
        print(f"[✗] Failed to download {url}")
        print(f"    Reason: {e}")


def download_batch(downloader: InstagramDownloader, filepath: str):
    path = Path(filepath)
    if not path.exists():
        print(f"[!] File not found: {filepath}")
        return

    with open(path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not urls:
        print("[!] No URLs found in the file.")
        return

    print(f"\n[+] Found {len(urls)} URLs to download in '{filepath}'...")
    for idx, url in enumerate(urls, start=1):
        print(f"\n--- Item {idx}/{len(urls)} ---")
        download_single(downloader, url)

    print("\n[✓] Batch download completed!")


def open_downloads_folder():
    downloads_path = Path("insta_videos_downloads").resolve()
    downloads_path.mkdir(parents=True, exist_ok=True)
    if sys.platform == "win32":
        os.startfile(str(downloads_path))
    elif sys.platform == "darwin":
        os.system(f'open "{downloads_path}"')
    else:
        os.system(f'xdg-open "{downloads_path}"')
    print(f"[+] Opened folder: {downloads_path}")


def interactive_menu(downloader: InstagramDownloader):
    while True:
        print_banner()
        print("1. Download single Reel / Post URL")
        print("2. Batch download from 'insta_urls.txt'")
        print("3. Open Insta Downloads Folder")
        print("4. Exit")
        print("-" * 60)
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            url = input("\nPaste Instagram URL: ").strip()
            if url:
                download_single(downloader, url)
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            file_name = input("Enter file path (default: insta_urls.txt): ").strip() or "insta_urls.txt"
            download_batch(downloader, file_name)
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            open_downloads_folder()
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            print("\nExiting. Happy downloading!")
            break
        else:
            print("[!] Invalid choice. Please enter 1, 2, 3, or 4.")


def main():
    parser = argparse.ArgumentParser(description="Free Instagram Reels and Posts Downloader")
    parser.add_argument("url", nargs="?", help="Instagram post/reel URL to download")
    parser.add_argument("--batch", "-b", help="Path to text file containing URLs (e.g. insta_urls.txt)")
    parser.add_argument("--output", "-o", default="insta_videos_downloads", help="Output directory (default: insta_videos_downloads)")
    parser.add_argument(
        "--cookies", "-c",
        help="Browser to import cookies from (e.g. chrome, edge, firefox) for restricted/login-walled posts"
    )

    args = parser.parse_args()
    downloader = InstagramDownloader(output_dir=args.output, browser_cookies=args.cookies)

    if args.url:
        download_single(downloader, args.url)
    elif args.batch:
        download_batch(downloader, args.batch)
    else:
        interactive_menu(downloader)


if __name__ == "__main__":
    main()

