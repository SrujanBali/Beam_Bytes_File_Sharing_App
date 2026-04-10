import os
import pyqrcode
import socket
import webbrowser
from flask import Flask, render_template, send_from_directory
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

@app.route('/')
def index():
    files = [f for f in os.listdir(files_directory) if os.path.isfile(os.path.join(files_directory, f))]
    return render_template("index.html", files = files)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(files_directory, filename, as_attachment = True)

if __name__ == "__main__":
    ip_address = get_ip()
    link = f"http:{ip_address}:{PORT}"

    url = pyqrcode.create(link)
    url.svg("myqrcode.svg", scale=8)
    webbrowser.open('myqrcode.svg')

    print(f"Serving at :- {link}")
    app.run(host="0.0.0.0", port=PORT, debug=True)