import io
import os
import customtkinter as ct
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox
from pyAesCrypt import encryptStream, decryptStream

__version__ = "v1.4"


class MyFrame(ct.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def label1(self, decrypted_data):
        label = ct.CTkLabel(self, text=decrypted_data)
        label.grid(row=0, column=0, padx=20)


class App(ct.CTk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - 400) // 2
        y = (screen_height - 435) // 2

        self.geometry(f"400x435+{x}+{y}")
        self._fg_color = "#1f1f1f"
        self.title(f"Keypy {__version__} (by busjr)")
        self.ico_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        self.iconbitmap(self.ico_path)
        self.icon_warning = os.path.join(os.path.dirname(__file__), 'war.png')
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
            anchor=ct.CENTER
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
            border_width=1
        )
        self.Entry_path.grid(padx=0, pady=5, row=0, column=0)

        self.button_path = ct.CTkButton(
            master=tabview.tab("OPEN"),
            text="PATH",
            text_color="#696969",
            command=self.path,
            width=50,
            height=30,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c"
        )
        self.button_path.grid(padx=5, pady=5, row=0, column=1)

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
            border_width=1
        )
        self.Entry_password.grid(padx=0, pady=5, row=1, column=0)

        self.button_password = ct.CTkButton(
            master=tabview.tab("OPEN"),
            command=self.decrypt_aes_file,
            text="OK",
            text_color="#696969",
            width=50,
            height=30,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c"
        )
        self.button_password.grid(padx=5, pady=5, row=1, column=1)

        # open text_box1

        self.text_box1 = ct.CTkTextbox(
            master=tabview.tab("OPEN"),
            width=300,
            height=300,
            fg_color="#181818",
            wrap="none"
        )
        self.text_box1.grid(padx=2, pady=2, row=2, column=0)

        # create text_box2

        self.text_box2 = ct.CTkTextbox(
            master=tabview.tab("CREATE"),
            width=300,
            height=300,
            fg_color="#181818",
            wrap="none"
        )
        self.text_box2.grid(padx=2, pady=2, row=0, column=0)

        # create Entry_path2

        self.Entry_path2 = ct.CTkEntry(
            master=tabview.tab("CREATE"),
            placeholder_text="The path to the file to open",
            placeholder_text_color="#696969",
            width=300,
            height=30,
            fg_color="#1f1f1f",
            corner_radius=10,
            border_width=1
        )
        self.Entry_path2.grid(padx=0, pady=5, row=1, column=0)

        self.button_path2 = ct.CTkButton(
            master=tabview.tab("CREATE"),
            text="PATH",
            text_color="#696969",
            command=self.path_save,
            width=50,
            height=30,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c"
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
            border_width=1
        )
        self.Entry_password2.grid(padx=0, pady=5, row=2, column=0)

        self.button_password2 = ct.CTkButton(
            master=tabview.tab("CREATE"),
            text="OK",
            text_color="#696969",
            command=self.encrypt_aes_file,
            width=50,
            height=30,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c"
        )
        self.button_password2.grid(padx=5, pady=5, row=2, column=1)

    def path(self):
        filename = filedialog.askopenfilename()
        self.Entry_path.delete(0, 'end')
        self.Entry_path.insert(0, filename)

    def path_save(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".aes",
            filetypes=[("AES files", "*.aes")]
        )
        self.Entry_path2.delete(0, 'end')
        self.Entry_path2.insert(0, file_path)

    def decrypt_aes_file(self):
        try:
            file_path = self.Entry_path.get()
            password = self.Entry_password.get()
            bufferSize = 64 * 1024

            with open(file_path, "rb") as fIn:
                fCiph = io.BytesIO(fIn.read())

            fCiph.seek(0)

            fDec = io.BytesIO()
            decryptStream(fCiph, fDec, password, bufferSize)

            decrypted_data = fDec.getvalue().decode('utf-8')
            self.text_box1.delete("1.0", "end")
            self.text_box1.insert("1.0", decrypted_data)
        except Exception:
            CTkMessagebox(
                title="Error",
                icon=self.icon_warning,
                option_1="Cancel",
                message="""
File not found or password is incorrect.
(Check the full path to the extension or check your password.
If nothing helps, open the program with administrator rights.)
                """,)

    def encrypt_aes_file(self):
        try:
            text = self.text_box2.get("1.0", "end-1c")
            file_path = self.Entry_path2.get()
            password = self.Entry_password2.get()
            bufferSize = 64 * 1024

            input_buffer = io.BytesIO(text.encode())
            with open(file_path, 'wb') as output_file:
                encryptStream(input_buffer, output_file, password, bufferSize)
            open_dir = os.path.dirname(file_path)
            os.startfile(open_dir)
        except Exception:
            CTkMessagebox(
                title="Error",
                icon=self.icon_warning,
                option_1="Cancel",
                message="""
File not found or password is incorrect.
(Check the full path to the extension or check your password.
If nothing helps, open the program with administrator rights.)
                """,)


if __name__ == "__main__":
    app = App()
    app.mainloop()