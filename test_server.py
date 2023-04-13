import socket
import select

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import sys

class OpenPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.greetings = Label(text='Hallo, would you like to start server?', font_size=Window.size[1]*0.05)
        self.add_widget(self.greetings)

        y = Window.size[1]*0.1
        x = Window.size[0]*0.1

        self.yes_no = GridLayout(cols=2, padding=[y, x])

        self.yes_button = Button(text='Yes', font_size=Window.size[1]*0.1)
        self.yes_button.bind(on_press=self.server_window)
        self.yes_no.add_widget(self.yes_button)

        self.no_button = Button(text='No', font_size=Window.size[1]*0.1)
        self.no_button.bind(on_press=self.server_kill)
        self.yes_no.add_widget(self.no_button)

        self.add_widget(self.yes_no)

    def server_window(self, _):
        server.screen_manager.current = 'Server'

    def server_kill(self, _):
        self.greetings.text = 'Ok, buy'
        Clock.schedule_once(sys.exit, 3)

class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y=None, markup=True)
        self.scroll_to_point = Label()


        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)


    def update_chat_history(self, message):
        self.chat_history.text += '\n' + message

        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

        self.scroll_to(self.scroll_to_point)

    def update_chat_history_layout(self, _=None):
        self.layout.height = self.chat_history.texture_size[1]+15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.98, None)

class ServerPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 1


        self.turn_on=Button(text="turn this server on")
        self.turn_on.bind(on_press = self.turner)
        self.add_widget(self.turn_on)



    def turner(self, _):
        HEADER_LENGTH = 10
        IP = "127.0.0.1"
        PORT = 1234
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((IP, PORT))
        server_socket.listen()
        sockets_list = [server_socket]
        clients = {}
        print(f'Listening for connections on {IP}:{PORT}...')
        def receive_message(client_socket):
            try:
                message_header = client_socket.recv(HEADER_LENGTH)
                if not len(message_header):
                    return False
                message_length = int(message_header.decode('utf-8').strip())
                return {'header': message_header, 'data': client_socket.recv(message_length)}
            except:
                return False
        while True:
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
            for notified_socket in read_sockets:
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()
                    user = receive_message(client_socket)
                    if user is False:
                        continue
                    sockets_list.append(client_socket)
                    clients[client_socket] = user
                    print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                                    user['data'].decode('utf-8')))
                else:
                    message = receive_message(notified_socket)
                    if message is False:
                        print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                        sockets_list.remove(notified_socket)
                        del clients[notified_socket]
                        continue
                    user = clients[notified_socket]
                    print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                    for client_socket in clients:
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
            for notified_socket in exception_sockets:
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
class ServerApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.open_page = OpenPage()
        self.screen = Screen(name='Starting')
        self.screen.add_widget(self.open_page)
        self.screen_manager.add_widget(self.screen)

        self.server_page = ServerPage()
        self.screen = Screen(name='Server')
        self.screen.add_widget(self.server_page)
        self.screen_manager.add_widget(self.screen)
        print('test 1')

        return self.screen_manager


if __name__ == '__main__':
    server = ServerApp()
    server.run()