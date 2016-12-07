#!/usr/bin/env python

from tkinter import Button, Label, Entry, Tk, messagebox, Scrollbar, RIGHT, Y, END, Text, X, W, E, N, S
from tkinter.ttk import Progressbar, LabelFrame, Frame
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
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def open_file(self):
        self.upload_folder = askdirectory(title="Choose a folder.")
        self.set_folder_label(self.upload_folder)

    def set_folder_label(self, s):
        if s == "":
            self.folder_label["text"] = "No folder selected"
        else:
            self.folder_label["text"] = "Currently selected: " + s

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
        self.title("Backup Management System")
        # self.geometry("500x250")

        self.server_frame = LabelFrame(self, text="Server options")
        self.server_frame.grid(column=0, row=0, padx=10, pady=10)

        self.server_ip_text = Label(
            self.server_frame, text="Server IP", anchor="e")
        self.server_ip_text.grid(column=0, row=0, padx=5, pady=5)

        self.server_ip_input = Entry(self.server_frame)
        self.server_ip_input.insert(END, settings.SERVER_IP)
        self.server_ip_input.grid(column=1, row=0, padx=5, pady=5)

        self.server_port_text = Label(
            self.server_frame, text="Port", anchor="e")
        self.server_port_text.grid(column=0, row=1, padx=5, pady=5)

        self.server_port_input = Entry(self.server_frame)
        self.server_port_input.insert(END, settings.SERVER_PORT)
        self.server_port_input.grid(column=1, row=1, padx=5, pady=5)

        self.server_info = Label(
            self.server_frame,
            text=("Please do not change this information unless asked to.\n"
                  "Doing so may lead to inability to back up your work."))
        self.server_info.grid(column=0, row=2, columnspan=2, padx=5, pady=5)

        # Creating the username & password entry boxes

        self.creds_frame = LabelFrame(self, text="Login credentials")
        self.creds_frame.grid(column=1, row=0, padx=10, pady=10)

        self.username_text = Label(
            self.creds_frame, text="Username", anchor="e")
        self.username_input = Entry(self.creds_frame)

        self.username_text.grid(column=0, row=0, padx=5, pady=5)
        self.username_input.grid(column=1, row=0, padx=5, pady=5)

        self.password_text = Label(
            self.creds_frame, text="Password", anchor="e")
        self.password_input = Entry(self.creds_frame, show="*")

        self.password_text.grid(column=0, row=1, padx=5, pady=5)
        self.password_input.grid(column=1, row=1, padx=5, pady=5)

        self.creds_info = Label(
            self.creds_frame,
            text=("The password used on first login is stored permanently.\n"
                  "Do not forget your password."))
        self.creds_info.grid(column=0, row=2, columnspan=2, padx=5, pady=5)

        # ----------------
        # Upload buttons
        # ----------------

        self.btn_frame = LabelFrame(self, text="Select folder")
        self.btn_frame.grid(
            column=0, row=1, columnspan=2, padx=10, pady=10, sticky=E + W)

        self.btn_frame.grid_columnconfigure(0, weight=1, pad=5)
        self.btn_frame.grid_columnconfigure(2, pad=5)
        self.btn_frame.grid_rowconfigure(0, pad=10)

        self.folder_label = Label(self.btn_frame)
        self.folder_label.grid(row=0, padx=5, pady=5, sticky=E + W)
        self.set_folder_label("")

        self.choose_file_btn = Button(
            self.btn_frame,
            text="Choose folder to upload",
            command=self.open_file)
        self.choose_file_btn.grid(column=1, row=0)

        self.upload_folder_btn = Button(
            self.btn_frame, text="Start upload", command=self.quit_dialog)
        self.upload_folder_btn.grid(column=2, row=0)

        # --------------------------
        # Upload frame
        # --------------------------

        self.upload_frame = LabelFrame(self, text="Upload progress")
        self.upload_frame.grid(
            column=0, row=2, columnspan=2, padx=10, pady=10, sticky=E + W)
        self.upload_frame.grid_columnconfigure(0, weight=1)

        self.progressbar = Progressbar(
            self.upload_frame, orient='horizontal', mode='determinate')
        self.progressbar.grid(row=0, padx=5, pady=5, sticky=E + W)

        self.info_label = Label(
            self.upload_frame,
            text="When you upload a folder, upload progress will be shown here."
        )
        self.info_label.grid(row=1, padx=5, pady=5, sticky=E + W)

        self.mainloop()

        try:
            return {
                "username": self.username,
                "password": self.password,
                "upload_folder": self.upload_folder,
                "ip": self.server_ip,
                "port": self.server_port
            }
        except AttributeError:
            return None


if __name__ == '__main__':
    f = FileChooserDialog()
    f.run_dialog()
