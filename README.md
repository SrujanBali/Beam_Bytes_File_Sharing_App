# Beam Bytes - A File Sharing Application

Ever found yourself needing a quick and personalized tool to share files directly to your PC? This application solves that very problem by creating a seamless bridge between your devices.

---

### 🛠 Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python - 3.10+** | Main programming language for the project core |
| **Tkinter** | Desktop GUI tool for the application interface |
| **Ngrok** | Quick and secure tunneling to send/receive data over the web |
| **Flask** | Web framework to handle file transfers on the receiving device |
| **HTML/CSS/JS** | Frontend webpage to accompany the Flask server |

---
### Notice - Important ‼️
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

### Installation

First install PyInstaller

```bash
pip install pyinstaller
```

Run the following command to create the exe file

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "templates;templates" --name "BeamBytes" beam_bytes.py
```

You will find the exe file in the dist folder after Installation.
---

###  How It Works

1. **Launch the App** Run the application to initialize the interface.  
   <img width="500" alt="App Startup" src="https://github.com/user-attachments/assets/12c3190a-2db3-4cc6-bc7c-769e232e7af7" />

2. **Select Your Directory** Select the folder you want to share files from, or the destination where you want to receive files.  
   <img width="500" alt="Folder Selection" src="https://github.com/user-attachments/assets/8d58338a-cdfe-4cf0-970e-02e25f9740f8" />

3. **Start Sharing** Click **"Start Sharing"**. A QR Code and a unique URL will be generated. Simply scan the code or visit the link on any other device.  
   <img width="500" alt="Sharing Active" src="https://github.com/user-attachments/assets/4295b87e-0b3d-4eaa-bf0d-27a64edded82" />

4. **Transfer Files** Use the mobile-friendly web interface to download from or upload to your PC instantly.

   <p align="left">
     <img src="https://github.com/user-attachments/assets/1fc19b37-2eeb-4fd0-aa46-11f0c7e8cd11" width="30%" />
     <img src="https://github.com/user-attachments/assets/e4f6ecfe-f363-4817-bab7-87946c1289f6" width="30%" />
     <img src="https://github.com/user-attachments/assets/010c181b-aa2e-4ef8-80c6-c4fb6f9d7ff3" width="30%" />
   </p>
