import tkinter as tk
from tkinter import messagebox
import socket
import sys

def get_service_name(port):
    try:
        service_name = socket.getservbyport(port)
        return service_name
    except (socket.error, OSError):
        return "Unknown Service"

def scan_ports():
    target_host = entry_target.get()
    start_port = int(entry_start_port.get())
    end_port = int(entry_end_port.get())

    result_text.delete(1.0, tk.END)  # Clear previous results

    try:
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_host, port))
            if result == 0:
                service_name = get_service_name(port)
                result_text.insert(tk.END, f"Port {port} is open. Service: {service_name}\n")
            sock.close()
    except KeyboardInterrupt:
        result_text.insert(tk.END, "\nScan interrupted by user. Exiting...\n")
        sys.exit(1)

    open_ports_count = result_text.get(1.0, tk.END).count("Port")
    result_text.insert(tk.END, f"\nThere are {open_ports_count} ports open out of {end_port - start_port + 1} ports")

def on_exit():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        root.destroy()

# GUI setup
root = tk.Tk()
root.title("Port Scanner")

# Entry widgets
label_target = tk.Label(root, text="Target IP address:")
label_start_port = tk.Label(root, text="Starting port:")
label_end_port = tk.Label(root, text="Ending port:")

entry_target = tk.Entry(root)
entry_start_port = tk.Entry(root)
entry_end_port = tk.Entry(root)

# Result text widget
result_text = tk.Text(root, height=15, width=50, wrap=tk.WORD)

# Scan button
scan_button = tk.Button(root, text="Scan Ports", command=scan_ports)

# Exit button
exit_button = tk.Button(root, text="Exit", command=on_exit)

# Grid layout
label_target.grid(row=0, column=0, padx=5, pady=5)
entry_target.grid(row=0, column=1, padx=5, pady=5)
label_start_port.grid(row=1, column=0, padx=5, pady=5)
entry_start_port.grid(row=1, column=1, padx=5, pady=5)
label_end_port.grid(row=2, column=0, padx=5, pady=5)
entry_end_port.grid(row=2, column=1, padx=5, pady=5)
scan_button.grid(row=3, column=0, columnspan=2, pady=10)
result_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
exit_button.grid(row=5, column=0, columnspan=2, pady=10)

# Configure row and column weights
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Run the GUI
root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()

