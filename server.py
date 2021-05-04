import socket

def servers_communication():
  while True
    sock.sendto(MESSAGE, (MCAST_GRP_SEVERS, MCAST_PORT_SERVERS))


def servers_state():
  
def client_communication():

NUMBER = 1
NUMBER_OF_SERVERS = 3
MCAST_GRP_CLIENT = '224.1.1.1'
MCAST_GRP_SEVERS = '224.1.1.2'

MCAST_PORT_CLIENT = 5007
MCAST_PORT_SERVERS = 5008

MULTICAST_TTL_SERVERS = NUMBER_OF_SERVERS*2
MULTICAST_TTL_CLIENT = NUMBER_OF_SERVERS*2

MESSAGE = 'Im active!'

sock_servers = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

sock_servers.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL_SERVERS)
sock_client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL_CLIENT)

sock_servers.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_servers.bind((MCAST_GRP, MCAST_PORT_SERVERS))
sock_client.bind((MCAST_GRP, MCAST_PORT_CLIENT))

mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP_SEVERS), socket.INADDR_ANY)
sock_servers.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP_CLIENT), socket.INADDR_ANY)
sock_client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  data, address = sock_servers.recvfrom(1024)

  if(data.decode() == "Ok?")
    sock_servers.sendto(str.encode("Server Ok - {}".format(NUMBER)), address)
