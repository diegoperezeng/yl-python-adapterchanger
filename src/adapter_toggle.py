import configparser
import tkinter as tk
import subprocess
import os

def toggle_adapters():
    script_name = "adapter_toggle.sh"
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    
    command = ["sudo", "-S", "bash", script_path]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate(sudo_password.encode() + b'\n')

# Read the password from the config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.cfg"))
sudo_password = config.get("password", "sudo_password")

app = tk.Tk()
app.title("Network Adapter Toggle")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

adapter_state = tk.StringVar()
adapter_state.set("unknown")

tk.Label(frame, text="Interface State:").grid(row=0, column=0, sticky="w")
tk.Label(frame, textvariable=adapter_state).grid(row=0, column=1, sticky="w")

toggle_button = tk.Button(frame, text="Toggle Adapters", command=toggle_adapters)
toggle_button.grid(row=1, columnspan=2, pady=10)

app.mainloop()

