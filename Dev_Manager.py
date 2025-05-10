import tkinter as tk
from resource_path import resource_path
from tkinter import filedialog
import os
import json
import mmap


def hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str.replace(' ', ''))

def find_hex_in_file(file_path, hex_values):
    found_positions = {}
    with open(file_path, 'rb') as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        for hex_value in hex_values:
            byte_seq = hex_to_bytes(hex_value)
            position = mmapped_file.find(byte_seq)
            if position != -1:
                found_positions[hex_value] = position
            else:
                found_positions[hex_value] = None
    return found_positions


def get_directory_from_file():
    try:
        with open("directory.feesh", "r") as file:
            directory = file.read().strip()
            if os.path.isdir(directory):
                return directory
            else:
                print("The directory path stored in 'directory.feesh' is invalid.")
                return None
    except FileNotFoundError:
        print("'directory.feesh' not found. Please provide the directory path")
        return None


def get_directory_from_user():
    root = tk.Tk()
    root.withdraw()

    directory = filedialog.askdirectory(title="Select Directory")
    if directory and os.path.isdir(directory):
        return directory
    else:
        print("The selected directory is invalid.")
        return None


directory = get_directory_from_file()
if directory is None:
    directory = get_directory_from_user()


if directory:
    with open("directory.feesh", "w") as file:
        file.write(directory)
else:
    print("No valid directory selected. Exiting.")

def update_offsets():
    pak20 = os.path.join(directory, 'pakchunk20-WindowsClient.ucas')

    airstrike_hex = ["9A 99 19 3F 9A 99 99 3D"]
    dev_pillar_hex = ["50 42 57 41 5F 4D 31 5F 41 72 63 68 77 61 79"]
    dev_wood_hex = ["50 42 57 41 5F 57 31 5F 41 72 63 68 77 61 79"]


    results = {}
    
    results_pak20_2 = find_hex_in_file(pak20, airstrike_hex)
    for hex_value, position in results_pak20_2.items():
        if position is not None:
                results["airstrike_offset"] = hex(position)[2:].upper()

    results_pak20_3 = find_hex_in_file(pak20, dev_pillar_hex)
    for hex_value, position in results_pak20_3.items():
        if position is not None:
            results["dev_pillar_offset"] = hex(position)[2:].upper()

    results_pak20_4 = find_hex_in_file(pak20, dev_wood_hex)
    for hex_value, position in results_pak20_4.items():
        if position is not None:
            results["dev_wood_offset"] = hex(position)[2:].upper()

    with open('offsets.feesh', 'w') as json_file:
        json.dump(results, json_file, indent=4)
    try:
        update_button.config(bg=button_on_color, text="Offsets Updated")
        create_close_window()
    except:
        pass


try:
    with open('offsets.feesh', "r") as json_file:
        offsets = json.load(json_file)
except (FileNotFoundError):
    with open('offsets.feesh', 'w') as file:
        file.write("")
        update_offsets()
    with open('offsets.feesh', "r") as json_file:
        offsets = json.load(json_file)

airstrike_offset = offsets.get("airstrike_offset")
dev_offset = offsets.get("dev_offset")
dev_pillar_offset = offsets.get("dev_pillar_offset")
dev_wood_offset = offsets.get("dev_wood_offset")

button_off_color = 'purple'
button_on_color = 'green'
text_color = 'white'

pillars = False
stairs = False
airStrike_140s = False
airStike_60s = False
seizure = False
wood_devs = False


pak20 = os.path.join(directory, 'pakchunk20-WindowsClient.ucas')

def write_bytes_to_offset(file_path, offset_hex, values):
    start_offset = int(offset_hex, 16)
    with open(file_path, 'r+b') as file:
        file.seek(start_offset)
        file.write(bytes(values))

def enable_pillar_devs(pak20):
    pillar_devs_sequence = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    write_bytes_to_offset(pak20, dev_pillar_offset, pillar_devs_sequence)
    print("Enabled Pillar Devs")
    

def disable_pillar_devs(pak20):
    pillar_devs_sequence = [0x50, 0x42, 0x57, 0x41, 0x5F, 0x4D, 0x31, 0x5F, 0x41, 0x72, 0x63, 0x68, 0x77, 0x61, 0x79]
    write_bytes_to_offset(pak20, dev_pillar_offset, pillar_devs_sequence)
    print("Disabled Pillar Devs")

