import os
import pyqrcode
import signal
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import tkinter
from tkinter import Tk, filedialog, messagebox
import threading
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

PORT = os.getenv("PORT")
base_path = os.getenv("BASE_PATH")
foldername = os.getenv("FOLDERNAME")
files_directory = os.path.join(base_path, foldername)

class Beam_Bytes_State:
    def __init__(self):
        self.shared_folder = ""
        self.public_url = ""

state = Beam_Bytes_State()


@app.route('/')
def index():
    files = [f for f in os.listdir(files_directory) if os.path.isfile(os.path.join(files_directory, f))]
    return render_template("index.html", files = files)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(files_directory, filename, as_attachment = True)

@app.route('/upload', methods=["POST"])
def upload_file():
    if 'file'not in request.files:
        return "No File Part", 400
    
    file = request.files["file"]

    if file.filename == "":
        return "No file selected", 400
    
    if file:
        file_path = os.path.join(files_directory, file.filename)
        file.save(file_path)
        print("File Saved")
        return redirect(url_for('index'))


def run_flask():
    app.run(host="127.0.0.1", port=int(PORT), debug=False, use_reloader = False)

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

        self.setup_frame = tkinter.Frame(root, padx=20, pady=20)
        self.setup_frame.pack(expand=True, fill="both")

        tkinter.Label(self.setup_frame, text="Beam Bytes - Setup", font=("Arial", 18, "bold")).pack(pady=10)
        tkinter.Label(self.setup_frame, text="Select the folder you want to share").pack()

        self.path_label = tkinter.Label(self.setup_frame, text="No folder selected")
        self.path_label.pack(pady=10)

        tkinter.Button(self.setup_frame, text="Browse Folder", command=self.browse).pack(pady=5)
        self.start_button = tkinter.Button(self.setup_frame, text="Start Sharing", font=("Helvetica", 15, "bold"), state="disabled", bg="orange", command=self.start_service, width=50, height=2)
        self.start_button.pack(pady=10)

    def browse(self):
        folder = filedialog.askdirectory()
        if folder:
            state.shared_folder = folder
            self.path_label.config(text=folder, fg="black")
            self.start_button.config(state="normal", bg="green")

    def start_service(self):
        self.setup_frame.pack_forget()
        self.root.title("Beam Bytes - Live")

        threading.Thread(target=run_flask, daemon=True).start()

        try:
            state.public_url = ngrok.connect(PORT).public_url
            print(f' * Public URL :- {state.public_url}')
            self.show_qr(state.public_url)
        except Exception as e:
            messagebox.showerror("Ngrok Error : ", f"Failed to start tunnel: {e}")
            self.root.destroy()

    def show_qr(self, url):
        qr_frame = tkinter.Frame(self.root, padx=10, pady=10)
        qr_frame.pack(expand=True, fill="both")
        tkinter.Label(qr_frame, text="Scan to Acess Files", font=("Arial", 18, "bold")).pack(pady=10)

        qr = pyqrcode.create(url)
        qr.png("myqrcode.png", scale=12)
        qr_image = tkinter.PhotoImage(file="myqrcode.png")
        qr_label = tkinter.Label(qr_frame, image = qr_image)
        qr_label.image = qr_image
        qr_label.pack(pady=(0,20))

        tkinter.Label(self.root, text = f'Serving at :- {url}', font=("Helvetica", 15, "bold"), fg="white", bg="black").pack()

        

if __name__ == "__main__":
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app_gui = Beam_Bytes_GUI(root)
    root.mainloop()