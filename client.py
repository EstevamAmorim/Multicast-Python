import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

while True:
    msg = input('Type the arithmetic expression: \n')
    sock.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))

    data, address = sock.recvfrom(128)
    print('Resposta: {fresp}, received from {fserver}'.format(fresp = data.decode(), fserver = address))