def enable_airStrike_140s(pak20):
    airStrike_sequence = [0x00, 0x00, 0x0C, 0x43]
    write_bytes_to_offset(pak20, airstrike_offset, airStrike_sequence)
    print("Enabled AirStrike 140s")

def disable_airStrike_140s(pak20):
    airStrike_disable_sequence = [0x9A, 0x99, 0x19, 0x3F]
    write_bytes_to_offset(pak20, airstrike_offset, airStrike_disable_sequence)
    print("Disabled AirStrike 140s")

def enable_seizure(pak20):
    sequence = [
        0x00, 0x00, 0x0C, 0x43, 0x9A, 0x99, 0x99, 0x3D, 0xCD, 0xCC, 0xCC, 0x3E, 0x00, 0x07, 0x00, 0x05,
        0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x00, 0x05, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 
        0xCC, 0xCC, 0x00, 0x05, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x00, 0x07, 0x00, 0x05,
        0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x00, 0x05, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 
        0xCC, 0xCC, 0x00, 0x05, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC
    ]
    write_bytes_to_offset(pak20, airstrike_offset, sequence)
    print("Enabled Seizure Air Strike")

def disable_seizure(pak20):
    sequence = [
        0x9A, 0x99, 0x19, 0x3F, 0x9A, 0x99, 0x99, 0x3D, 0xCD, 0xCC, 0xCC, 0x3E, 0x00, 0x07, 0x00, 0x05,
        0x00, 0x00, 0xA0, 0x3F, 0x00, 0x00, 0xA0, 0x41, 0x00, 0x05, 0x12, 0x83, 0x20, 0x40, 0x00, 0x00,
        0x70, 0x41, 0x00, 0x05, 0x77, 0xBE, 0xFF, 0x3F, 0x00, 0x00, 0x00, 0x41, 0x00, 0x07, 0x00, 0x05,
        0x00, 0x00, 0xA0, 0x40, 0x00, 0x00, 0xC0, 0x40, 0x00, 0x05, 0x00, 0x00, 0x80, 0x40, 0x00, 0x00,
        0x70, 0x41, 0x00, 0x05, 0x00, 0x00, 0x00, 0x41, 0x00, 0x00, 0x40, 0x41
    ]
    write_bytes_to_offset(pak20, airstrike_offset, sequence)
    print("Disabled Seizure Air Strike")

def enable_wood_devs(pak20):
    sequence = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    write_bytes_to_offset(pak20, dev_wood_offset, sequence)
    print("Enabled Wood Devs")

def disable_wood_devs(pak20):
    sequence = [0x50, 0x42, 0x57, 0x41, 0x5F, 0x57, 0x31, 0x5F, 0x41, 0x72, 0x63, 0x68, 0x77, 0x61, 0x79]
    write_bytes_to_offset(pak20, dev_wood_offset, sequence)
    print("Disabled Wood Devs")

def enable_airstrike_60s(pak20):
    sequence = [0x00, 0x00, 0x74, 0x42]
    write_bytes_to_offset(pak20, airstrike_offset, sequence)
    print("Enabled AirStrike 60s")

def disable_airstrike_60s(pak20):
    sequence = [0x9A, 0x99, 0x19, 0x3F]
    write_bytes_to_offset(pak20, airstrike_offset, sequence)
    print("Disabled AirStrike 60s")

def toggle_pillar():
    global pillars
    if pillars == True:
        pillar_button.config(text='Dev Pillars ❌', bg=button_off_color)
        disable_pillar_devs(pak20)
        pillars = False
    else:
        pillar_button.config(text='Dev Pillars ✔️', bg=button_on_color)
        enable_pillar_devs(pak20)
        pillars = True

def toggle_airStrike_140s():
    global airStrike_140s
    if airStrike_140s == True:
        airStrike_140s_button.config(text='AirStrike 140s ❌', bg=button_off_color)
        disable_airStrike_140s(pak20)
        airStrike_140s = False
    else:
        airStrike_140s_button.config(text='AirStrike 140s ✔️', bg=button_on_color)
        enable_airStrike_140s(pak20)
        airStrike_140s = True

def toggle_seizure():
    global seizure
    if seizure == True:
        seizure_button.config(text='Seizure ❌', bg=button_off_color)
        disable_seizure(pak20)
        seizure = False
    else:
        seizure_button.config(text='Seizure ✔️', bg=button_on_color)
        enable_seizure(pak20)
        seizure = True

