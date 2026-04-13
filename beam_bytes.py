import os
import pyqrcode
import socket
import signal
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import tkinter
from tkinter import Label, Tk
import threading
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

PORT = os.getenv("PORT")
base_path = os.getenv("BASE_PATH")
foldername = os.getenv("FOLDERNAME")
files_directory = os.path.join(base_path, foldername)

def get_ip():
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect(("8.8.8.8", 80))
    ip = soc.getsockname()[0]
    soc.close()
    return ip

def on_closing():
    print("Shutting Down the Service...")
    try:
        ngrok.disconnect(public_url)
        ngrok.kill()
    except:
        pass
        
    os.kill(os.getpid(), signal.SIGINT)
    root.destroy()
    os._exit(0)

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
    

if __name__ == "__main__":
    public_url = ngrok.connect(PORT).public_url
    print(f' * Public URL :- {public_url}')

    url = pyqrcode.create(public_url)
    url.png("myqrcode.png", scale=12)
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    root = Tk()
    root.title("QR Code for Beam Bytes")
    root.configure(bg="black")
    qr_image = tkinter.PhotoImage(file="myqrcode.png")
    width, height = qr_image.width(), qr_image.height()
    root.geometry(f'{width}x{height + 60}')
    image_label = Label(root, image=qr_image)
    image_label.pack(pady=(0, 20))
    tkinter.Label(root, text = f'Serving at :- {public_url}', font=("Helvetica", 15, "bold"), fg="white", bg="black").pack()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()