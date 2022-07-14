import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

try:
    input = raw_input
except NameError:
    pass

while True:
    msg = input('\nType the arithmetic expression: \n')
    print('Requesting evaluation of expresion: {}'.format(msg))
    sock.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))

    data, address = sock.recvfrom(128)
    print('Answer: {fresp}, received from {fserver}'.format(fresp = data.decode(), fserver = address))