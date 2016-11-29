#!/usr/bin/env python
from tkinter import Button, Label, Entry, Tk, messagebox, Scrollbar, RIGHT, Y, END, Text
from tkinter.ttk import Progressbar
from tkinter.filedialog import askdirectory
from threading import Thread

from client import Client
import settings


class FileChooserDialog(object):
    def __init__(self):
        self.root = Tk()
        self.upload_folder = ""
        self.username = ""
        self.password = ""

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
        self.root.title("Writing GUIs is hard, okay?")
        self.root.geometry("500x250")

        server_ip_text = Label(self.root, text="Server IP")
        self.server_ip_input = Entry(self.root)
        self.server_ip_input.insert(END, settings.SERVER_IP)

        server_port_text = Label(self.root, text="Port")
        self.server_port_input = Entry(self.root)
        self.server_port_input.insert(END, settings.SERVER_PORT)

        # Creating the username & password entry boxes
        username_text = Label(self.root, text="Username")
        self.username_input = Entry(self.root)
        password_text = Label(self.root, text="Password")
        self.password_input = Entry(self.root, show="*")

        self.info_label = Label(self.root, text="")

        upload_folder_btn = Button(
            text="Upload folder", command=self.quit_dialog)
        choose_file_btn = Button(
            text="Choose folder to upload", command=self.open_file)

        self.progressbar = Progressbar(
            self.root, orient='horizontal', mode='determinate')

        server_ip_text.pack()
        self.server_ip_input.pack()

        server_port_text.pack()
        self.server_port_input.pack()

        username_text.pack()
        self.username_input.pack()
        password_text.pack()
        self.password_input.pack()
        upload_folder_btn.pack()
        choose_file_btn.pack()

        self.progressbar.pack()
        self.info_label.pack()

        self.root.mainloop()

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
