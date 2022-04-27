import socket
import sys
import time
import datetime
import random
import os
from os.path import exists
print('.......................')
print('Initializing FTP Server')
print('.......................')
print(socket.gethostbyname(socket.gethostname())) # have tp be inside the directory of the program or else it will be masked
print('.......................')

#TCPport=input('enter a custom tcp port number for your server\n')
TCPport=input('please select your custom TCP port number,5 default')
if len(TCPport)<1 or TCPport==' ':
    TCPport=5
def ConnectWithClient():
    requestNumber=random.randint(0,10000) #r randomized because i said so 
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (socket.gethostbyname(socket.gethostname()), int(TCPport))              
    print('starting up on %s port %s' % server_address)
    print('.......................')
    sock.bind(server_address)
    
    sock.listen(1)

    while True:
        print('Waiting for a connection from the clients')
        connection, client_address = sock.accept()

        try:
                print('Connection From: ' + str(client_address))            
                data = connection.recv(200)


                if data.decode()[0:4]=='bye ':
                                
                    print('hey')

                if data.decode()[0:7]=='change ':
                                
                    chunks = data.decode().split(' ')
                    falsehood=exists(chunks[1])
                    if(falsehood): # if server actually have the file
                        
                        os.rename(chunks[1],chunks[2])                   
                        currentTime = datetime.datetime.now()
                        with open('serverlog.txt', 'a+') as logfile:   
                                        logfile.write(str(currentTime)+' UPDATE RQ: '+str(requestNumber)+' : '+str(data.decode()))
                                        logfile.write('\n')
                        logfile.close() 


                elif data.decode()[0:4]=='put ':

                    print('attemping to publish new file~~~')
                    chunks2 = data.decode().split(' ')
                    time.sleep(5)  # set a delay of 5000ms because i m always late by 5 seconds in everything
                 
                     
                    requestDownload('6666','127.0.1.1',chunks2[1])              
                   
                else:

                    #print('Transfering "%s"' % data)   
                    

                    try:
                        
                        currentTime = datetime.datetime.now()
                        with open('serverlog.txt', 'a+') as logfile:   
                                        logfile.write(str(currentTime)+' DOWNLOAD RQ: '+str(requestNumber)+' file name sent: '+str(data.decode()))
                                        logfile.write('\n')
                        logfile.close()
                        requestNumber=requestNumber+1   
                        with open(data.decode(), 'r+') as f:
                            data = f.read().rstrip() 
                                        
                            connection.sendall(data.encode())
                                                
                    except:
                        currentTime = datetime.datetime.now()
                        data='DOWNLOAD-ERROR, file dont exist'
                        connection.sendall(data.encode())
                        requestNumber=requestNumber+1

        except socket.error as msg:
            print('Error')                    
        finally:
            connection.close()

def requestDownload(destination,host,alert):
            
    tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:            
            server_address = (host, int(destination))
            tempsock.connect(server_address)
            tempsock.sendall(alert.encode())

            string=''           
            while True:
              
                data = tempsock.recv(50) # length                
                if not data:
                        break
                if data.decode()=='DOWNLOAD-ERROR, file dont exist':
                    print(data.decode())
                elif len(data)<50:

                        string=string+data.decode()
                        print('File downloaded')
                        stdout = sys.stdout
                            
                        try:
                                    sys.stdout = open(alert, 'w')
                                    print(string)

                        finally:
                                    sys.stdout.close()  # close file.txt
                                    sys.stdout = stdout
                        
                        break      # Ends everything here *****************************                 
                else:


                        string=string+data.decode()
    except:        
        print('Wrong port, make sure you enter the right port number ')            
        tempsock.close()
    finally:        
        tempsock.close()


        
ConnectWithClient()



