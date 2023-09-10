# EasyEdit Configurator for config.ini.
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
### Load Input box Values

    host.insert(0, config.get("websocket_settings", "host"))
    port.insert(0, config.get("websocket_settings", "port"))
    password.insert(0, config.get("websocket_settings", "password"))
    stream_server.insert(0, config.get("stream_settings", "streamserver"))
    stream_key.insert(0, config.get("stream_settings", "streamkey"))

### Load Radio Values    
    radio_rec_value = config.get("output_options", "output_record")
    if radio_rec_value == "True":
        radio_rec_var.set(1)
    else:
        radio_rec_var.set(2)

    radio_stream_value = config.get("output_options", "output_stream")
    if radio_stream_value == "True":
        radio_stream_var.set(1)
    else:
        radio_stream_var.set(2)

### Load Slider Values
    hours_slider_value = config.getint("run_time", "hours")
    hours_slider.set(hours_slider_value)

    mins_slider_value = config.getint("run_time", "mins")
    mins_slider.set(mins_slider_value)

    hold_slider_value = config.getint("run_time", "hold_time")
    hold_slider.set(hold_slider_value)

def save_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
### Save Input Box Values
    config["websocket_settings"]["host"] = host.get()
    config["websocket_settings"]["port"] = port.get()
    config["websocket_settings"]["password"] = password.get()
    config["stream_settings"]["streamserver"] = stream_server.get()
    config["stream_settings"]["streamkey"] = stream_key.get()
### Save Radio Values
    if radio_rec_var.get() == 1:
        config["output_options"]["output_record"] = "True"
    else:
        config["output_options"]["output_record"] = "False"
    
    if radio_stream_var.get() == 1:
        config["output_options"]["output_stream"] = "True"
    else:
        config["output_options"]["output_stream"] = "False"

### Save Slider values
    config["run_time"]["hours"]=str(hours_slider.get())
    config["run_time"]["mins"]=str(mins_slider.get())
    config["run_time"]["hold_time"]=str(hold_slider.get())


### Save all the info to config file
    with open("config.ini", "w") as config_file:
        config.write(config_file)

    
    messagebox.showinfo("Info", "Saved Successfully")

def clear_form():
    host.delete(0, tk.END)
    port.delete(0, tk.END)
    password.delete(0, tk.END)
    stream_server.delete(0, tk.END)
    stream_key.delete(0, tk.END)
    

    radio_rec_var.set("")
    radio_stream_var.set("")
    mins_slider.set(0)
    hours_slider.set(2)
    hold_slider.set(5)

def clear_and_load():
    clear_form()
    load_config()   

def toggle_password_visibility():
    if password_visibility.get() == 1:
        password.config(show="")
    else:
        password.config(show="*")
   

# Set font, window size, and padding variables
font = ("Poppins", 12)
header_font = ("Helvetica", 14, "bold")
window_size = (470, 850)
padding = 10
paddx = 5
paddy= 10
header_pad = 5
custom_style_dark = {"background": "#333", "foreground": "#fff"}
custom_style_white =  {"background": "#fff", "foreground": "#000"}

custom_style=custom_style_dark
if custom_style==custom_style_white:
    bagk="#ffffff"
else:
    bagk="#333"


# Create the window and set its title and size
root = tk.Tk()
#root.iconbitmap("obs.ico") - add icon here
root.configure(bg=bagk)
root.title("OBS Configurator")
root.geometry("{}x{}".format(*window_size))

# Read the config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

t_width=60

# Section Header: Websocket Settings 
section_label = tk.Label(root, text="WebSocket Settings", font=header_font, **custom_style)
section_label.grid(row=1, column=0, columnspan=3, padx=header_pad, pady=header_pad+1, sticky="w")


# Textbox Host IP
host_label = tk.Label(root, text="  OBS Host IP : ", font=font, **custom_style)
host_label.grid(row=2, column=0, padx=padding, pady=padding, sticky="w")
host = tk.Entry(root, font=font, **custom_style)
host.grid(row=2, column=1, padx=padding, pady=padding, sticky="w")

# Textbox Port
port_label = tk.Label(root, text="  OBS WS Port : ", font=font, **custom_style)
port_label.grid(row=3, column=0, padx=padding, pady=padding, sticky="w")
port = tk.Entry(root, font=font, **custom_style)
port.grid(row=3, column=1, padx=padding, pady=padding, sticky="w")

# ----------------------- O L D ----------------------------------
# Textbox Password ---- OLD, Default show
# password_label = tk.Label(root, text="  Authenication : ", font=font, **custom_style)
# password_label.grid(row=4, column=0, padx=padding, pady=padding, sticky="w")
# password = tk.Entry(root, font=font, **custom_style)
# password.grid(row=4, column=1, padx=padding, pady=padding, sticky="w")
# --------------------- O L D -------------------------------------


# Textbox Password --- New, Default Hidden
password_label = tk.Label(root, text="  Password : ", font=font, **custom_style)
password_label.grid(row=4, column=0, padx=padding, pady=padding, sticky="w")
password = tk.Entry(root, show="*", font=font, **custom_style)
password.grid(row=4, column=1, padx=padding, pady=padding, sticky="w")

password_visibility = tk.IntVar()
checkbox = tk.Checkbutton(root, text="Show", variable=password_visibility,
                          bg=custom_style["background"], fg=custom_style["foreground"], selectcolor='#333',
                          command=toggle_password_visibility)
