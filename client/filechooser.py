#!/usr/bin/env python
from tkinter import Button, Label, Entry, Tk, messagebox, Scrollbar, RIGHT, LEFT, Text, Y, END
from tkinter.filedialog import askdirectory
from threading import Thread

from client import Client


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
        self.T.insert(END, s + "\n")

    def quit_dialog(self):
        self.username = self.username_input.get()
        self.password = self.password_input.get()

        if not self.username:
            messagebox.showinfo("Error", "Please enter a username.")

        elif not self.password:
            messagebox.showinfo("Error", "Please enter a password.")

        elif not self.upload_folder:
            messagebox.showinfo("Error", "Please enter a folder to upload.")

        else:
            self.client = Client(
                uid=self.username, pwd=self.password, parent_dialog=self)
            self.client_thread = Thread(
                target=lambda: self.client.mirror_dir_to_server(self.upload_folder)
            )
            self.client_thread.start()

    def run_dialog(self):
        self.root.title("ects")
        self.root.geometry("500x250")

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

        username_text.pack()
        self.username_input.pack()
        password_text.pack()
        self.password_input.pack()
        upload_folder_btn.pack()
        choose_file_btn.pack()

        S = Scrollbar(self.root)
        self.T = Text(self.root, width=50)
        S.pack(side=RIGHT, fill=Y)
        self.T.pack(fill=Y)
        S.config(command=self.T.yview)
        self.T.config(yscrollcommand=S.set)

        self.root.mainloop()

        return {
            "username": self.username,
            "password": self.password,
            "upload_folder": self.upload_folder
        }


if __name__ == '__main__':
    f = FileChooserDialog()
    f.run_dialog()
