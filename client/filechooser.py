#!/usr/bin/env python

from tkinter import Button, Label, Entry, Tk, messagebox, Scrollbar, RIGHT, Y, END, Text
from tkinter.ttk import Progressbar
from tkinter.filedialog import askdirectory
from threading import Thread

from client import Client
import settings


class FileChooserDialog(Tk):
    def __init__(self, parent=None):
        if parent:
            Tk.__init__(self, parent)
            self.parent = parent
        else:
            Tk.__init__(self)

        self.upload_folder = ""
        self.username = ""
        self.password = ""

        self.grid()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def open_file(self):
        try:
            self.upload_folder = askdirectory(title="Choose a file.")
        except:
            print("No file exists")

    def set_info_label(self, s):
        self.info_label["text"] = s

    def set_progressbar_max(self, amt):
        self.progressbar["maximum"] = amt

    def set_progressbar_amt(self, amt):
        self.progressbar["value"] = amt

    def quit_dialog(self):
        def get_formatted_server_id(ip, port):
            return str(ip) + ":" + str(port)

        self.username = self.username_input.get()
        self.password = self.password_input.get()
        self.server_ip = self.server_ip_input.get()
        self.server_port = self.server_port_input.get()

        if not self.username:
            messagebox.showinfo("Error", "Please enter a username.")

        elif not self.password:
            messagebox.showinfo("Error", "Please enter a password.")

        elif not self.upload_folder:
            messagebox.showinfo("Error", "Please enter a folder to upload.")

        elif not self.server_ip:
            messagebox.showinfo("Error", "Please enter a server IP address.")

        elif not self.server_port:
            messagebox.showinfo("Error", "Please enter a server port.")

        else:
            self.client = Client(
                uid=self.username,
                pwd=self.password,
                parent_dialog=self,
                server=get_formatted_server_id(self.server_ip,
                                               self.server_port))
            self.client_thread = Thread(
                target=lambda: self.client.mirror_dir_to_server(self.upload_folder)
            )
            self.client_thread.start()

    def run_dialog(self):
        self.title("Writing GUIs is hard, okay?")
        # self.geometry("500x250")

        server_ip_text = Label(self, text="Server IP", anchor="e")
        self.server_ip_input = Entry(self)
        self.server_ip_input.insert(END, settings.SERVER_IP)

        server_ip_text.grid(column=0, row=0)
        self.server_ip_input.grid(column=1, row=0)

        server_port_text = Label(self, text="Port", anchor="e")
        self.server_port_input = Entry(self)
        self.server_port_input.insert(END, settings.SERVER_PORT)

        server_port_text.grid(column=0, row=1)
        self.server_port_input.grid(column=1, row=1)

        # Creating the username & password entry boxes
        username_text = Label(self, text="Username", anchor="e")
        self.username_input = Entry(self)

        username_text.grid(column=0, row=2)
        self.username_input.grid(column=1, row=2)

        password_text = Label(self, text="Password", anchor="e")
        self.password_input = Entry(self, show="*")
        password_text.grid(column=0, row=3)
        self.password_input.grid(column=1, row=3)

        upload_folder_btn = Button(
            text="Upload folder", command=self.quit_dialog)
        choose_file_btn = Button(
            text="Choose folder", command=self.open_file)
        upload_folder_btn.grid(column=1, row=4)
        choose_file_btn.grid(column=0, row=4)

        self.progressbar = Progressbar(
            self, orient='horizontal', mode='determinate')
        self.progressbar.grid(column=0, row=5, columnspan=2)

        self.info_label = Label(self, text="", anchor="e")
        self.info_label.grid(column=0, row=6, columnspan=2)

        self.mainloop()

        return {
            "username": self.username,
            "password": self.password,
            "upload_folder": self.upload_folder,
            "ip": self.server_ip,
            "port": self.server_port
        }


if __name__ == '__main__':
    f = FileChooserDialog()
    f.run_dialog()
