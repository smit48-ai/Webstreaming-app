
#for desgin purpose
#one root rule and many child rules which are instance of some class in Kv



desgin = """
ScreenManager:
    MenuScreen:
    MakestreamScreen:
    StreamScreen:
    JoinScreen:
    StreamScreen2:

<MenuScreen>:
    name:'ShowYou'
    MDRectangleFlatButton:
        text: 'Go Live'
        pos_hint: {'center_x':0.5,'center_y':0.6}
        on_release: root.go_live()

    MDRectangleFlatButton:
        text: 'Join a Stream'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        on_press: root.join_stream()


<MakestreamScreen>
    name:'Form'
    spacing:100
    MDTextField:
        size_hint_x:0.3
        id:nameofstream
        hint_text: "Enter name of stream"
        pos_hint: {'center_x':0.5,'center_y':0.6}

    MDTextField:
        size_hint_x:0.3
        id:Username
        hint_text: "Username"
        pos_hint: {'center_x':0.5,'center_y':0.5}
        bind:

    MDRectangleFlatButton:
        text: 'Submit'
        pos_hint: {'center_x':0.5,'center_y':0.4}
        on_press: root.connection()



<StreamScreen>:
    name:'Live'
    on_enter:self.startthreads()
    GridLayout:
        rows:2
        padding:10
        GridLayout:
            rows:1
            Image:
                id:video
                size_hint:(1,1)
        GridLayout:
            rows:2
            ScrollView:
                size_hint:(1,0.8)
                MDList:
                    id:chatpage
            GridLayout:
                cols:2 
                size_hint:(1,0.2)
                MDTextField:
                    id:chats
                    hint_text: "chat live"
                    size_hint_x:0.6
                MDRectangleFlatButton:
                    text: 'Submit'
                    pos_hint: {'y':0.05}
                    on_press: root.New_chat()

<JoinScreen>:
    name:'Join'
    spacing:100

    MDTextField:
        size_hint_x:0.3
        id:nameofstream
        hint_text: "Enter name of stream"
        pos_hint: {'center_x':0.5,'center_y':0.6}

    MDTextField:
        size_hint_x:0.3
        id:Username
        hint_text: "Enter Your name"
        pos_hint: {'center_x':0.5,'center_y':0.5}
        bind:

    MDRectangleFlatButton:
        text: 'Join'
        pos_hint: {'center_x':0.5,'center_y':0.4}
        on_press: root.connection()

<StreamScreen2>:
    name:'Livewatching'
    on_enter:self.startthreads()
    GridLayout:
        rows:2
        padding:10
        GridLayout:
            rows:1
            Image:
                id:video
                size_hint:(1,1)
        GridLayout:
            rows:2
            ScrollView:
                size_hint:(1,0.8)
                MDList:
                    id:chatpage
            GridLayout:
                cols:2  
                size_hint:(1,0.2)
                MDTextField:
                    id:chats
                    hint_text: "chat live"
                    size_hint_x:0.7
                MDRectangleFlatButton:
                    text: 'Submit'
                    pos_hint: {'y':0.05}
                    on_press: root.New_chat()





"""
