import os
import sys
import subprocess
import pyqrcode
import signal
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import socket
from werkzeug.serving import make_server
import tkinter
from tkinter import Tk, filedialog, messagebox
import threading
from pyngrok import ngrok
from PIL import Image, ImageTk
from dotenv import load_dotenv

if sys.stdout is None:
    log_file = open("beam_bytes_error.log", "w", buffering=1)
    sys.stdout = log_file
    sys.stderr = log_file

if sys.platform == "win32":
    _old_init = subprocess.Popen.__init__
    def _new_init(self, *args, **kwargs):
        if "creationflags" not in kwargs:
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        _old_init(self, *args, **kwargs)
    subprocess.Popen.__init__ = _new_init

PORT = os.getenv("PORT") or 8010

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path  = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

load_dotenv()
template_dir = get_resource_path('templates')
app = Flask(__name__, template_folder=template_dir)

server_instance = None

class Beam_Bytes_State:
    def __init__(self):
        self.shared_folder = ""
        self.public_url = ""

state = Beam_Bytes_State()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

@app.route('/')
def index():
    if not state.shared_folder:
        return ("No folder selected on hosting device", 403)
    files = os.listdir(state.shared_folder)
    return  render_template('index.html', files=files)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(state.shared_folder, filename, as_attachment = True)

@app.route('/upload', methods=["POST"])
def upload_file():
    if 'file[]'not in request.files and 'file' not in request.files:
        return "No File Part", 400
    
    uploaded_files = request.files.getlist('file[]')

    for file in uploaded_files:
        if file.filename == "":
            continue
        
        if file:
            file_path = os.path.join(state.shared_folder, file.filename)
            file.save(file_path)
            print("File Saved")

    return redirect(url_for('index'))

def run_flask():
    global server_instance
    print(f"Starting Flask Server on port {PORT}")
    try:

        server_instance = make_server('0.0.0.0', int(PORT), app)
        server_instance.serve_forever()
    except Exception as e:
        print(f" * Flask server error: {e}")
    print(" * Flask server background thread stopped.")

def stop_flask():
    global server_instance
    if server_instance:
        print(" * Shutting down Flask server instance...")
        server_instance.shutdown()
        server_instance = None
        print(" * Flask server successfully ended.")

def on_closing():
    print("Shutting Down the Service...")
    try:
        ngrok.disconnect(state.public_url)
        ngrok.kill()
    except:
        pass
        
    os.kill(os.getpid(), signal.SIGINT)
    root.destroy()
    os._exit(0)


