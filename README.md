# ⚡ ShadowNet

ShadowNet is a cybersecurity desktop application built with Python featuring a live Network Scanner and an encrypted Password Manager.

---

##  Preview

<!-- Record a short demo video and upload it to your GitHub repo, then replace the link below -->
>  Demo video coming soon 

---

##  Technologies Used

- **Python 3** — core language
- **Tkinter** — GUI framework
- **socket** — network communication for port scanning
- **threading** — background scanning so UI stays responsive
- **cryptography (Fernet)** — AES-128-CBC encryption for passwords
- **JSON** — local encrypted data storage

---

##  Features

- **Network Scanner** — scan any IP or hostname for open ports with live console output
-  **Password Manager** — master password protected vault with full encryption
-  **Copy to Clipboard** — copy any saved password with one click
- ⚡ **Real-time Results** — live output as ports are scanned
-  **Stop Anytime** — cancel a scan mid-way instantly
-  **Cyberpunk UI** — dark themed interface inspired by hacker aesthetics

---

## The Process

The app is split into two modules inside a single tabbed window.

**Network Scanner** uses Python's `socket` library to knock on each port in a given range using a TCP connection attempt. Each port is tested with `connect_ex()` which returns `0` if the port is open. The scan runs inside a background `thread` so the window never freezes, and a global flag lets the Stop button cancel the loop mid-scan instantly.

**Password Manager** uses `Fernet` symmetric encryption from the `cryptography` library. On first run, a random AES-128 key is generated and saved to `secret.key`. Every credential field — site, username and password — is individually encrypted before being written to `passwords.json`. Decryption only happens at runtime, meaning the file on disk is always fully encrypted and unreadable without the key.

---

## How to Run?

**1. Clone the repository**
```bash
git clone https://github.com/SP13xd/ShadowNet
cd ShadowNet
```

**2. Install the only external dependency**
```bash
pip install cryptography
```

**3. Run the app**
```bash
python netscan.py
```

> Requires Python 3. All other libraries (`tkinter`, `socket`, `threading`, `json`) are built into Python, so no extra installs needed.

---

## Project Structure

```
ShadowNet/
├── netscan.py              → main window + network scanner logic
├── password_manager.py  → password manager UI + encryption logic
├── passwords.json       → auto-created on first save (encrypted)
└── secret.key           → auto-created on first run (DO NOT DELETE)
```

---

## ⚠️ Disclaimer

Built for educational purposes as a college project. Only scan networks and systems you have explicit permission to test. Unauthorized port scanning may be illegal in your jurisdiction.
