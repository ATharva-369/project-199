import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000
server.bind((ip_address,port))

server.listen()
clients = []
questions = [
    "What other country, besides the US, uses the US dollar as its official currency?\na.Equador\n  b.Canada\n  c.Mexico \n d.United Kingdom",
    "The Statue of Liberty was a gift to the United States from which European country?\n a.Belgium\n b.Germany\n c.Spain\n d.France",
    "Which artist famously cut off his own ear?\n a.Vincent Van Gogh\n b.Claude Monet\n c.Salvador Dali\n d.Pablo Picasso",
     "The Mad Hatter and the Cheshire Cat are characters in which famous book?\n a.Winne-the-Pooh\n b.Charlotte's Web\n c.Charlie and the Chocolate Factory\n d.Alice In Wonderland"
]
answers = ['a','d','a','d']

#remove question
def remove_question(index):
    questions.pop(index)
    answers.pop(index)

# client thread function
def clientthread(conn,addr):
    conn.send('Welcome to trivia game!\n'.encode('utf-8'))
    conn.send('You will receieve a question that needs to be answered by choosing between a,b,c or d\n'.encode('utf-8'))
    conn.send('All the best!!\n'.encode('utf-8'))
    index , question , answer = get_random_qa(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score +=1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time\n\n".encode('utf-8'))
                    remove_question(index)    
                    index, question , answer = get_random_qa(conn)
            else : 
                remove(conn)    
        except:
            continue            

# get random question answer function
def get_random_qa(conn):
    rand_ind = random.randint(0,len(questions)-1)
    rand_ques = questions[rand_ind]
    rand_ans = answers[rand_ind]
    conn.send(rand_ques.encode('utf-8'))
    return rand_ind, rand_ques, rand_ans    

while True:
    conn,addr = server.accept()
    clients.append(conn)
    print(addr[0] + ' connected')
    new_thread = Thread(target=clientthread, args=(conn,addr))
    new_thread.start()
