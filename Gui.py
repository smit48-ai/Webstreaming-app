from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.graphics.texture import Texture
from kivy.clock import Clock,mainthread
from Socket import client
import Appdesgin
import pyshine as ps
from kivymd.uix.list import OneLineListItem
import threading
import pickle
import struct
import cv2

# <----------------------------------------threading concept----------------------------------------------------------->
# To spawn another thread, you need to call following method available in thread module −
# thread.start_new_thread ( function, args[, kwargs] )
# This method call enables a fast and efficient way to create new threads in both Linux and Windows.
# The method call returns immediately and the child thread starts and calls function with the passed list of args.
# When function returns, the thread terminates.
# Here, args is a tuple of arguments; use an empty tuple to call function without passing any arguments.
# kwargs is an optional dictionary of keyword arguments.

# <----------------------------------------threading concept----------------------------------------------------------->

# this is actually type of dom mode and with properties and all
# posinning with respect to parent layout screen
# sizing with respect to parent layout screen

frames=[]
chats=[]
audios=[]
username=""

#todo: check for the video
#todo: check for data=b"" msgsize[0] and pickle.loads

def start_reciving_chats():
    while True:
        print("reciving no thread to kam kare che")
        chat_msg= client.client_socket_chat.recv(4096).decode('utf-8')
        print("client recieved ok -->" + chat_msg)
        chats.append(chat_msg)
        print(len(chats))



def start_reciving_video():
    data=b""
    payload_size = struct.calcsize('Q')  # this much size of data recived is just for the lenght of the data coming
    while True:
        while len(data)<payload_size:
            packet = client.client_socket_video.recv(4 * 1024)  # 4K
            if not packet: break
            data += packet
        packed_msg_size=data[:payload_size]
        data=data[payload_size:]#extra taken data has to be there in the data variable
        msz_size=struct.unpack("Q",packed_msg_size)[0]
        while len(data)<msz_size:
            data+= client.client_socket_video.recv(4096)
        frame_data=data[:msz_size]
        data=data[msz_size:] #extra data can be of next frame
        frame=pickle.loads(frame_data)
        frames.append(frame)



def start_reciving_audio():
    data = b""
    payload_size = struct.calcsize('Q')  # this much size of data recived is just for the lenght of the data coming
    while True:
        while len(data) < payload_size:
            packet = client.client_socket_audio.recv(4 * 1024)  # 4K
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]  # extra taken data has to be there in the data variable
        msz_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msz_size:
            data += client.client_socket_audio.recv(4096)
        frame_data = data[:msz_size]
        data = data[msz_size:]  # extra data can be of next frame
        frame = pickle.loads(frame_data)
        print(frame)
        audio, context = ps.audioCapture(mode='get')
        audio.put(frame)

# for defining the screens and for defining the functionalities of screens

class MenuScreen(Screen):

    def go_live(self):
        self.manager.current='Form'

    def join_stream(self):
        self.manager.current='Join'



class MakestreamScreen(Screen):
    def connection(self):
        name = self.ids.nameofstream.text
        global username
        username=self.ids.Username.text
        client.connect_to_server_as_streamer(name, username)
        self.manager.current='Live'


class StreamScreen(Screen):

    def New_chat(self):
        chatmsg=username+">"+self.ids.chats.text
        item = OneLineListItem(text=chatmsg)
        self.ids.chatpage.add_widget(item)
        self.ids.chats.text=''
        client.send_chat(chatmsg)

    def startthreads(self):
        threading.Thread(target=self.start_video).start()
        # threading.Thread(target=self.start_audio).start()
        threading.Thread(target=self.start_chat).start()

    def start_audio(self):
        client.start_sending_audio()


    def start_video(self):

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0 / 30.0)


    def load_video(self, *args):
        ret, frame = self.capture.read()
        # Reading (cam.read()) from a VideoCapture returns a tuple (return value, image).
        # With the first item you check wether the reading was successful,
        # and if it was then you proceed to use the returned image.
        #this is some matrix data of 0 to 255 values
        client.start_sending_video(frame)
        buffer = cv2.flip(frame, 0).tobytes()
        # texture is like handling the  graphics thing
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        # how the buffers is stored and in which colour format the texture is created
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.ids.video.texture = texture

    def start_chat(self):
        threading.Thread(target=start_reciving_chats).start()
        while True:
            if len(chats) != 0:
                chatsmsg = chats.pop()
                self.add_item(chatsmsg)

    # Decorator that will schedule the call of the function for the next available frame in the mainthread.
    # It can be useful when you use UrlRequest or when you do Thread programming: you cannot do any OpenGL - related work in a thread.
    @mainthread
    def add_item(self, chatsmsg):
        item = OneLineListItem(text=chatsmsg)
        self.ids.chatpage.add_widget(item)

    @mainthread
    def rendervideo(self, texture):
        pass


class JoinScreen(Screen):
    #TODO: join to sever and request for array of the streamname and conn at present assume that users know which stream they want to join
    def connection(self):
        Streamname=self.ids.nameofstream.text
        global username
        username=self.ids.Username.text
        client.connect_to_server_as_viewr(Streamname, username)
        self.manager.current='Livewatching'



class StreamScreen2(Screen):

    def New_chat(self):
        chatmsg=username+">"+self.ids.chats.text
        item = OneLineListItem(text=chatmsg)
        self.ids.chats.text = ''
        self.ids.chatpage.add_widget(item)
        client.send_chat(chatmsg)


    def startthreads(self):
        threading.Thread(target=start_reciving_video).start()
        Clock.schedule_interval(self.start_video,1.0 / 30.0)
        # threading.Thread(target=self.start_audio).start()
        threading.Thread(target=self.start_chat).start()

    # @mainthread
    def start_video(self, *args):
        if len(frames)!=0:
            self.frame=frames.pop()
            self.buffer = cv2.flip(self.frame, 0).tobytes()
            # texture is like handling the  graphics thing
            self.ids.video.texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
            # how the buffers is stored and in which colour format the texture is created
            # print("client recieved ok -->" + frame)
            self.ids.video.texture.add_reload_observer(self.populate_texture)
            self.populate_texture(self.ids.video.texture)

    def populate_texture(self,texture):
        texture.blit_buffer(self.buffer, colorfmt='bgr', bufferfmt='ubyte')


    def start_audio(self):
        threading.Thread(target=start_reciving_audio).start()
        audio = ps.audioCapture(mode='recv')
        while True:
            if len(audios) != 0:
                frame = frames.pop()
                audio.put(frame)


    def start_chat(self):
        threading.Thread(target=start_reciving_chats).start()
        while True:
            if len(chats) != 0:
                chatsmsg=chats.pop()
                self.add_item(chatsmsg)

    # Decorator that will schedule the call of the function for the next available frame in the mainthread.
    # It can be useful when you use UrlRequest or when you do Thread programming: you cannot do any OpenGL - related work in a thread.
    @mainthread
    def add_item(self,chatsmsg):
        item = OneLineListItem(text=chatsmsg)
        self.ids.chatpage.add_widget(item)

    @mainthread
    def rendervideo(self,texture):
        pass



# screen managers to switch between the screens
# sm = ScreenManager()
# sm.add_widget(MenuScreen(name='ShowYou'))
# sm.add_widget(MakestreamScreen(name='Form'))
# sm.add_widget(StreamScreen(name='Live'))

#main app class to be run
class ShowYou(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Yellow"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(Appdesgin.desgin)


mainappobj=ShowYou();
mainappobj.run() #calls build method



