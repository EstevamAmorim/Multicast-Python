import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

while True:
    MESSAGE = input('Type the arithmetic expression: \n')
    sock.sendto(MESSAGE.encode(), (MCAST_GRP, MCAST_PORT))
    print('Resposta: {} \n'.format(sock.recv(128).decode()))