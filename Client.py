import socket
import struct
import time
import msvcrt

TeamName="RIPGoalDiago"
BufferSize=1024
MyPort=2047

def tcp_connection(ip, Port):
    TCPSock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        TCPSock.connect((ip, Port))
    except:
        print("connection faild")
    return TCPSock

#UDP
def initUDPclient():
    client= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(("", 13117))
    return client

#TCP

def Main():
    client = initUDPclient()
    while True:
        mess , add = client.recvfrom(1024)
        ip, port = add
        MagicNumber , MessageType , Port = struct.unpack('IBH', mess)

        if(MagicNumber == 0xfeedbeef and MessageType == 0x2):
            TCPSock = tcp_connection(ip, Port)
            try:
                TCPSock.sendall(TeamName.encode())

                try:
                    startmss= TCPSock.recv(BufferSize)
                except:
                    print("reciving name faild")

                print(startmss)
                timer = time.time() + 10
                while time.time()<timer:
                    char=msvcrt.getch() # change to ubuntu version
                    try:
                        TCPSock.sendall(char)
                    except:
                        print("sending characters faild")
            except:
                print("sending name faild")
            finally:
                TCPSock.close()

def test():
    while True:
        client = initUDPclient()
        mess, add = client.recvfrom(BufferSize)
        ip, port = add
        MagicNumber, MessageType, Port = struct.unpack('IBH', mess)
        if (MagicNumber == 0xfeedbeef and MessageType == 0x2):
            TCPSock = tcp_connection(ip, Port)
            print("start listining:")
            TCPSock.sendall(TeamName.encode())
            startMsg=TCPSock.recv(BufferSize)
            print(startMsg.decode())
            timer=time.time()+5
            while time.time() < timer:
                char = msvcrt.getch()  # change to ubuntu version
                try:
                    TCPSock.send(char)
                except:
                    print("sending characters faild")
            print("recive all the Character, please W8 for the resultd:")





if __name__ == '__main__':
    test()
