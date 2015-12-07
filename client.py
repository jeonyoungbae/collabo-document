# telnet program example
import kivy
kivy.require('1.0.4')
import socket, select, string, sys
import thread
import threading
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import Queue

class MyApp(App):

    class action_queue(object):
        def __init__(self, action, msg):
            self.action = action
            self.msg = msg

    s = None
    opened = False
    textinput = TextInput(size_hint=(1,1))
    q = Queue.Queue()

    def prompt(self):
        sys.stdout.write('<You> ')
        sys.stdout.flush()

    def send_data(self, msg):
        if self.s is not None:
            self.s.send(msg)
        else:
            print "s is None"
        self.prompt()

    def recieve_data(self, msg):
        #textinput = self.textinput
        #if textinput is not None:
        #self.textinput.text = msg
        print msg
        self.prompt()

    def start_network(self):
        if(len(sys.argv) < 3) :
            print 'Usage : python telnet.py hostname port'
            sys.exit()

        host = sys.argv[1]
        port = int(sys.argv[2])
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(2)

        # connect to remote host
        try :
            self.s.connect((host, port))
        except :
            print 'Unable to connect'
            sys.exit()

        print 'Connected to remote host. Start sending messages'
        self.prompt()

        while 1:

            socket_list = [sys.stdin, self.s]

            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

            for sock in read_sockets:
                #incoming message from remote server
                if sock == self.s:
                    data = sock.recv(4096)
                    if not data :
                        print '\nDisconnected from chat server'
                        sys.exit()
                    else :
                        #print data
                        self.recieve_data(data)
                #user entered a message
                else :
                    msg = sys.stdin.readline()
                    self.send_data(msg)

    def build(self):
        textinput = self.textinput
        textinput.bind(text = self.on_text)

        def rcv_callback():
            col = textinput.cursor_col
            row = textinput.cursor_row
            print 'cursor col : ', col
            print 'cursor row : ', row
            textinput.text = 'recieving'

        box = BoxLayout(orientation='vertical')
        box.add_widget(textinput)
        #textinput.text = "sample"
        t = thread
        t.start_new_thread(self.start_network,())
        return box

    #start_network()

    def on_text(self, instance, value):
        if value is not "":
            self.opened = True
        if self.opened:
            print "[sended]"
            self.send_data(value)
        print value


#main function
if __name__ == "__main__":
    MyApp().run()
