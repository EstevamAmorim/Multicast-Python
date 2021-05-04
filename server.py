import socket
import struct

NUMBER = 1
NUMBER_OF_SERVERS = 3
MCAST_GRP_CLIENT = '224.1.1.1'
MCAST_GRP_SEVERS = '224.1.1.2'

MCAST_PORT_CLIENT = 5007
MCAST_PORT_SERVERS_SEND = 5008
MCAST_PORT_SERVERS_RCV = 5009

MULTICAST_TTL_SERVERS = NUMBER_OF_SERVERS*2
MULTICAST_TTL_CLIENT = 2

ACTIVE = 1
NOT_CONFIRMED = 4
DISABLED = 5

MESSAGE = str(NUMBER)

SVRS_STATE = [DISABLED]*NUMBER_OF_SERVERS
SVRS_STATE[NUMBER] = ACTIVE

def servers_communication():
  while True:
    sock_servers_send.sendto(MESSAGE, (MCAST_GRP_SEVERS, MCAST_PORT_SERVERS))

    for i in range(NUMBER_OF_SERVERS:
      if SVRS_STATE[i] == ACTIVE or SVRS_STATE[i] < NOT_CONFIRMED:
        SVRS_STATE[i]+=1
      elif SVRS_STATE[i] == NOT_CONFIRMED:
        SVRS_STATE = DISABLED
      
    #pausa de tempo assincrona e constante

def servers_state():
  while True:
    data = sock_servers_rcv.recv(512) 
    n = int(data.decode())
    SVRS_STATE[n] = ACTIVE

def client_communication():
  flag = True
  while True:
    data, address = sock_client.recvfrom(512)
    exp = data.decode

    for i in range(NUMBER_OF_SERVERS)
      if i < NUMBER and SVRS_STATE[i] <= NOT_CONFIRMED
        flag = False

    if flag:
      try:
        result = eval(exp);
      except:
        result = 'Invalid Expression!'

      sock_servers.sendto(str.encode(result), address)

# --------------------------- SERVER-SERVER SOCKET SET UP - SEND -----------------------------------

sock_servers_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_servers_send.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL_SERVERS)

# --------------------------------------------------------------------------------------------------
# --------------------------- SERVER-SERVER SOCKET SET UP - RECEIVE --------------------------------

sock_servers_rcv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_servers_rcv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_servers_rcv.bind((MCAST_GRP, MCAST_PORT_SERVERS_RCV))

mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP_SEVERS), socket.INADDR_ANY)
sock_servers_rcv.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# --------------------------------------------------------------------------------------------------
# --------------------------- SERVER-CLIENT SOCKET SET UP - SEND AND RECEIVE -----------------------

sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL_CLIENT)
sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_client.bind((MCAST_GRP, MCAST_PORT_CLIENT))

mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP_CLIENT), socket.INADDR_ANY)
sock_client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# --------------------------------------------------------------------------------------------------
#-------------------------------------------MAIN----------------------------------------------------

# --------------------------------------------------------------------------------------------------
