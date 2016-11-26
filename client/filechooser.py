from tkinter import Button, Label, Entry, Tk, messagebox
from tkinter.filedialog import askdirectory

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
            self.client = Client(uid=self.username, pwd=self.password)
            self.client.mirror_dir_to_server(self.upload_folder)
            self.root.destroy()

    def run_dialog(self):
        self.root.title("ects")

        # Creating the username & password entry boxes
        username_text = Label(self.root, text="Username")
        self.username_input = Entry(self.root)
        password_text = Label(self.root, text="Password")
        self.password_input = Entry(self.root, show="*")

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

        self.root.mainloop()

        return {
            "username": self.username,
            "password": self.password,
            "upload_folder": self.upload_folder
        }
