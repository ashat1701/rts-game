import tkinter as tk
from tkinter import font as tkfont


class Master(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("400x200")
        self.resizable(width=False, height=False)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Frame in (MainMenu, MultiPlayer, Loading, Settings, Host, Connect):
            page_name = Frame.__name__
            frame = Frame(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Main menu", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        singleplayer_button = tk.Button(self, text="Single Player",
                                        command=lambda: controller.show_frame("Loading"))
        multiplayer_button = tk.Button(self, text="Multi Player",
                                       command=lambda: controller.show_frame("MultiPlayer"))
        settings_button = tk.Button(self, text="Settings",
                                    command=lambda: controller.show_frame("Settings"))
        singleplayer_button.pack()
        multiplayer_button.pack()
        settings_button.pack()



class MultiPlayer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        host_game_button = tk.Button(self, text="Host Game",
                                     command=lambda: controller.show_frame("Host"))
        connect_button = tk.Button(self, text="Connect",
                                   command=lambda : controller.show_frame("Connect"))
        back_button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("MainMenu"))
        host_game_button.pack()
        connect_button.pack()
        back_button.pack()


class Loading(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Loading ...", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("MainMenu"))
        back_button.pack()


class Host(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)



class Connect(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


if __name__ == "__main__":
    app = Master()
    app.mainloop()