def toggle_wood_devs():
    global wood_devs
    if wood_devs == True:
        wood_dev_button.config(text="Wood Devs ❌", bg=button_off_color)
        disable_wood_devs(pak20)
        wood_devs = False
    else:
        wood_dev_button.config(text="Wood Devs ✔️", bg=button_on_color)
        enable_wood_devs(pak20)
        wood_devs = True
        

def reset_paks():
    global wood_devs, seizure, airStrike_140s, stairs, pillars, airStike_60s
    wood_devs = True
    seizure = True
    airStrike_140s = True
    stairs = True
    pillars = True
    airStike_60s = True
    toggle_airStrike_140s()
    toggle_airstrike_60s()
    toggle_pillar()
    toggle_seizure()
    toggle_wood_devs()
    print("Reset modified pakchunks")


def toggle_airstrike_60s():
    global airStike_60s
    if airStike_60s == True:
        airstrike_60s_button.config(text="AirStrike 60s ❌", bg=button_off_color)
        disable_airstrike_60s(pak20)
        airStike_60s = False
    else:
        airstrike_60s_button.config(text="AirStrike 60s ✔️", bg=button_on_color)
        enable_airstrike_60s(pak20)
        airStike_60s = True


def resize_background(event):
    width_scale = window_width / original_bg_image.width()
    height_scale = window_height / original_bg_image.height()
    
    scaled_width = int(original_bg_image.width() * min(width_scale, height_scale))
    scaled_height = int(original_bg_image.height() * min(width_scale, height_scale))
    
    global resized_background_image
    resized_background_image = original_bg_image.subsample(round(original_bg_image.width() / scaled_width), 
                                                          round(original_bg_image.height() / scaled_height))
    
    bg_label.config(image=resized_background_image)

root = tk.Tk()
root.title("DEV TOOLS")

window_width = 720
window_height = 512
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)
original_bg_image = tk.PhotoImage(file=resource_path("background.png"))
bg_label = tk.Label(root, image=original_bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


pillar_button = tk.Button(root, text="Dev Pillars ❌", bg=button_off_color, fg=text_color, width=12, command=toggle_pillar)
pillar_button.place(x=40, y=230)
airStrike_140s_button = tk.Button(root, text="AirStrike 140s ❌", bg=button_off_color, fg=text_color, width=12, command=toggle_airStrike_140s)
airStrike_140s_button.place(x=590, y=230)
airstrike_60s_button = tk.Button(root, text="AirStrike 60s ❌", bg=button_off_color, fg=text_color, width=12, command=toggle_airstrike_60s)
airstrike_60s_button.place(x=590, y=200)
seizure_button = tk.Button(root, text="Seizure ❌", bg=button_off_color, fg=text_color, width=12, command=toggle_seizure)
seizure_button.place(x=590, y=260)
wood_dev_button = tk.Button(root, text="Wood Devs ❌", bg=button_off_color, fg=text_color, width=12, command=toggle_wood_devs)
wood_dev_button.place(x=40, y=200)
update_button = tk.Button(root, text="Update Offsets", bg=button_off_color, fg=text_color, width=12, command=update_offsets)
update_button.place(x=590, y=100)
reset_paks_button = tk.Button(root, text="Disable All", bg=button_off_color, fg=text_color, width=12, command=reset_paks)
reset_paks_button.place(x=590, y=130)


credits = tk.Label(root, text="Developed by Chimkins", bg="black", fg="white", width=20)
credits.place(x=30, y=60)
dev_warning = tk.Label(root, text="Don't enable more than one option per side!", bg="black", fg='white', width=33)
dev_warning.place(x=30, y=30)

def create_close_window():
    close_window = tk.Toplevel()
    close_window.title("Close Program")
    
    def close_button_click():
        root.destroy()  # Close the new window
    
    close_button = tk.Button(
        close_window,
        text="Close",
        bg='gray',
        fg='white',
        command=close_button_click
    )
    
    close_message = tk.Label(close_window, text="Offsets updated! Please close and reopen the program!")
    close_message.pack()
    close_button.pack(pady=5)

    # Position the button in the center of the new window
    x_position = (close_message.width() - 100) // 2
    y_position = (close_message.height() - 50) // 2
    close_button.place(x=x_position, y=y_position)
    
    return close_window

root.bind("<Configure>", resize_background)

root.mainloop()

def main():
    pass

if __name__ == "__main__":
    main()