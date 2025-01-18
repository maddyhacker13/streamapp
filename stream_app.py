# import necessary modules
import http.server
import socket
import socketserver
import webbrowser
import pyqrcode
import os

# Assign the appropriate port value
PORT = 8010

# Detect user's Desktop directory dynamically
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
os.chdir(desktop)

# Create an HTTP request handler
Handler = http.server.SimpleHTTPRequestHandler

# Get the hostname
hostname = socket.gethostname()

# Find the IP address of the PC
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
except Exception as e:
    print("Error retrieving IP address:", e)
    ip_address = "127.0.0.1"  # Fallback to localhost

link = f"http://{ip_address}:{PORT}"

# Generate a QR code for the IP address
try:
    url = pyqrcode.create(link)
    qr_file = r"D:\kALI\python\project\telegram bots\uploads\myqr.png"
    url.png(qr_file, scale=8)  # Save as PNG
    print(f"QR code saved as {qr_file}")
    webbrowser.open(qr_file)  # Open in the default browser
except Exception as e:
    print("Error generating QR code:", e)

# Create the HTTP request and serve the folder on PORT 8010
try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        print("Type this in your browser:", link)
        print("Or scan the QR code")
        httpd.serve_forever()
except Exception as e:
    print(f"Error starting server: {e}")
