import socket
import pickle
import struct
import cv2
import pyshine as ps
import tempfile
import imutils


host = '192.168.137.1' # stay aware of making changes in the host ip  #not definging any can use publicip ig
video_port=9999
audio_port=9998
chat_port=9997
client_socket_video=socket.socket()
client_socket_audio=socket.socket()
client_socket_chat=socket.socket()


def connect_to_server_as_viewr(streamname,username):
    try:
        client_socket_video.connect((host, video_port))
        # client_socket_audio.connect((host,audio_port))
        client_socket_chat.connect((host,chat_port))
        datatobesend = "0 " + streamname + " " + username
        datatobesend=datatobesend.encode('utf-8');
        # client_socket_audio.send(datatobesend)
        client_socket_video.send(datatobesend)
        client_socket_chat.send(datatobesend)
        print('connectd to server')
    except:
        print("error in making a socket")


def connect_to_server_as_streamer(name,username):
    try:
        client_socket_video.connect((host, video_port))
        # client_socket_audio.connect((host, audio_port))
        client_socket_chat.connect((host, chat_port))
        datatobesend = "1 " + name +" "+username
        datatobesend=datatobesend.encode('utf-8');
        print(datatobesend)
        # client_socket_audio.send(datatobesend)
        client_socket_video.send(datatobesend)
        client_socket_chat.send(datatobesend)
    except:
        print("error in making a socket")



# At first Python pickle serialize the object and then converts the object into a character stream so that this character
# stream contains all the information necessary to reconstruct the object in another python script.



# pickle is ok for data serialization but you have to make a protocol of you own for the messages you exchange between the client and the server,
# this way you can know in advance the amount of data to read for unpickling (see below)

# socket.send is a low-level method and basically just the C/syscall method send(3) / send(2).
# It can send less bytes than you requested, but returns the number of bytes sent.
# socket.sendall is a high-level Python-only method that sends the entire buffer you pass or throws an exception.
# It does that by calling socket.send until everything has been sent or an error occurs.
# If you're using TCP with blocking sockets and don't want to be bothered by internals
# (this is the case for most simple network applications), use sendall.

#bestpossible definition for sendall()
# Unlike send(), this method continues to send data from string until either all data has been sent or an error occurs.
# None is returned on success. On error, an exception is raised,
# and there is no way to determine how much data, if any, was successfully sent
#H is for unsigned short integer format


def start_sending_video(frame):
    serialized_data=pickle.dumps(frame)
    # encode method can work for string only
    # convering the data to character stream because ig we cannot
    # send the matrix data and all
    # finally it will be bits or characterstream data which can be passed over the netwrok
    # print(frame)
    message=struct.pack("Q",len(serialized_data))+serialized_data
    client_socket_video.sendall(message)
    #we cannot use the len --> str --> encode becuase on reciving side it may lead to take
    # some data from serialize_data as well we will be mashed up
    # length is to be passed so that the server came to know about when the one frame completes
    # coneverting the character stream length to bytes object
    # and sending it along with the data

def send_chat(chats):
    print("client --> ok ")
    client_socket_chat.send(chats.encode('utf-8'))


#handle the issues with audiocaputre
def start_sending_audio():
    audio, context = ps.audioCapture(mode='send')
    #it will take the audio from the microphone of pc we can it set the microphone for
    # listeng and rendering frames on callinf get function

    while True:
        frame=audio.get()
        serialized_data=pickle.dumps(frame)
        client_socket_audio.sendall(struct.pack("Q",len(serialized_data))+serialized_data)











