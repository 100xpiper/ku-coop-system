import urllib.request
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind(('0.0.0.0', 8085))
    s.listen(1)
    print("Binding to 0.0.0.0:8085 SUCCESS! Python can bind to 0.0.0.0 without admin.")
    s.close()
except Exception as e:
    print("Socket error:", e)

