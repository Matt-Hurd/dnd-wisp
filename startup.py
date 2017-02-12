import socket

UDP_IP = "10.138.144.76"
UDP_PORT = 5005
MESSAGE = b"WHISPER"

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))