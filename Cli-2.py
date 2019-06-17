# to client-1: send msg; receive msg; send msg
# within defined functions
# just one socket in use
# modular structure
# prevent application from crashing due an expected 'ConnectionResetError' (connection handling) and quitting

import socket
import threading


class client2Class:
    # class variabels:
    TCP_IP = socket.gethostbyname(socket.gethostname())
#    TCP_IP = '192.168.2.134'
    TCP_PORT = 1234
    HEADERSIZE = 10

    # connect to the default port
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # SOCK_STREAM -> TCP
        self.sock.connect((client2Class.TCP_IP, client2Class.TCP_PORT))       # connect to client socket
        print("---- Client 2 active ----\n")


    def main(self):
        try:
            print('Connection from client-2: ', socket.gethostbyname(socket.gethostname()), ' to CLIENT-1: ', client2Class.TCP_IP)
            # msg = "Welcome from CLIENT-2!"
            t0 = threading.Thread(target = self.sendCli2())
            t1 = threading.Thread(target = self.recvCli2())
            t0.start()
            t1.start()
            # msg = input("Second msg to client-1?: ")
            # self.sendCli2(msg)
        except ConnectionResetError as e:
            print("Client-1 closed the window\n", "OS-Error:", e, "\nApplication quitted")


    def sendCli2(self):
        msg = input("Second msg to client-1?: ")
        msg = f"{len(msg):<{client2Class.HEADERSIZE}}" + msg     # rebuild msg: counting length of msg and append the length number in front of the msg within the defined headersize
        self.sock.send(bytes(msg, "utf-8"))     # send msg in given transformation format


    def recvCli2(self):
            fullClient1Msg = ''
            newClient1Msg = True

            while True:
                msg = self.sock.recv(16)

                if newClient1Msg == True:
                    print(f"First 10 characters of client-1's message: {msg[:client2Class.HEADERSIZE]}")
                    msgLen = int(msg[:client2Class.HEADERSIZE])
                    newClient1Msg = False

                fullClient1Msg += msg.decode("utf-8")

                if len(fullClient1Msg)-client2Class.HEADERSIZE == msgLen:
                    print("Client-1's message received: ", fullClient1Msg[client2Class.HEADERSIZE:])
                    break



client2Object = client2Class()
client2Object.main()




# self.s.close()???
# later: getsockname() and getpeername()
