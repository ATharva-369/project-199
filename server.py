import socket
from threading import Thread

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000
server.bind((ip_address,port))

server.listen()
clients = []
print('server is running')


def remove(conn):
    if conn in clients:
        clients.remove(conn)

def broadcast(message,connection):
    for client in clients:
        if client != connection:
            try: 
                client.send(message.encode('utf-8'))
            except :
                remove(client)    


def clientthread(conn,addr):
    conn.send('Welcome to this chatroom'.encode('utf-8'))
    while True:
        try : 
            message = conn.recv(2048).decode('utf-8')
            if message:
                print('<',addr[0],'>',message)
                messageToSend = '<',addr[0],'>',message
                broadcast(messageToSend, conn)
            else:
                remove(conn)    
        except :    
             continue    
       


while True :
    conn, addr = server.accept()
    clients.append(conn)
    print(addr[0] + ' connected')
    new_thread = Thread(target=clientthread,args = (conn,addr))
    new_thread.start()
