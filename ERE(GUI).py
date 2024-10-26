import io
import os
import sys
import subprocess
import hashlib
import customtkinter as ct
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox
from CTkToolTip import CTkToolTip
from pyAesCrypt import encryptStream, decryptStream
from tkinterdnd2 import DND_FILES, TkinterDnD

__version__ = "v0.6"


class MyFrame(ct.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def label1(self, decrypted_data):
        label = ct.CTkLabel(self, text=decrypted_data)
        label.grid(row=0, column=0, padx=20)


class App(ct.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - 400) // 2
        y = (screen_height - 435) // 2

        self.geometry(f"400x435+{x}+{y}")
        self._fg_color = "#1f1f1f"
        self.title(f"Keypy {__version__} (by busjr)")
        self.ico_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.iconbitmap(self.ico_path)
        self.icon_warning = os.path.join(os.path.dirname(__file__), "war.png")
        self.icon_que = os.path.join(os.path.dirname(__file__), "que.png")
        self.resizable(False, False)

        tabview = ct.CTkTabview(
            master=self,
            width=400,
            height=435,
            fg_color="#1f1f1f",
            segmented_button_fg_color="#2a2a2a",
            segmented_button_unselected_color="#2a2a2a",
            segmented_button_selected_hover_color="#1f1f1f",
            segmented_button_selected_color="#1f1f1f",
            segmented_button_unselected_hover_color="#2a2c2c",
            text_color="#707070",
            corner_radius=10,
            anchor=ct.CENTER,
        )
        tabview.pack(padx=0, pady=0)

        tabview.add("OPEN")
        tabview.add("CREATE")

        # open Entry_path

        self.Entry_path = ct.CTkEntry(
            master=tabview.tab("OPEN"),
            placeholder_text="The path to the file to open",
            placeholder_text_color="#696969",
            width=300,
            height=30,
            fg_color="#1f1f1f",
            corner_radius=10,
            border_width=1,
        )
        self.Entry_path.grid(padx=0, pady=5, row=0, column=0)
        self.Entry_path.bind("<Button-3>", lambda event: self.paste_text(event, who=self.Entry_path))
        self.Entry_path.bind("<Return>", lambda event: self.Entry_password.focus())
        self.Entry_path.drop_target_register(DND_FILES)
        self.Entry_path.dnd_bind('<<Drop>>', lambda event: self.drop(event, who=self.Entry_path))

        self.button_path = ct.CTkButton(
            master=tabview.tab("OPEN"),
            text="PATH",
            text_color="#696969",
            command=self.path,
            width=50,
            height=30,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c",
        )
        self.button_path.grid(padx=5, pady=5, row=0, column=1)

        self.button_menu = ct.CTkButton(
            master=tabview.tab("OPEN"),
            text="!",
            text_color="green",
            command=self.menu,
            width=5,
            height=5,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c",
        )
        self.button_menu.grid(padx=5, pady=2, row=0, column=2)
        CTkToolTip(self.button_menu, delay=0.5, message="Enable context menu")

        # open Entry_password

        self.Entry_password = ct.CTkEntry(
            master=tabview.tab("OPEN"),
            placeholder_text="Password",
            placeholder_text_color="#696969",
            show="*",
            width=300,
            height=30,
            fg_color="#1f1f1f",
            corner_radius=10,
            border_width=1,
        )
        self.Entry_password.grid(padx=0, pady=5, row=1, column=0)
        self.Entry_password.bind("<Button-3>", lambda event: self.paste_text(event, who=self.Entry_password))
        self.Entry_password.bind("<Return>", lambda event: self.Entry_path.focus())

        self.button_password = ct.CTkButton(
            master=tabview.tab("OPEN"),
            command=self.decrypt_aes_file,
            text="OK",
            text_color="#696969",
            width=50,
            height=30,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c",
        )
        self.button_password.grid(padx=5, pady=5, row=1, column=1)

        self.button_menu_delete = ct.CTkButton(
            master=tabview.tab("OPEN"),
            text="!",
            text_color="green",
            command=self.menu_delete,
            width=5,
            height=5,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c",
        )
        self.button_menu_delete.grid(padx=5, pady=2, row=1, column=2)
        CTkToolTip(self.button_menu_delete,
                   delay=0.5, message="Disable context menu")

        # open text_box1

        self.text_box1 = ct.CTkTextbox(
            master=tabview.tab("OPEN"),
            width=300,
            height=300,
            fg_color="#181818",
            wrap="none",
        )
        self.text_box1.grid(padx=2, pady=2, row=2, column=0)
        self.text_box1.bind("<Button-3>", lambda event: self.paste_text(event, who=self.text_box1))

        # create text_box2

        self.text_box2 = ct.CTkTextbox(
            master=tabview.tab("CREATE"),
            width=300,
            height=300,
            fg_color="#181818",
            wrap="none",
        )
        self.text_box2.grid(padx=2, pady=2, row=0, column=0)
        self.text_box2.bind("<Button-3>", lambda event: self.paste_text(event, who=self.text_box2))

        # create Entry_path2

        self.Entry_path2 = ct.CTkEntry(
            master=tabview.tab("CREATE"),
            placeholder_text="The path to the file to open",
            placeholder_text_color="#696969",
            width=300,
            height=30,
            fg_color="#1f1f1f",
            corner_radius=10,
            border_width=1,
        )
        self.Entry_path2.grid(padx=0, pady=5, row=1, column=0)
        self.Entry_path2.bind("<Button-3>", lambda event: self.paste_text(event, who=self.Entry_path2))
        self.Entry_path2.bind("<Return>", lambda event: self.Entry_password2.focus())

        self.button_path2 = ct.CTkButton(
            master=tabview.tab("CREATE"),
            text="PATH",
            text_color="#696969",
            command=self.path_save,
            width=50,
            height=30,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c",
        )
        self.button_path2.grid(padx=5, pady=5, row=1, column=1)

        # create Entry_password2

        self.Entry_password2 = ct.CTkEntry(
            master=tabview.tab("CREATE"),
            placeholder_text="Password",
            placeholder_text_color="#696969",
            show="*",
            width=300,
            height=30,
            fg_color="#1f1f1f",
            corner_radius=10,
            border_width=1,
        )
        self.Entry_password2.grid(padx=0, pady=5, row=2, column=0)
        self.Entry_password2.bind("<Button-3>", lambda event: self.paste_text(event, who=self.Entry_password2))
        self.Entry_password2.bind("<Return>", lambda event: self.Entry_path2.focus())

        self.button_password2 = ct.CTkButton(
            master=tabview.tab("CREATE"),
            text="OK",
            text_color="#696969",
            command=self.encrypt_aes_file,
            width=50,
            height=30,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c",
        )
        self.button_password2.grid(padx=5, pady=5, row=2, column=1)

        # message

    def menu_delete(self):
        path = r"HKEY_CLASSES_ROOT\Directory\Background\shell\ERE"
        command = ["reg", "delete", path, "/f"]
        subprocess.run(command, check=True)

    def menu(self):
        message = CTkMessagebox(
            title="Info",
            title_color="#696969",
            icon=self.icon_que,
            option_1="Cancel",
            option_2="No",
            option_3="Yes",
            text_color="#696969",
            button_text_color="#696969",
            button_color="#1d1e1e",
            button_hover_color="#2a2c2c",
            fg_color="#1f1f1f",
            bg_color="#1f1f1f",
            message="""
If you want to enable the context menu, click "Yes"
(When moving .exe file, click here again").
            """,
        )

        response = message.get()

        if response == "Yes":
            script_path = sys.argv[0]
            base_path = r"HKEY_CLASSES_ROOT\Directory\Background\shell"
            key_name = "ERE"
            command_key_path = f"{base_path}\\{key_name}\\command"
            subprocess.run(
                [
                    "reg",
                    "add",
                    f"{base_path}\\{key_name}",
                    "/ve",
                    "/t",
                    "REG_SZ",
                    "/d",
                    "Open in ERE",
                    "/f",
                ],
                check=True,
            )
            subprocess.run(
                [
                    "reg",
                    "add",
                    command_key_path,
                    "/ve",
                    "/t",
                    "REG_SZ",
                    "/d",
                    script_path,
                    "/f",
                ],
                check=True,
            )

    def drop(self, event, who):
        file_path = event.data
        who.delete(0, ct.END)
        who.insert(0, file_path)

    def paste_text(self, event, who):
        text = self.clipboard_get()
        who.insert(ct.END, text)

    def path(self):
        filename = filedialog.askopenfilename()
        self.Entry_path.delete(0, "end")
        self.Entry_path.insert(0, filename)

    def path_save(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".aes", filetypes=[("AES files", "*.aes")]
        )
        self.Entry_path2.delete(0, "end")
        self.Entry_path2.insert(0, file_path)

    def decrypt_aes_file(self):
        try:
            file_path = self.Entry_path.get()
            password = self.Entry_password.get()
            bufferSize = 64 * 1024

            hpassword = hashlib.sha256(password.encode()).hexdigest()

            with open(file_path, "rb") as fIn:
                fCiph = io.BytesIO(fIn.read())

            fCiph.seek(0)

            fDec = io.BytesIO()
            decryptStream(fCiph, fDec, hpassword, bufferSize)

            decrypted_data = fDec.getvalue().decode("utf-8")

            del password, hpassword
            self.Entry_password.delete(0, ct.END)
            self.text_box1.delete("1.0", "end")
            self.text_box1.insert("1.0", decrypted_data)
        except Exception:
            CTkMessagebox(
                title="Error",
                title_color="#696969",
                icon=self.icon_warning,
                option_1="Cancel",
                text_color="#696969",
                button_text_color="#696969",
                button_color="#1d1e1e",
                button_hover_color="#2a2c2c",
                fg_color="#1f1f1f",
                bg_color="#1f1f1f",
                message="""
File not found or password is incorrect.
(Check the full path to the extension or check your password.
If nothing helps, open the program with administrator rights.)
                """,
            )

    def encrypt_aes_file(self):
        try:
            text = self.text_box2.get("1.0", "end-1c")
            file_path = self.Entry_path2.get()
            password = self.Entry_password2.get()
            bufferSize = 64 * 1024

            hpassword = hashlib.sha256(password.encode()).hexdigest()

            input_buffer = io.BytesIO(text.encode())

            with open(file_path, "wb") as output_file:
                encryptStream(input_buffer, output_file, hpassword, bufferSize)

            del password, hpassword

            open_dir = os.path.dirname(file_path)
            os.startfile(open_dir)
        except Exception:
            CTkMessagebox(
                title="Error",
                title_color="#696969",
                icon=self.icon_warning,
                option_1="Cancel",
                text_color="#696969",
                button_text_color="#696969",
                button_color="#1d1e1e",
                button_hover_color="#2a2c2c",
                fg_color="#1f1f1f",
                bg_color="#1f1f1f",
                message="""
File not found or password is incorrect.
(Check the full path to the extension or check your password.
If nothing helps, open the program with administrator rights.)
                """,
            )


if __name__ == "__main__":
    app = App()
    app.mainloop()
