# Beam Bytes - A File Sharing Application

Ever found yourself needing a quick and personalized tool to share files directly from and to your PC? This application solves that very problem by creating a seamless bridge between your devices.
---
<img width="480" height="1040" alt="git_project" src="https://github.com/user-attachments/assets/5d35badc-d117-461d-8918-2046619dfc57" />


---
## Features
- **Modern Tkinter GUI** for easy folder selection and state management.
- **Dual Hosting Mode** that lets users share files globally using Ngrok servers by simply sharing the QR code or share files locally (10-100x faster than Ngrok).
- **Dynamic QR Code Generation** for global and local hosting.

---

## Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python - 3.10+** | Main programming language for the project core |
| **Tkinter** | Desktop GUI tool for the application interface |
| **Ngrok** | Quick and secure tunneling to send/receive data over the web |
| **Flask** | Web framework to handle file transfers on the receiving device |
| **HTML/CSS/JS** | Frontend webpage to accompany the Flask server |

---
## Notice - Important ‼️
- You will need to first add your own Ngrok Auth Token after signing up with Ngrok to run the tunneling
- Use the following command to add your auth token after installing the dependencies from requirements.txt
```bash
ngrok config add-authtoken <YOUR AUTHTOKEN>
```
---
### Run Locally

Clone the project

```bash
  git clone https://github.com/SrujanBali/Beam_Bytes_File_Sharing_App
```

Go to the project directory

```bash
  cd Beam_Bytes_File_Sharing_App
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the program

```bash
  python beam_bytes.py
```
---

## Installation

First install PyInstaller

```bash
pip install pyinstaller
```

Run the following command to create the exe file

```bash
pyinstaller BeamBytes.spec
```

You will find the exe file in the dist folder after Installation.
---

##  How It Works

1. **Launch the App** Run the application to initialize the interface.  
   <img width="606" height="733" alt="Screenshot 2026-10-26 184924" src="https://github.com/user-attachments/assets/e034fe30-3db7-4c21-94f1-f020b216f8ae" />

2. **Select Your Directory** Select the folder you want to share files from, or the destination where you want to receive files.  
   <img width="603" height="732" alt="Screenshot 2026-10-26 185005" src="https://github.com/user-attachments/assets/1e299728-5fa9-4fad-a8f0-0304d7b97d68" />

3. **Select Hosting Mode** Select the hosting mode. Beam Bytes features Local (localhost) and Global (Ngrok) hosting.
   <img width="608" height="729" alt="Screenshot 2026-10-26 185029" src="https://github.com/user-attachments/assets/f60690fe-8162-4168-9b1d-4a5642faba2f" />

4. **Start Sharing** Click **"Start Sharing"**. A QR Code and a unique URL will be generated. Simply scan the code or visit the link on any other device.  
   <img width="608" height="735" alt="Screenshot 2026-10-26 185109" src="https://github.com/user-attachments/assets/f890ecb8-d67e-4122-875d-466fe501652c" />

5. **Transfer Files** Use the mobile-friendly web interface to download from or upload to your PC instantly.

   <p align="left">
     <img src="https://github.com/user-attachments/assets/1fc19b37-2eeb-4fd0-aa46-11f0c7e8cd11" width="30%" />
     <img src="https://github.com/user-attachments/assets/e4f6ecfe-f363-4817-bab7-87946c1289f6" width="30%" />
     <img src="https://github.com/user-attachments/assets/010c181b-aa2e-4ef8-80c6-c4fb6f9d7ff3" width="30%" />
   </p>
