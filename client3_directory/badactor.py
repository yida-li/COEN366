import socket
import multiprocessing
import sys
import time
import threading
import datetime
import random



ServerIP = input('enter the IP of the server please\n') 
while len(ServerIP)<1:
        ServerIP= input("you cant just enter blank IP")




ServerTCPport = input('enter the TCP port of the server\n')
while len(ServerTCPport)<1:
    ServerTCPport= input("you cant just enter blank TCP")  





ServerTCPport2 = input('enter the TCP port of the client\n')
while len(ServerTCPport2)<1:
    ServerTCPport2= input("you cant just enter blank TCP")   


requestNumber=random.randint(0,10000)  

def ConnectWithServer():
    
    while 1:
        msg = input('Enter message to send')
        if not msg:
                msg=''
        if msg=="get":  
            requestDownload(ServerTCPport,ServerIP)
        if msg=="change":  
            requestChange(ServerTCPport,ServerIP)
        if msg=="put":  
            requestPut(ServerTCPport,ServerIP)
            ConnectWithClient(ServerTCPport2)
        if msg=="help":  
            print('Commands are: bye change get help put')
        if msg=="bye":
            print('Session is terminated.')
            return False
  

def requestDownload(destination,host):
            
    tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:            
            server_address = (host, int(destination))
            tempsock.connect(server_address)
            alert= input("enter name of text file")
            while len(alert)<1:
                alert= input("you cant just enter blank") 
            tempsock.sendall(alert.encode())

            string=''           
            while True:
              
                data = tempsock.recv(50) # length                
                if not data:
                        break
                if data.decode()=='DOWNLOAD-ERROR, file dont exist':
                    print(data.decode())
                    currentTime = datetime.datetime.now()
                    with open('clientlog.txt', 'a+') as logfile:   
                                    logfile.write(str(currentTime)+'Attempting to DOWNLOAD : '+' file name: '+str(data.decode()))
                                    logfile.write('\n')
                    logfile.close()
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
        
def requestChange(destination,host):
            
    tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:            
            server_address = (host, int(destination))
            tempsock.connect(server_address)

            src= input("enter name of old text file")
            dst= input("to be changed to the name of new text file :")
            alert="change "+src+" "+dst
            tempsock.sendall(alert.encode())
            currentTime = datetime.datetime.now()
            with open('clientlog.txt', 'a+') as logfile:   
                            logfile.write(str(currentTime)+'ATTEMPING TO CHANGE: '+' file name :'+src+'to'+dst)
                            logfile.write('\n')
            logfile.close()
    except:        
        print('Wrong port, make sure you enter the right port number ')            
        tempsock.close()
    finally:        
        tempsock.close()


def requestPut(destination,host):
            
    tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:            
            server_address = (host, int(destination))
            tempsock.connect(server_address)

            src= input("enter name to be submitted")
            alert="put "+src
            tempsock.sendall(alert.encode())
    except:        
        print('Wrong port, make sure you enter the right port number ')            
        tempsock.close()
    finally:        
        tempsock.close()
    

def ConnectWithClient(TCPport):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (socket.gethostbyname(socket.gethostname()), int(TCPport))              
    print('starting up on %s port %s' % server_address)
    print('.......................')
    sock.bind(server_address)
    
    sock.listen(1)

    
 
    connection, client_address = sock.accept()

    try:
            print('Connection From: ' + str(client_address))            
            data = connection.recv(200)

            if data.decode()[0]==' ':
                print('bad ') 
            
            else:
                try:
                    currentTime = datetime.datetime.now()
                    with open('clientlog.txt', 'a+') as logfile:   
                                    logfile.write(str(currentTime)+' DOWNLOAD RQ: '+' file name sent: '+str(data.decode()))
                                    logfile.write('\n')
                    logfile.close()
       
                    with open(data.decode(), 'r+') as f:
                        data = f.read().rstrip() 
                                    
                        connection.sendall(data.encode())
                    connection.close()                         
                except:
                    currentTime = datetime.datetime.now()
                    data=str(currentTime)+'DOWNLOAD-ERROR RQ: '+str(requestNumber)+' Reason: file dont exist'
                    connection.sendall(data.encode())
                    requestNumber=requestNumber+1

    except socket.error as msg:
        print('Error')                    
    finally:
        connection.close()



        
ConnectWithServer()