checkbox.grid(row=4, column=2, padx=padding, pady=padding, sticky="w")

# Section Header: Stream Settings 
section_label = tk.Label(root, text="Stream Settings", font=header_font, **custom_style)
section_label.grid(row=5, column=0, columnspan=3, padx=header_pad, pady=header_pad, sticky="w")

# Textbox server
server_label = tk.Label(root, text="    Stream Server : ", font=font, **custom_style)
server_label.grid(row=6, column=0, padx=padding, pady=padding, sticky="w")
stream_server = tk.Entry(root, font=font, **custom_style)
stream_server.grid(row=6, column=1, padx=padding, pady=padding, sticky="w")

# Textbox key
key_label = tk.Label(root, text="   Stream Key : ", font=font, **custom_style)
key_label.grid(row=7, column=0, padx=padding, pady=padding, sticky="w")
stream_key = tk.Entry(root, font=font, **custom_style)
stream_key.grid(row=7, column=1, padx=padding, pady=padding, sticky="w")

# Section Header: Output Settings 
section_label = tk.Label(root, text="Output Settings", font=header_font, **custom_style)
section_label.grid(row=8, column=0, columnspan=3, padx=padding, pady=padding, sticky="w")

# Radio button Recording
radio_rec_label = tk.Label(root, text="    Recording: ", font=font, **custom_style)
radio_rec_label.grid(row=9, column=0, padx=padding, pady=padding, sticky="w")

radio_rec_var = tk.IntVar()
true_button = tk.Radiobutton(root, text="On", font=font, 
                             bg=custom_style["background"], fg=custom_style["foreground"], selectcolor='#333',
                             variable=radio_rec_var, value=1)
true_button.grid(row=9, column=1, padx=padding, pady=padding, sticky="w")

false_button = tk.Radiobutton(root, text="Off", font=font, 
                              bg=custom_style["background"], fg=custom_style["foreground"], selectcolor='#333',
                              variable=radio_rec_var, value=2)
false_button.grid(row=9, column=1, padx=padding, pady=padding, sticky="e")


# Radio button Streaming
radio_stream_label = tk.Label(root, text="    Streaming: ", font=font, **custom_style)
radio_stream_label.grid(row=10, column=0, padx=padding, pady=padding, sticky="w")

radio_stream_var = tk.IntVar()
true_button = tk.Radiobutton(root, text="On", font=font, 
                             bg=custom_style["background"], fg=custom_style["foreground"], selectcolor='#333',
                             variable=radio_stream_var, value=1)
true_button.grid(row=10, column=1, padx=padding, pady=padding, sticky="w")

false_button = tk.Radiobutton(root, text="Off", font=font, 
                              bg=custom_style["background"], fg=custom_style["foreground"], selectcolor='#333',
                              variable=radio_stream_var, value=2)
false_button.grid(row=10, column=1, padx=padding, pady=padding, sticky="e")


# Section header: RunTime Settings
section_label = tk.Label(root, text="Runtime Settings", font=header_font, **custom_style)
section_label.grid(row=11, column=0, columnspan=3, padx=padding, pady=padding, sticky="w")

# Time Slider: Hour
hours_slider_label = tk.Label(root, text="    Hours: ", font=font, **custom_style)
hours_slider_label.grid(row=12, column=0, padx=padding, pady=padding, sticky="w")
hours_slider = tk.Scale(root, from_=0, to=5, orient="horizontal", resolution=1, font=font,**custom_style,width=10,length=200, borderwidth=0, border=0)
hours_slider.grid(row=12, column=1,padx=padding, pady=padding, columnspan=1, sticky="e",)

# Time Slider: Min
mins_slider_label = tk.Label(root, text="    Minutes: ", font=font, **custom_style)
mins_slider_label.grid(row=13, column=0, padx=padding, pady=padding, sticky="w")
mins_slider = tk.Scale(root, from_=0, to=60, orient="horizontal", resolution=1, font=font,**custom_style,width=10,length=200, borderwidth=0, border=0)
mins_slider.grid(row=13, column=1,padx=padding, pady=padding, columnspan=1, sticky="e",)

# Time Slider: Hold Time
hold_slider_label = tk.Label(root, text="    Hold Time: ", font=font, **custom_style)
hold_slider_label.grid(row=14, column=0, padx=padding, pady=padding, sticky="w")
hold_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", resolution=1, font=font,**custom_style,width=10,length=200, borderwidth=0, border=0)
hold_slider.grid(row=14, column=1,padx=padding, pady=padding, columnspan=1, sticky="e",)


# Buttons 

# Save button
save_button = tk.Button(root, text="Save", font=font, **custom_style, width=1, height=1, command=save_config)
save_button.grid(row=15, column=0, padx=8, pady=4, columnspan=1, sticky="ew", ipadx=10, ipady=1)

# Load button
load_button = tk.Button(root, text="Load", font=font,**custom_style, width=9, height=1 ,command=clear_and_load)
load_button.grid(row=15, column=1, padx=8, pady=4, columnspan=1, sticky="w", ipadx=1, ipady=1)

# clear button
clear_button = tk.Button(root, text="Clear", font=font,**custom_style, width=8, height=1 ,command=clear_form)
clear_button.grid(row=15, column=1, padx=8, pady=4, columnspan=1, sticky="e", ipadx=1, ipady=1)


load_config()
root.mainloop()
