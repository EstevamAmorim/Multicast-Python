import socket
import struct
import time
import sys
import threading

NUMBER = int(sys.argv[1])
MAX_NUMBER_OF_SERVERS = 5

MCAST_GRP_CLIENT = '224.1.1.1'
MCAST_GRP_SEVERS = '224.1.1.2'

MCAST_PORT_CLIENT = 5007
MCAST_PORT_SERVERS = 5008

MULTICAST_TTL_SERVERS = MAX_NUMBER_OF_SERVERS*2
MULTICAST_TTL_CLIENT = 2

ACTIVE = 4
NOT_CONFIRMED = 2
DISCONNECTED = 0

MESSAGE = str(NUMBER)
SVRS_STATE = [DISCONNECTED]*MAX_NUMBER_OF_SERVERS

srvs_state_lock = threading.Lock()

def servers_communication():
  print('Started communicating state to other servers.')
  while True:
    global SVRS_STATE

    sock_servers_send.sendto(MESSAGE.encode(), (MCAST_GRP_SEVERS, MCAST_PORT_SERVERS))

    with srvs_state_lock:
      for i in range(MAX_NUMBER_OF_SERVERS):
        if SVRS_STATE[i] > DISCONNECTED:
            SVRS_STATE[i]-=1
            if SVRS_STATE[i] < NOT_CONFIRMED:
              if (SVRS_STATE[i] == DISCONNECTED):
                print('Server {} is Disconnected'.format(i))
              else:
                print('Server {} is Unresponsive'.format(i))

    time.sleep(1)

def servers_state():
  print('Started listening to other servers.')
  while True:
    data = sock_servers_rcv.recv(512) 
    n = int(data.decode())
    with srvs_state_lock:
      if (SVRS_STATE[n] < NOT_CONFIRMED):
        print('Server {} is Active'.format(n))
      SVRS_STATE[n] = ACTIVE
      

def client_communication():
  while True:
    exp, address = sock_client.recvfrom(512)

    shouldRespond = True
    
    with srvs_state_lock:
      for i in range(NUMBER):
        if SVRS_STATE[i] >= NOT_CONFIRMED:
          print('Client message received, expecting server {} will answer.'.format(i))
          shouldRespond = False
          break

    if shouldRespond:
      print('Client message received, evaluating expression {}'.format(exp))
      try:
        result = eval(exp)
      except:
        result = 'Invalid Expression!'

      print('Sending result: {}'.format(result))
      sock_client.sendto(str(result).encode(), address)

# --------------------------- SERVER-SERVER SOCKET SET UP - SEND -----------------------------------

sock_servers_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_servers_send.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL_SERVERS)

# --------------------------------------------------------------------------------------------------
# --------------------------- SERVER-SERVER SOCKET SET UP - RECEIVE --------------------------------

sock_servers_rcv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_servers_rcv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_servers_rcv.bind((MCAST_GRP_SEVERS, MCAST_PORT_SERVERS))

mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP_SEVERS), socket.INADDR_ANY)
sock_servers_rcv.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# --------------------------------------------------------------------------------------------------
# --------------------------- SERVER-CLIENT SOCKET SET UP - SEND AND RECEIVE -----------------------

sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL_CLIENT)
sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_client.bind((MCAST_GRP_CLIENT, MCAST_PORT_CLIENT))

mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP_CLIENT), socket.INADDR_ANY)
sock_client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# --------------------------------------------------------------------------------------------------
#-------------------------------------------MAIN----------------------------------------------------
# --------------------------------------------------------------------------------------------------

threadServerSend = threading.Thread(target=servers_communication)
threadServerSend.start()

threadServerRcv = threading.Thread(target=servers_state)
threadServerRcv.start()

threadClientRcv = threading.Thread(target=client_communication)
threadClientRcv.start()