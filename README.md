# 📸 Instagram Reels & Posts Downloader (100% Free)

A simple, free, and lightweight tool to download Instagram **Reels**, **Videos**, **Photos**, and **Multi-slide Carousel Albums** directly to your computer using their links.

> **Zero Cost:** No subscriptions, no paid APIs (like RapidAPI), and no login credentials required for public posts.

---

## 🚀 Quick Start Guide (For First-Time Users)

If you have received this folder for the first time, follow these **3 simple steps**:

### Step 1: Ensure Python is Installed
1. If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).
2. ⚠️ **VERY IMPORTANT:** During installation, check the box that says:
   `☑ Add Python to PATH` (at the bottom of the installer window).

---

### Step 2: Install Required Packages (One-Time Setup)
You only need to do this **once** on a new computer:

- **Method A (Easiest - 1 Click):**  
  Double-click the file named:
  ```
  install_dependencies.bat
  ```
  *(A black window will open, install the needed free libraries, and say "Dependencies installed successfully!").*

- **Method B (Via Command Prompt):**  
  Open terminal in this folder and run:
  ```bash
  pip install -r requirements.txt
  ```

---

### Step 3: Run the Program
Whenever you want to download videos or photos:

- **Simply double-click:**
  ```
  run_insta_downloader.bat
  ```
  *(The downloader menu will immediately open on your screen!)*

---

## 📖 How to Use the Menu

When you double-click `run_insta_downloader.bat`, you will see this menu:

```text
============================================================
      📸 INSTAGRAM REELS & POSTS DOWNLOADER (FREE)      
============================================================
Supports: Reels, Videos, Photos, and Multi-slide Carousels
Output directory: ./insta_videos_downloads
============================================================
1. Download single Reel / Post URL
2. Batch download from 'insta_urls.txt'
3. Open Insta Downloads Folder
4. Exit
------------------------------------------------------------
Enter your choice (1-4):
```

### Option 1: Download a Single Link
1. Type `1` and press `Enter`.
2. Go to Instagram on your browser or phone, copy the link of any Reel or Post:
   - Example: `https://www.instagram.com/reel/Cxxxxxxxxx/`
   - Example: `https://www.instagram.com/p/Cxxxxxxxxx/`
3. Right-click in the terminal to paste the URL and press `Enter`.
4. The video/photos will be downloaded and saved automatically!

---

### Option 2: Batch Download Multiple Links at Once
1. Open the file named `insta_urls.txt` in Notepad.
2. Paste all your Instagram links, **one link per line**, for example:
   ```text
   https://www.instagram.com/reel/DAA111xxxx/
   https://www.instagram.com/p/DBB222xxxx/
   https://www.instagram.com/reel/DCC333xxxx/
   ```
3. Save and close `insta_urls.txt`.
4. In the downloader menu, type `2` and press `Enter`.
5. All links will be downloaded one by one automatically.

---

### Option 3: Open the Downloads Folder
- Type `3` and press `Enter`.
- Your Windows File Explorer will instantly open the `insta_videos_downloads` folder containing all your downloaded media files.

---

### Option 4: Exit
- Type `4` and press `Enter` to close the program.

---

## 📁 Where Are My Downloaded Files Saved?

All downloaded videos, photos, and carousels are saved directly inside:
```
📁 insta_videos_downloads/
```
- **Reels & Videos:** Saved as high-quality `.mp4` video files with full synchronized audio.
- **Carousels & Albums:** Saved inside their own subfolder with all images and video slides intact.

---

## 🛠️ Advanced Usage (Optional)

If you prefer using PowerShell or Command Prompt directly:

- **Run menu via terminal:**
  ```powershell
  python insta_video_downloader.py
  ```
- **Quick download single URL via command line:**
  ```powershell
  python insta_video_downloader.py "https://www.instagram.com/reel/YOUR_REEL_CODE/"
  ```
- **Batch download from custom text file:**
  ```powershell
  python insta_video_downloader.py --batch insta_urls.txt
  ```
- **If Instagram asks for login (Private or restricted posts):**  
  Pass your browser name to automatically use your existing login session cookies:
  ```powershell
  python insta_video_downloader.py "https://www.instagram.com/reel/YOUR_REEL_CODE/" --cookies chrome
  ```
  *(Supported browsers: `chrome`, `edge`, `firefox`, `opera`)*

---

## ❓ Frequently Asked Questions (FAQ)

### 1. The window closes immediately when I double-click `run_insta_downloader.bat`.
- Ensure Python is installed and added to PATH.
- Run `install_dependencies.bat` first so all required packages are present.

### 2. Can I share this folder with friends or colleagues?
- **Yes!** You can send them this entire folder (e.g. as a `.zip` file).
- They only need to follow the **Quick Start Guide** above:
  1. Have Python installed.
  2. Double-click `install_dependencies.bat`.
  3. Double-click `run_insta_downloader.bat`.

### 3. Is it completely free?
- **Yes, 100% free forever.** It relies on trusted open-source libraries (`yt-dlp` and `instaloader`) without any subscriptions or credit card requirements.
