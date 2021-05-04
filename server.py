import socket

NUMBER = 1
NUMBER_OF_SERVERS = 3
MCAST_GRP_CLIENT = '224.1.1.1'
MCAST_GRP_SEVERS = '224.1.1.2'

MCAST_PORT_CLIENT = 5007
MCAST_PORT_SERVERS = 5008

MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((MCAST_GRP, MCAST_PORT_CLIENT))

mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  data, address = sock.recvfrom(1024)

  if(data.decode() == "Ok?")
    sock.sendto(str.encode("Server Ok - {}".format(NUMBER)), address)