class Beam_Bytes_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Beam Bytes")
        self.root.geometry("600x700")
        self.root.config(bg="black")
        try:
            self.root.iconbitmap(get_resource_path("beambytes.ico"))
        except Exception as e:
            print(f"Error file applying icon : {e}")

        self.setup_frame = tkinter.Frame(root, padx=20, pady=20, bg="#121212")
        self.setup_frame.pack(expand=True, fill="both")

        tkinter.Label(self.setup_frame, text="Beam Bytes - Setup", font=("Arial", 22, "bold"), bg="#121212", fg="#f8fafc").pack(pady=(5, 50))
        tkinter.Label(self.setup_frame, text="Select the folder you want to share", font=("Arial", 16), bg="#121212", fg="#f8fafc").pack(pady=(0, 10))

        self.path_label = tkinter.Label(self.setup_frame, text="No folder selected", font=("Arial", 12), bg="#121212", fg="#f8fafc")
        self.path_label.pack(pady=(0, 20))

        tkinter.Button(self.setup_frame, text="Browse Folder", font=("Arial", 12, "bold") , command=self.browse, width=30, height=2, bg="#578fe4", fg="black", borderwidth=4).pack(pady=(0, 15))

        self.hosting_frame = tkinter.Frame(self.setup_frame, bg="#121212")
        self.hosting_frame.pack(pady=40)

        tkinter.Label(self.hosting_frame, text="Select Hosting Mode: ", bg="#121212", font=("Helvetica", 12), fg="#f8fafc").pack(padx=10, side=tkinter.LEFT)
        self.mode_var = tkinter.StringVar(value="Local Wifi")
        self.mode_dropdown = tkinter.OptionMenu(
            self.hosting_frame,
            self.mode_var,
            "Local Wifi",
            "Global (Ngrok)"
        )
        self.mode_dropdown.config(width=25 , bg="orange", fg="black", font=("Arial", 12, "bold"))
        self.mode_dropdown.pack(padx=10, side=tkinter.LEFT)

        self.start_button = tkinter.Button(self.setup_frame, text="Start Sharing", font=("Helvetica", 18, "bold"), state="disabled", bg="#2a2a2a", command=self.start_service, width=50, height=2)
        self.start_button.pack(pady=10)


    def browse(self):
        folder = filedialog.askdirectory()
        if folder:
            state.shared_folder = folder
            self.path_label.config(text=folder, fg="#f8fafc")
            self.start_button.config(state="normal", bg="green")

    def start_service(self):
        selected_mode = self.mode_var.get()
        self.setup_frame.pack_forget()
        self.root.title("Beam Bytes - Live")

        threading.Thread(target=run_flask, daemon=True).start()

        if selected_mode == "Local Wifi":
            local_ip = get_local_ip()
            local_url = f"http://{local_ip}:{PORT}"
            self.show_qr(local_url, title="Scan for Fast Local Wifi Transfer")
        else: 
            try:
                state.public_url = ngrok.connect(PORT).public_url
                print(f' * Public URL :- {state.public_url}')
                self.show_qr(state.public_url, title="Scan for Global Ngrok Transfer")
            except Exception as e:
                messagebox.showerror("Ngrok Error : ", f"Failed to start tunnel: {e}")
                self.root.destroy()

    def end_service(self):
        selected_mode = self.mode_var.get()

        stop_flask()
        state.shared_folder = ""
        self.path_label.config(text="No folder selected")
        self.start_button.config(state="disabled", bg="#2a2a2a")

        if "Global (Ngrok)" in selected_mode:
            try:
                ngrok.disconnect(state.public_url)
                ngrok.kill()
                print("Ngrok ended")
            except Exception as e:
                print(f"Error killing ngrok : {e}")

        self.qr_frame.pack_forget()
        self.setup_frame.pack(expand=True, fill="both")
        self.root.title("Beam Bytes - Setup")

    def show_qr(self, url, title="Scan to Access Files"):
        self.qr_frame = tkinter.Frame(self.root, padx=10, pady=5, bg="lightgreen")
        self.qr_frame.pack(expand=True, fill="both")
        tkinter.Label(self.qr_frame, text="Scan to Access Files", font=("Arial", 18, "bold"), bg="lightgreen").pack(pady=10)

        qr = pyqrcode.create(url)
        qr.png("myqrcode.png", scale=12)
        pil_img = Image.open("myqrcode.png")
        pil_img = pil_img.resize((500, 500), Image.Resampling.NEAREST)

        self.qr_image = ImageTk.PhotoImage(pil_img)
        qr_label = tkinter.Label(self.qr_frame, image = self.qr_image, bg="black")
        qr_label.image = self.qr_image
        qr_label.pack(pady=(0,20))
        tkinter.Label(self.qr_frame, text = f'Serving at :- {url}', font=("Helvetica", 15, "bold"), fg="white", bg="black").pack(pady=(0, 20), fill="x")
        self.end_button = tkinter.Button(self.qr_frame, text="End Service", font=("Helvetica", 12, "bold") , bg="red", width=20, height=2 , command=self.end_service)
        self.end_button.pack(pady=1)


        

if __name__ == "__main__":
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app_gui = Beam_Bytes_GUI(root)
    root.mainloop()