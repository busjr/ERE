import io
import os
import sys
import subprocess
import hashlib
import shutil
import customtkinter as ct
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox
from CTkToolTip import CTkToolTip
from pyAesCrypt import encryptStream, decryptStream
from tkinterdnd2 import DND_FILES, TkinterDnD

__version__ = "v0.7"


class MyFrame(ct.CTkScrollableFrame):
    """
    Allows CTkScrollableFrame to be executed in CTkTextbox
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def widgets(self, decrypted_data):
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
        ico_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.iconbitmap(ico_path)
        self.icon_warning = os.path.join(os.path.dirname(__file__), "war.png")
        self.icon_que = os.path.join(os.path.dirname(__file__), "que.png")
        self.resizable(False, False)

        # create tabs
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

        # OPEN tabs
        self.path_entry_open = self.create_entry(tabview.tab("OPEN"), placeholder="The path to the file to open", handler=self.password_entry_open_handler, row=0)
        self.batton_path_open = self.create_batton(tabview.tab("OPEN"), "PATH", self.path, 0, 1)
        self.batton_context_open = self.create_batton(tabview.tab("OPEN"), "!", self.context_menu, 0, 2, tooltip="Enable context menu. (open file with admin administrator)")

        self.password_entry_open = self.create_entry(master=tabview.tab("OPEN"), placeholder="Password", handler=self.path_entry_open_handler, row=1, show_password="*")
        self.batton_ok_open = self.create_batton(tabview.tab("OPEN"), "OK", self.decrypt_aes_file, 1, 1)
        self.batton_context_del_open = self.create_batton(tabview.tab("OPEN"), "!", self.context_menu_delete, 1, 2, tooltip="Disable context menu. (open file with admin administrator)",)

        self.box_open = self.create_textbox(tabview.tab("OPEN"), 2)

        # CREATE tabs
        self.path_entry_create = self.create_entry(master=tabview.tab("CREATE"), placeholder="The path to the file to open", handler=self.entry_path_create_handler, row=1)
        self.batton_path_create = self.create_batton(tabview.tab("CREATE"), "PATH", self.path_save, 1, 1)

        self.password_entry_create = self.create_entry(master=tabview.tab("CREATE"), placeholder="Password", handler=self.entry_password_create_handler, row=2, show_password="*")
        self.batton_ok_create = self.create_batton(tabview.tab("CREATE"), "OK", self.encrypt_aes_file, 2, 1)

        self.box_create = self.create_textbox(tabview.tab("CREATE"), 0)

    def password_entry_open_handler(self, event):
        self.password_entry_open.focus()

    def path_entry_open_handler(self, event):
        self.path_entry_open.focus()

    def entry_path_create_handler(self, event):
        self.password_entry_create.focus()

    def entry_password_create_handler(self, event):
        self.path_entry_create.focus()

    def create_textbox(self, master, row):
        self.textbox = ct.CTkTextbox(
            master=master,
            width=300,
            height=300,
            fg_color="#181818",
            wrap="none",
        )
        self.textbox.grid(padx=2, pady=2, row=row, column=0)
        self.textbox.bind("<Button-3>", lambda event: self.paste_text(event, target_entry=self.textbox))
        return self.textbox


    def create_batton(self, master, text, command, row, column, tooltip=None):
        self.button = ct.CTkButton(
            master=master,
            text=text,
            text_color="#696969" if text != "!" else "green",
            command=command,
            width=50 if text != "!" else 5,
            height=30 if text != "!" else 5,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c",
        )
        self.button.grid(padx=5, pady=5 if text != "!" else 2, row=row, column=column)
        if tooltip:
            CTkToolTip(self.button, delay=0.5, message=tooltip)
        return self.button

    def create_entry(self, master, placeholder, handler, row, show_password=None):
        self.entry = ct.CTkEntry(
            master=master,
            placeholder_text=placeholder,
            placeholder_text_color="#696969",
            show=show_password,
            width=300,
            height=30,
            fg_color="#1f1f1f",
            corner_radius=10,
            border_width=1,
        )
        self.entry.grid(padx=0, pady=5, row=row, column=0)
        self.entry.bind("<Button-3>", lambda event, target_entry=self.entry: self.paste_text(event, target_entry))
        self.entry.bind("<Return>", handler)
        if row == 0:
            self.entry.drop_target_register(DND_FILES)
            self.entry.dnd_bind('<<Drop>>', lambda event, target_entry=self.entry: self.drop(event, target_entry))
        return self.entry

    def path_program(self):
        home_dir = os.path.expanduser("~")
        documents_dir = os.path.join(home_dir, "Documents")  # path to the target Documents
        dst_dir = os.path.join(documents_dir, "ERE")  # path to the target directory
        return dst_dir

    def context_menu_delete(self):
        path = r"HKEY_CLASSES_ROOT\Directory\Background\shell\ERE"
        command = ["reg", "delete", path, "/f"]
        subprocess.run(command, check=True)

        # delete dir and file
        shutil.rmtree(self.path_program())

    def context_menu(self):
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
            src = sys.argv[0]  # path to the source file
            dst_file = os.path.join(self.path_program(), os.path.basename(src))  # full path sourse file

            # create dir in "Documents"
            try:
                os.makedirs(self.path_program(), exist_ok=True)
            except PermissionError:
                self.show_error(message="""
