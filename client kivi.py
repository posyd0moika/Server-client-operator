import socket
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from time import sleep
from kivy.uix.label import Label


dict_send_mess = {
    "CC": "card_credit",
    "CD": "card_debit",
    "M": "mortgage",
    "BA": "brokerage_account"
}


class ClientApp(App):


    def on_press_button(self, instance):
        text = instance.text.rstrip("[/color]").lstrip("[color=000000]")
        text = send_message(text)
        main_layout_text.text = text





    def build(self):

        # global box_layout
        # box_layout = BoxLayout()

        global main_layout
        main_layout = BoxLayout(orientation="vertical",
                                spacing=5,
                                padding=[5],
                                pos_hint={'center_x': .5, 'center_y': .5},
                                size_hint=(.7, .7)
                                )
        global main_layout_text
        main_layout_text = Label(text=f"[color=ffffff] x [/color]",
                                 markup=True,
                                 font_size='60sp',
                                 color=[1, 1, 1, 1],
                                 )

        buttons = [
            ["CC", "CD"],
            ["M", "BA" ],
        ]

        for row in buttons:
            h_layout = BoxLayout(spacing=5, padding=[5])
            for label in row:
                button = Button(
                    text=f"[color=000000]{label}[/color]",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_press=self.on_press_button,
                    markup=True,
                    font_size="50sp",
                    background_color=[1, 1, 1, 1],
                    background_normal="",
                )
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
        # box_layout.add_widget(main_layout)
        main_layout.add_widget(main_layout_text)
        return main_layout


def send_message(text):
    mess = "client " + text
    sock.send(mess.encode("UTF-8"))
    data = (sock.recv(4096)).decode()  # Принимаем сообщение
    print(data)
    return data


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 5003)  # Подключаем сокет к порту,
    # через который прослушивается сервер
    sock.connect(server_address)  # Конектим слиента к серверу

    # print("\033[4m\033[37m\033[44m{}\033[0m".format(f"Posible comand:"), "\nCC,CD,M,BA,break")

    Config.set("graphics", "resizable", "0")
    Config.set("graphics", "widht", "600")
    Config.set("graphics", "height", "800")
    app = ClientApp()
    app.run()