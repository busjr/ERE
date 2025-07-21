import io
import os
from os import name
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
        y = (screen_height - 485) // 2

        self.geometry(f"400x485+{x}+{y}")
        self._fg_color = "#1f1f1f"
        self.title(f"Keypy {__version__} (by busjr)")
        if name == "nt":
            ico_path = os.path.join(os.path.dirname(__file__), "icon.ico")
            self.iconbitmap(ico_path)
        self.icon_warning = os.path.join(os.path.dirname(__file__), "war.png")
        self.icon_que = os.path.join(os.path.dirname(__file__), "que.png")
        self.resizable(False, False)
        
        # create tabs
        tabview = ct.CTkTabview(
            master=self,
            width=400,
            height=485,
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
        self.path_entry_open = self.create_entry(
            tabview.tab("OPEN"),
            placeholder="The path to the file to open",
            handler=self.password_entry_open_handler,
            drop="yes")
        self.path_entry_open.place(x=0, y=0)
        
        self.batton_path_open = self.create_button(
            master=tabview.tab("OPEN"),
            text="PATH",
            width=40,
            height=30,
            command=self.path)
        self.batton_path_open.place(x=310, y=0)

        self.batton_context_open = self.create_button(
            master=tabview.tab("OPEN"),
            text="!",
            width=5,
            height=30,
            command=self.context_menu,
            tooltip="Enable context menu. (open file with admin administrator)")
        self.batton_context_open.place(x=360, y=0)

        self.password_entry_open = self.create_entry(
            master=tabview.tab("OPEN"),
            placeholder="Password",
            handler=self.path_entry_open_handler,
            show_password="*")
        self.password_entry_open.place(x=0, y=40)
        
        self.show_password_open = self.create_button(
            master=tabview.tab("OPEN"),
            text="()",
            command=lambda: self.toggle_password_visibility(self.password_entry_open),
            tooltip="Show/Hide",
            width=45,
            height=30)
        self.show_password_open.place(x=310, y=40)

        self.batton_context_del_open = self.create_button(
            master=tabview.tab("OPEN"), 
            text="!", 
            width=5, 
            height=30, 
            command=self.context_menu_delete, 
            tooltip="Disable context menu. (open file with admin administrator)")
        self.batton_context_del_open.place(x=360, y=40)

        self.box_open = self.create_textbox(tabview.tab("OPEN"))
        self.box_open.place(x=0, y=80)
        
        self.batton_ok_open = self.create_button(
            master=tabview.tab("OPEN"),
            text="Decrypt the file",
            width=380,
            height=35,
            command=self.decrypt_aes_file)
        self.batton_ok_open.place(x=0, y=390)
        

        # CREATE tabs

        self.box_create = self.create_textbox(tabview.tab("CREATE"))
        self.box_create.place(x=0, y=0)

        self.path_entry_create = self.create_entry(
            master=tabview.tab("CREATE"),
            placeholder="The path to the file to open",
            handler=self.entry_path_create_handler,
            drop="yes")
        self.path_entry_create.place(x=0, y=310)

        self.batton_path_create = self.create_button(
            master=tabview.tab("CREATE"),
            text="PATH",
            width=40,
            height=30,
            command=self.path_save)
        self.batton_path_create.place(x=310, y=310)

        self.password_entry_create = self.create_entry(
            master=tabview.tab("CREATE"),
            placeholder="Password",
            handler=self.entry_password_create_handler,
            show_password="*")
        self.password_entry_create.place(x=0, y=350)

        self.show_password_create = self.create_button(
            master=tabview.tab("CREATE"), 
            text="()", 
            width=45, 
            height=30, 
            command=lambda: self.toggle_password_visibility(self.password_entry_create), 
            tooltip="Show/Hide")
        self.show_password_create.place(x=310, y=350)

        self.batton_ok_create = self.create_button(
            master=tabview.tab("CREATE"),
            text="Encrypt the file",
            width=380,
            height=35,
            command=self.encrypt_aes_file)
        self.batton_ok_create.place(x=0, y=390)

    def toggle_password_visibility(self, target_button):
        if target_button.cget("show") == "":
            target_button.configure(show="*")
        else:
            target_button.configure(show="")

    def password_entry_open_handler(self, event):
        self.password_entry_open.focus()

    def path_entry_open_handler(self, event):
        self.path_entry_open.focus()

    def entry_path_create_handler(self, event):
        self.password_entry_create.focus()

    def entry_password_create_handler(self, event):
        self.path_entry_create.focus()

    def create_textbox(self, master):
        self.textbox = ct.CTkTextbox(
            master=master,
            width=300,
            height=300,
            fg_color="#181818",
            text_color="#696969",
            wrap="none",
        )
        self.textbox.bind("<Button-3>", lambda event: self.paste_text(event, target_entry=self.textbox))
        return self.textbox

    def create_button(self, master, text, width, height, command, tooltip=None,):
        self.button = ct.CTkButton(
            master=master,
            text=text,
            text_color="#696969" if text != "!" else "green",
            command=command,
            width=width,
            height=height,
            fg_color="#1d1e1e",
            hover_color="#2a2c2c",
            border_width=0
        )
        if tooltip:
            CTkToolTip(self.button, delay=0.5, message=tooltip)

        return self.button

    def create_entry(self, master, placeholder, handler, show_password=None, drop=None):
        self.entry = ct.CTkEntry(
            master=master,
            placeholder_text=placeholder,
            placeholder_text_color="#696969",
            text_color="#696969",
            show=show_password,
            width=300,
            height=30,
            fg_color="#1f1f1f",
            corner_radius=10,
            border_width=1,
        )
        self.entry.bind("<Button-3>", lambda event, target_entry=self.entry: self.paste_text(event, target_entry))
        self.entry.bind("<Return>", handler)
        if drop:
            self.entry.drop_target_register(DND_FILES)
            self.entry.dnd_bind('<<Drop>>', lambda event, target_entry=self.entry: self.drop(event, target_entry))
        return self.entry

    def path_program(self):
        if name == "nt":
            home_dir = os.path.expanduser("~")
            documents_dir = os.path.join(home_dir, "Documents")  # path to the target Documents
            dst_dir = os.path.join(documents_dir, "ERE")  # path to the target directory
            return dst_dir

    def context_menu_delete(self):
        if name == "nt":
            paths = [
                r"HKEY_CLASSES_ROOT\Directory\Background\shell\ERE",
                r"HKEY_CLASSES_ROOT\SystemFileAssociations\.aes\shell\OpenWithERE"
            ]

            for path in paths:
                subprocess.run(["reg", "delete", path, "/f"], check=True)

            shutil.rmtree(self.path_program()) # delete dir and file
        else:
            path = "/home/user/.local/share/nemo/actions/ERE.nemo_action"
            os.remove(path)

            shutil.rmtree("/home/user/ERE/EREGUI.bin") # delete dir and file

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

        if response == "Yes" and name == "nt":
            try:
                src = sys.argv[0]  # path to the source file
                dst_file = os.path.join(self.path_program(), os.path.basename(src))  # full path sourse file

                # dst_icon_file = dst_file.replace("ERE.exe", "icon.ico")
                command_open = f'"{dst_file}" "%1"'

                os.makedirs(self.path_program(), exist_ok=True) # create dir in "Documents"
                shutil.copy(src, dst_file)  # copy source file

                # create context_menu
                base_path = r"HKEY_CLASSES_ROOT\Directory\Background\shell"
                key_name = "ERE"
                command_key_path = f"{base_path}\\{key_name}\\command"

                # adds a default value "Open in ERE" to the specified registry key
                subprocess.run(["reg", "add", f"{base_path}\\{key_name}", "/ve", "/t", "REG_SZ", "/d", "Open in ERE", "/f"], check=True)

                # sets the default value of the command key to the path of the executable (dst_file)
                subprocess.run(["reg", "add", command_key_path, "/ve", "/t", "REG_SZ", "/d", dst_file, "/f"], check=True)

                # sets icon for .aes file
                # subprocess.run(["reg", "add", "HKEY_CLASSES_ROOT\.aes", "/ve", "/t", "REG_SZ", "/d", "", "/f"], check=True)
                # subprocess.run(["reg", "add", "HKEY_CLASSES_ROOT\.aes\DefaultIcon", "/ve", "/t", "REG_SZ", "/d", f"dst_icon_file", "/f"], check=True)

                # adds the default value "Open in ERE" at RMB to the specified registry key
                subprocess.run(["reg", "add", r"HKEY_CLASSES_ROOT\SystemFileAssociations\.aes\shell\OpenWithERE", "/ve", "/t", "REG_SZ", "/d", "Открыть с помощью ERE", "/f"], check=True)
                subprocess.run(["reg", "add", r"HKEY_CLASSES_ROOT\SystemFileAssociations\.aes\shell\OpenWithERE\command", "/ve", "/t", "REG_SZ", "/d", command_open, "/f"], check=True)


            except PermissionError:
                self.show_error(message="No permission to create directory. Run the script as administrator.")
                sys.exit(1)

        else:
            try:
                src = sys.argv[0]
                user_dir = "/home/user/"
                dst_dir = os.path.join(user_dir, "ERE")

                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy(src, dst_dir)

                # create context_menu
                actions_dir = "/home/user/.local/share/nemo/actions"

                # Создание директории actions если она не существует
                if not os.path.exists(actions_dir):
                    os.makedirs(actions_dir)

                action_file_path = os.path.join(actions_dir, 'ERE.nemo_action')

                action_content = f"""
[Nemo Action]
Name=Open ERE
Comment=ERE crypt/encrypt

Exec={dst_dir + "/EREGUI.bin"} %F

Selection=s

Extensions=any;
 """
                with open(action_file_path, 'w') as f:
                    f.write(action_content)
            except PermissionError:
                self.show_error(message="No permission to create directory. Run the script as administrator.")
                sys.exit(1)

    def drop(self, event, target_entry):
        if name == 'nt':
            file_path = event.data
            target_entry.delete(0, ct.END)
            target_entry.insert(0, file_path)
        else:
            file_path = event.data
            file_path = file_path.replace("{", "").replace("}", "")
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

            if name == "nt": # open floder
                dir_path = os.path.dirname(file_path) 
                os.startfile(dir_path)
            else:
                dir_path = os.path.abspath(file_path)
                subprocess.run(["xdg-open", dir_path])

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