No permission to create directory. Run the script as administrator.
""")
                sys.exit(1)

            # copy source file
            try:
                shutil.copy(src, dst_file)
            except PermissionError:
                self.show_error(message="""
No permission to create directory. Run the script as administrator.
""")
                sys.exit(1)

            # create context_menu
            base_path = r"HKEY_CLASSES_ROOT\Directory\Background\shell"
            key_name = "ERE"
            command_key_path = f"{base_path}\\{key_name}\\command"
            # adds a default value "Open in ERE" to the specified registry key
            subprocess.run(["reg", "add", f"{base_path}\\{key_name}", "/ve", "/t", "REG_SZ", "/d", "Open in ERE", "/f"], check=True)
            # sets the default value of the command key to the path of the executable (dst_file)
            subprocess.run(["reg", "add", command_key_path, "/ve", "/t", "REG_SZ", "/d", dst_file, "/f"], check=True)

    def drop(self, event, target_entry):
        file_path = event.data
        target_entry.delete(0, ct.END)
        target_entry.insert(0, file_path)

    def paste_text(self, event, target_entry):
        text = self.clipboard_get()
        target_entry.insert(ct.END, text)

    def path(self):
        filename = filedialog.askopenfilename()
        self.path_entry_open.delete(0, "end")
        self.path_entry_open.insert(0, filename)

    def path_save(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".aes", filetypes=[("AES files", "*.aes")]
        )
        self.path_entry_create.delete(0, "end")
        self.path_entry_create.insert(0, file_path)

    def decrypt_aes_file(self):
        """
        Decrypt an AES encrypted file.
        DOC: https://github.com/marcobellaccini/pyAesCrypt
        """

        try:
            file_path = self.path_entry_open.get()
            password = self.password_entry_open.get()
            bufferSize = 64 * 1024

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            with open(file_path, "rb") as fIn:
                fCiph = io.BytesIO(fIn.read())

            try:
                fDec = io.BytesIO()
                decryptStream(fCiph, fDec, hashed_password, bufferSize)
                decrypted_data = fDec.getvalue().decode("utf-8")
            except Exception:
                fCiph.seek(0)
                fDec = io.BytesIO()
                decryptStream(fCiph, fDec, password, bufferSize)
                decrypted_data = fDec.getvalue().decode("utf-8")

            del password, hashed_password
            self.password_entry_open.delete(0, ct.END)
            self.box_open.delete("1.0", "end")
            self.box_open.insert("1.0", decrypted_data)
        except FileNotFoundError:
            self.show_error(f"Error: File not found at {file_path}")
        except PermissionError:
            self.show_error(f"Error: Permission denied. Unable to read {file_path}")
        except ValueError as e:
            self.show_error(f"Error: Value error {str(e)}")
        except UnicodeDecodeError:
            self.show_error("Error: Unable to decode the decrypted data. The file might not be a text file.")
        except Exception as e:
            self.show_error(f"An unexpected error occurred: {str(e)}")

    def encrypt_aes_file(self):
        """
        Encrypt a file using AES encryption.
        DOC: https://github.com/marcobellaccini/pyAesCrypt
        """

        try:
            text = self.box_create.get("1.0", "end-1c")
            file_path = self.path_entry_create.get()
            password = self.password_entry_create.get()
            bufferSize = 64 * 1024

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            input_buffer = io.BytesIO(text.encode())

            with open(file_path, "wb") as output_file:
                encryptStream(input_buffer, output_file, hashed_password, bufferSize)

            del password, hashed_password

            open_dir = os.path.dirname(file_path)
            os.startfile(open_dir)
        except FileNotFoundError:
            self.show_error(f"Error: Unable to create or access the file at {file_path}")
        except PermissionError:
            self.show_error(f"Error: Permission denied. Unable to write to {file_path}")
        except IOError as e:
            self.show_error(f"Error: An I/O error occurred: {str(e)}")
        except Exception as e:
            self.show_error(f"An unexpected error occurred: {str(e)}")

    def show_error(self, message):
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
            message=message
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
