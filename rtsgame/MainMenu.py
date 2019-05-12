import multiprocessing
import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox


# import eventlet
# eventlet.monkey_patch()


class Master(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("400x200")
        self.resizable(width=False, height=False)
        self.title_font = tkfont.Font(family='Helvetica', size=18,
                                      weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Frame in (MainMenu, MultiPlayer, Loading, Settings, Connect):
            page_name = Frame.__name__
            frame = Frame(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def exit_app(self):
        input_ = tk.messagebox.askquestion('Exit Application',
                                           'Are you sure you want to exit the '
                                           'application',
                                           icon='warning')
        if input_ == 'yes':
            self.destroy()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def single_player_start(self):
        from rtsgame.src.Client.Game import game
        server_thread = multiprocessing.Process(target=run_server,
                                                args=["Singleplayer"])
        server_thread.start()
        self.destroy()

        time.sleep(5)
        game.run("localhost")

    def connect(self, ip: tk.StringVar):
        from rtsgame.src.Client.Game import game
        self.destroy()
        game.run(ip.get())

    def create_multiplayer_server(self):
        from rtsgame.src.Client.Game import game
        server_thread = multiprocessing.Process(target=run_server,
                                                args=["Multiplayer"])
        server_thread.start()
        self.destroy()

        time.sleep(5)

        game.run("localhost")


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Main menu", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        singleplayer_button = tk.Button(self, text="Single Player",
                                        command=lambda: [
                                            controller.show_frame("Loading"),
                                            controller.single_player_start()])
        multiplayer_button = tk.Button(self, text="Multi Player",
                                       command=lambda: controller.show_frame(
                                           "MultiPlayer"))
        settings_button = tk.Button(self, text="Settings",
                                    command=lambda: controller.show_frame(
                                        "Settings"))
        exit_button = tk.Button(self, text="Exit",
                                command=controller.exit_app)
        singleplayer_button.pack()
        multiplayer_button.pack()
        settings_button.pack()
        exit_button.pack()


class MultiPlayer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        host_game_button = tk.Button(self, text="Host Game",
                                     command=lambda: controller.create_multiplayer_server())
        connect_button = tk.Button(self, text="Connect",
                                   command=lambda: controller.show_frame(
                                       "Connect"))
        back_button = tk.Button(self, text="Back",
                                command=lambda: controller.show_frame(
                                    "MainMenu"))
        host_game_button.pack()
        connect_button.pack()
        back_button.pack()


class Loading(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Loading ...", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        cancel_button = tk.Button(self, text="Cancel",
                                  command=lambda: controller.show_frame(
                                      "MainMenu"))
        cancel_button.pack()


class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_button = tk.Button(self, text="Back",
                                command=lambda: controller.show_frame(
                                    "MainMenu"))
        back_button.pack()


class Connect(tk.Frame):
    def __init__(self, parent, controller):
        ip = tk.StringVar()
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Connect", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        ip_entry = tk.Entry(self, textvariable=ip)
        ip_entry.pack()

        connect_button = tk.Button(self, text="Connect",
                                   command=lambda: [
                                       controller.show_frame("Loading"),
                                       controller.connect(ip)])
        back_button = tk.Button(self, text="Back",
                                command=lambda: controller.show_frame(
                                    "MainMenu"))
        connect_button.pack()
        back_button.pack()


def run_server(mode):
    import rtsgame.App
    rtsgame.App.start_game(mode)

def main():
    app = Master()
    app.protocol("WM_DELETE_WINDOW", app.exit_app)
    app.mainloop()

if __name__ == "__main__":
    main()


