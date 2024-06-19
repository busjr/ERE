import dearpygui.dearpygui as dpg
import pyAesCrypt

_version_ = "0.3"

dpg.create_context()

with dpg.window(tag="Primary Window"):

    t = dpg.add_text("(?)", color=[0, 255, 0], pos=(5, 20))
    with dpg.tooltip(t):
        dpg.add_text("Use only Latin symbols")
    dir_input_encrypt = dpg.add_input_text(hint="Path file for encrypt", pos=(30, 20), width=180)
    dpg.add_button(label="OK", pos=(230, 20), width=40, callback=lambda: Clear_encrypt())

    dir_input_decrypt = dpg.add_input_text(hint="Path file for decrypt", pos=(30, 50), width=180)
    dpg.add_button(label="OK", pos=(230, 50), width=40, callback=lambda: Clear_decrypt())

    Password_input = dpg.add_input_text(hint="Password", pos=(30, 80), width=180, password=True)
    dpg.add_button(label="Clear", pos=(230, 80), width=40, callback=lambda: Clear())

    dpg.add_progress_bar(label="Progress Bar", tag="progress_bar", pos=(30, 110), width=240)

    def Encrypt_Ere(dir): 
        password = str(Password_input)
        pyAesCrypt.encryptFile(str(dir), str(dir) + ".aes", password)
        dpg.set_value("progress_bar", 1)
        dpg.set_value("progress_bar", 0)



    def Decipher_Ere(dir):
        password = str(Password_input)
        pyAesCrypt.decryptFile(str(dir), str(dir) + "dataout.txt", password)
        dpg.set_value("progress_bar", 1)
        dpg.set_value("progress_bar", 0)

    def Clear_encrypt():
        dpg.set_value("progress_bar", 0.5)
        dir = str(dpg.get_value(dir_input_encrypt))
        dir.replace("/", "\\")
        Encrypt_Ere(dir)
        

    def Clear_decrypt():
        dpg.set_value("progress_bar", 0.5)
        dir = str(dpg.get_value(dir_input_decrypt))
        dir.replace("/", "\\")
        Decipher_Ere(dir)

    def Clear():
        dpg.set_value(dir_input_encrypt, "")
        dpg.set_value(dir_input_decrypt, "")
        dpg.set_value(Password_input, "")
        dpg.set_value("progress_bar", 0)



dpg.create_viewport(title=f'ERE {_version_} (by busjr)', width=310, height=200)
dpg.set_viewport_small_icon("icon.ico")
dpg.set_viewport_large_icon("icon.ico")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()