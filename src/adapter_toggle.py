import configparser
import tkinter as tk
import subprocess
import os

# Read the password and user from the config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.cfg"))
sudo_password = config.get("password", "sudo_password")
sudo_user = config.get("user", "sudo_user")

os.environ["DISPLAY"] = ":0"
os.environ["XAUTHORITY"] = "/home/"  + sudo_user + "/.Xauthority"


def get_interface_state():
    command = ["sudo", "-S", "-p", "", "ip", "link", "show"]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(sudo_password.encode() + b'\n')
    if stderr:
        return f"Error: {stderr.decode()}"
    output_lines = stdout.decode().split("\n")
    eth0_state = next((line.strip().split(" ")[8] for line in output_lines if line.strip().startswith("2: eth0")), "unknown")
    eth1_state = next((line.strip().split(" ")[8] for line in output_lines if line.strip().startswith("3: eth1")), "unknown")
    return f"eth0: {eth0_state}\neth1: {eth1_state}"


def toggle_adapters():
    toggle_button.config(state="disabled")  # Disable the button
    script_name = "./adapter_toggle.sh"
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    
    command = ["sudo", script_path]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate(sudo_password.encode() + b'\n')

    
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())
    
    # Update the adapter state label
    adapter_state.set(get_interface_state())

    app.after(6500, toggle_button.config, {"state": "normal"})  # Enable the button after 6.5 seconds
    

app = tk.Tk()
app.title("Network Adapter Toggle")
app.geometry("400x150")  # Set the window size
app.resizable(False, False)  # Prevent manual resizing

frame = tk.Frame(app)
frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

adapter_state = tk.StringVar()
adapter_state.set(get_interface_state())

tk.Label(frame, text="Interface State:").grid(row=0, column=0, sticky="w")
tk.Label(frame, textvariable=adapter_state).grid(row=0, column=1, sticky="w")

toggle_button = tk.Button(frame, text="Toggle Adapters", command=toggle_adapters)
toggle_button.grid(row=1, columnspan=2, pady=10)

# Keep the window always on top
app.attributes("-topmost", True)

app.mainloop()
