import socket
import struct

MCAST_GRP = '224.1.1.1'

MCAST_PORT = 5007

MULTICAST_TTL = 2

msg = 1


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((MCAST_GRP, MCAST_PORT))

mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


while True:
  exp, address = sock.recvfrom(512)
  try:
    result = eval(exp)
  except:
    result = 'Invalid Expression!'

  print(result)
  sock.sendto(str(result).encode(), address)
  
  
  