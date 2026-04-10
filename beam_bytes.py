import os
import http.server
import pyqrcode
import socket
import socketserver
import webbrowser
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT")
base_path = os.getenv("BASE_PATH")
foldername = os.getenv("FOLDERNAME")

files_directory = os.path.join(base_path, foldername)
os.chdir(files_directory)

Handler = http.server.SimpleHTTPRequestHandler
hostname  = socket.gethostname()


#Using datagram transfer protocol for maximum speed
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.connect(("8.8.8.8", 80))
IP = f'http://{soc.getsockname()[0]}:{str(PORT)}'
link = IP

url = pyqrcode.create(link)
url.svg("myqr.svg", scale = 8)
webbrowser.open('myqr.svg')


with socketserver.TCPServer(("", int(PORT)), Handler) as httpd:
    print("Serving at Port", PORT)
    print("Type this in your browser :- ", IP)
    print("Or Use this QRcode")
    httpd.serve_forever()