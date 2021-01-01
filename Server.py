import threading
import socket
import struct
import time
import threading
import random
from concurrent.futures import ThreadPoolExecutor

BufferSize=1024
MyPort=2047
Team1=[]
Team2=[]
ToartalCount1=0
ToartalCount2=0
LocalIP="255.255.255.255"

def run(conn):
    try:
        #get the name in  one bytes
        lName =''
        count=0
        global ToartalCount1,ToartalCount2
        timer=time.time()+5
        while True and time.time()<timer:
            ch=conn.recv(1)
            ch=ch.decode()
            if ch=='\n':
                break
            lName.__add__(ch)
        print(lName)



        #append client to team
        rand=random.randint(0,1)
        if rand==0:
            Team1.append(lName)
        else:
            Team2.append(lName)
        conn.sendall("plese enter whatever you want, you have 10 sec\n")
        timer = time.time() + 10
        while time.time() < timer:
            ch=conn.recv(1)
            count=count+1
        #add the points to the specific team
        if rand==0:
            ToartalCount1=ToartalCount1+count
        else:
            ToartalCount2=ToartalCount2+count
    except:
        print("the client disconnect")



#init UDP connection
def initUDPconn():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    mreq = struct.pack("IBH", 0xfeedbeef, 0x2, MyPort)
    return sock,mreq

#init TCP connection
def initTcpConn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), MyPort))
    return s

def Main():
    global ToartalCount1, ToartalCount2
    s = initTcpConn()
    sock, mreq = initUDPconn()
    s.listen(1)
    executor = ThreadPoolExecutor()
    while True:

        timer = time.time()+10
        while time.time() < timer:
            sock.sendto(mreq, (LocalIP, 13117))
            time.sleep(1)
            s.settimeout(0)
            try:
                conn, add = s.accept()
                #THREADING
                executor.submit(run(conn))
                #th= threading.Thread(target=run, args=(conn,))
                #th.start()

                if(ToartalCount1>ToartalCount2):
                    print("team 1 win the game:\n")
                    for i in Team1:
                        print(i+'\n')
                    print("team1 earned "+ ToartalCount1+'\n')
                    print("team2 earned "+ ToartalCount2+'\n')
                else:
                    print("team 2 win the game:\n")
                    for i in Team2:
                        print(i + '\n')
                    print("team2 earned " + ToartalCount2 + '\n')
                    print("team1 earned " + ToartalCount1 + '\n')




            except:
                pass

def tests():
    """#s = initTcpConn()
    sock, mreq = initUDPconn()
    sock.bind(("", 2047))
    print("UDP server up and listening")
    bytesAddressPair = sock.recvfrom(1024)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print(message)
    print(address)

    sock.sendto(mreq, ("255.255.255.255", 13117))"""

    global ToartalCount1, ToartalCount2
    s = initTcpConn()
    sock, mreq = initUDPconn()
    s.listen(1)
    while True:
        timer = time.time() + 10
        while time.time() < timer:
            sock.sendto(mreq, (LocalIP, 13117))
            time.sleep(1)
            s.settimeout(0)
            try:
                conn, add = s.accept()
            except:
                print("accepting connection faild")
            conn.setblocking(1)
            data=conn.recv(BufferSize)
            print("hii " + data.decode() + " welcome to the game")
            try:
                conn.sendall("Please Enter what ever you want you have 10 sec".encode())
            except:
                print("sending starting mss faild")
            timer = time.time() + 10
            while time.time() < timer:
                ch = conn.recv(1)
                count = count + 1
            print(count)



if __name__ == '__main__':
    tests()