import socket
import argparse

if __name__ == '__main__':

    socket_num = 2
    IP_list = []
    connec = []

    parser = argparse.ArgumentParser(description='manul to this script')
    parser.add_argument('--port',type=int, default=8080)

    args = parser.parse_args()
    print ("Parsing port....")
    print ("Port: ",args.port)

    port = args.port
    host = ''

    while True:
        gamers = []
        IP_list = []
        connec = []
        ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        ssocket.bind((host,port))
        ssocket.listen(socket_num)

        for x in range(socket_num):
            connect,addr = ssocket.accept()
            connec.append(connect)
            IP_list.append(addr)
            print ("User IP, ",addr)
            data = connect.recv(1024)
        
            print ("Received data ,", data.decode('UTF-8','ignore'))
            if data.decode('UTF-8','ignore') == "Request":
                gamers.append(addr)
                connect.sendall(str(len(connec)-1).encode("utf8"))
        print ("Game already established!")
        print ("All requirements statisfied , we are about to launch....")
    
        connec[0].sendall(("clear").encode("utf8"))
        connec[1].sendall(("clear").encode("utf8"))
 
        while True:
            try:
                data1 = connec[0].recv(512)
                if data1.decode("UTF-8",'ignore') == "done":
                    print("data1 quit")
                    break
                connec[1].sendall((data1).encode("utf8"))

            except Exception, e:
                print ("One player quits, we are about to restart....")
                break
            try:
                data2 = connec[1].recv(512)
                if data2.decode("UTF-8",'ignore') == "done":
                    print ("data2 quit")
                    break
                connec[0].sendall((data2).encode("utf8"))
            except Exception, e:
                print ("One player quits, we are about to restart....")
                break

 