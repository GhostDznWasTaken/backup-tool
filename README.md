# Minecraft World Backup to Google Drive

This is a Python script that automatically creates a timestamped `.zip` backup of a local Minecraft world folder and uploads it to a specific Google Drive folder. It also manages storage by keeping only the 3 most recent backups in Drive and deleting the oldest if necessary.

---

## 📦 What It Does

1. Reads configuration from `config.json`
2. Compresses the specified folder into a `.zip` file
3. Renames the `.zip` using a timestamped template
4. Moves the `.zip` to the output directory
5. Authenticates with Google Drive and uploads the backup
6. Deletes the oldest `.zip` file in the target Google Drive folder if there are more than 3

---

## 🧰 Requirements

- Python 3.x
- `PyDrive`
- A `client_secrets.json` file from Google Cloud Console
- First-time authentication via browser

Install dependencies:

```bash
pip install pydrive
```

---

## ⚙️ Configuration (`config.json`)

```json
{
  "world_path": "D:\\obs",
  "backup_path": "D:\\__WorldBackups",
  "template": "%hh%-%MM%-%ss%  %dd%.%mm%.%yyyy%"
}
```

- `world_path`: Path to the Minecraft world directory you want to back up
- `backup_path`: Where the `.zip` backup will be stored locally
- `template`: Timestamp format for the backup file name  
  You can use:
  - `%hh%`: Hour
  - `%MM%`: Minute
  - `%ss%`: Second
  - `%dd%`: Day
  - `%mm%`: Month
  - `%yyyy%`: Year

---

## 🔐 Google Drive Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable the **Google Drive API**
4. Go to **Credentials** → Create an **OAuth Client ID**
   - Choose `Desktop App`
5. Download the credentials file as `client_secrets.json`
6. Place `client_secrets.json` in the project folder
7. First run will open a browser window for authentication
8. Credentials will be saved in `mycreds.txt` to skip login next time

---

## 📁 Google Drive Folder Setup

The uploaded backups go into a specific Drive folder.  
You need to provide the **folder ID** in the code (inside `incarcare()` function):

```python
folder_id = "your-folder-id-here"
```

You can find the folder ID by opening it in your browser and copying the part after `/folders/` in the URL.

---

## 🚀 How to Run

```bash
python BACKUP_TOOL.py
```

Make sure `config.json`, `client_secrets.json`, and the script are in the same directory.

---

## 🧹 Auto-Cleanup

If there are more than 3 `.zip` files in the Drive folder, the script deletes the **oldest one** automatically to save space.

---

## 🔒 Notes

- `mycreds.txt` is used to cache your Drive access token. Do not share it.
- The script assumes the Google Drive folder is not shared or moved.

---

## 🛠 Optional Improvements

- CLI arguments for paths and template
- Email notification after upload
- Zip compression options
- Logging to file

---

## ✅ Example Result

A backup file might look like:

```
22-16-45  12.06.2025.zip
```

Uploaded to your Drive folder `Backup Mc`.

---

Made with ❤️ using Python and PyDrive.
