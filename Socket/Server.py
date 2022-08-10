import socket
import struct

#server details
#server ip
import threading
import time

host=socket.gethostname() #stay aware of making changes in the host ip #not defining any can use publicip ig
video_port=9999
audio_port=9998
chat_port=9997
#creating three sockets --> three different channels
video_socket=socket.socket()
audio_socket=socket.socket()
chat_socket=socket.socket()

#binding the socket with the server
video_socket.bind((host,video_port))
audio_socket.bind((host,audio_port))
chat_socket.bind((host,chat_port))

#start listening on each socket
video_socket.listen(5) #5 here is the listening capacity of the server means at the same time only 5 connection can be in waiting
audio_socket.listen(5)
chat_socket.listen(5)



#how to store the things
#i have to two types of persons
#1-->streamer  ---> stream name, ip address and port
#2-->viewer   ---> stream name, username, ip address and port

#array of streams harek stream ke andar streamer ka ip and connected members unka ip hoga

#todo: closing connections

class Data:
    def __init__(self):
        self.streamname=''
        self.nameofstreamer=''
        self.streamerconn=None
        self.streameraddr=''
        self.member_conn = []
        self.member_addresses = []
        self.member_names = []



All_data_video=[]
All_data_audio=[]
All_data_chat=[]

#todo: chack for changing conn to menbers at all place
def send_video_to_others(conn,streamname):
    while True:
        recieved_item=conn.recv(4096)
        if recieved_item:
            for stream in All_data_video:
                if (streamname == stream):
                    for members in stream.member_conn:
                        if (members != conn):
                            members.send(recieved_item)


def send_audio_to_others(conn,streamname):
    while True:
        recieved_item=conn.recv(4096)
        if recieved_item:
            for stream in All_data_audio:
                if (streamname == stream):
                    for members in stream.member_conn:
                        if (members != conn):
                            members.send(recieved_item)



def send_chats_to_others(conn,streamname):

    while True:
        chatmsg=conn.recv(4096)
        print("server ok -->"+str(chatmsg))
        if chatmsg:
            print("ok")
            for stream in All_data_chat:
                if(streamname==stream):
                    for members in stream.member_conn:
                        print("ahiya avtu che")
                        print("member --> " + str(members))
                        print("streamer---> "+ str(conn))
                        if(members!=conn):
                            print("ahiya bhi ave che")
                            members.send(chatmsg)


def video_socket_accept():
    print("accept 1")
    while True:
        conn,address=video_socket.accept()
        #conn is a object which bascially contains send and all functions
        #address is a list of port and ip
        type_of_userhandling_video(conn,address)


def type_of_userhandling_video(conn,address):
    data=conn.recv(4096)
    data=data.decode("utf-8") #decoding data according to format of utf-8
    listdata = data.split(" ") #splitting the data based on the space
    print(listdata[0])
    #for finding the type of connection
    if(listdata[0]=='1'):
        Newdata = Data()  # data object
        Newdata.streamerconn = conn
        Newdata.streameraddr = address
        Newdata.streamname=listdata[1]
        Newdata.nameofstreamer=listdata[2]
        All_data_video.append(Newdata)
        threading.Thread(target=send_video_to_others,args=(conn,Newdata)).start()

    else:
        print(listdata[1])
        ok=True
        for stream in All_data_video:
            print(stream)
            if(stream.streamname==listdata[1]):
                print(conn)
                stream.member_conn.append(conn)
                stream.member_addresses.append(address)
                stream.member_names.append(listdata[2])
                ok=False
                break
        if ok:
            print("no such video stream is present")

def audio_socket_accept():
    print("accept 2")
    while True:
        #TODO:setblocking needed or not??
        conn,address=audio_socket.accept()
        #conn is a object which bascially contains send and all functions
        #address is a list of port and ip
        type_of_userhandling_audio(conn,address)


def type_of_userhandling_audio(conn,address):
    data=conn.recv(4096)
    data=data.decode("utf-8") #decoding data according to format of utf-8
    listdata = data.split(" ") #splitting the data based on the space

    #for finding the type of connection
    if(listdata[0]=='1'):
        Newdata = Data()  # data object
        Newdata.streamerconn = conn
        Newdata.streameraddr = address
        Newdata.streamname=listdata[1]
        Newdata.nameofstreamer=listdata[2]
        All_data_audio.append(Newdata)
        threading.Thread(target=send_audio_to_others, args=(conn,Newdata)).start()
    else:
        ok=True
        for stream in All_data_audio:
            if(stream.streamname==listdata[1]):
                stream.member_conn.append(conn)
                stream.member_addresses.append(address)
                stream.member_names.append(listdata[2])
                ok=False
                break
        if ok:
            print("no such audio stream is present")

def chat_socket_accept():
    print("accept 3")
    while True:
        conn,address=chat_socket.accept()
        #conn is a object which bascially contains send and all functions
        #address is a list of port and ip
        type_of_userhandling_chat(conn,address)


def type_of_userhandling_chat(conn,address):
    data=conn.recv(4096)
    data=data.decode("utf-8") #decoding data according to format of utf-8
    listdata = data.split(" ") #splitting the data based on the space

    #for finding the type of connection
    if(listdata[0]=='1'):
        Newdata = Data()  # data object
        Newdata.streamerconn = conn
        Newdata.streameraddr = address
        Newdata.streamname=listdata[1]
        Newdata.nameofstreamer=listdata[2]
        Newdata.member_conn.append(conn)
        All_data_chat.append(Newdata)
        threading.Thread(target=send_chats_to_others, args=(conn,Newdata)).start()

    else:
        ok=True
        for stream in All_data_chat:
            if(stream.streamname==listdata[1]):
                stream.member_conn.append(conn)
                stream.member_addresses.append(address)
                stream.member_names.append(listdata[2])
                ok=False
                threading.Thread(target=send_chats_to_others, args=(conn, stream)).start()
                break
        if ok:
            print("no such stream is present")



#creating thread for accepting the socket request each for audio,video,chat

try:
    threading.Thread(target=video_socket_accept).start()
except:
    print("error1")

try:
    threading.Thread(target=audio_socket_accept).start()
except:
    print("error2")

try:
    threading.Thread(target=chat_socket_accept).start()
except:
    print("error3")






























