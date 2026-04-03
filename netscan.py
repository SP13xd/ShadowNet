import tkinter as tk
from tkinter import ttk
import socket
import threading
from password_manager import build_password_tab

#  THEME COLORS

BG      = "#0d0d18"
BG2     = "#12121e"
BG3     = "#1e1e2d"
BG4     = "#242434"
ACCENT  = "#6dddff"
PURPLE  = "#7b2fff"
PURPLE2 = "#ad89ff"
DANGER  = "#ff716c"
TEXT    = "#e9e6f7"
SUBTEXT = "#757482"
FONT    = "Consolas"

# Main Window
root = tk.Tk()
root.title("ShadowNet")
root.geometry("1100x700")
root.resizable(False, False)
root.configure(bg=BG)


style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab", background=BG, foreground=SUBTEXT,
                font=(FONT, 10, "bold"), padding=[24, 10])
style.map("TNotebook.Tab",
          background=[("selected", BG)],
          foreground=[("selected", ACCENT)])

#  Top Navigation Bar 
navbar = tk.Frame(root, bg=BG2, height=52)
navbar.pack(fill="x")
navbar.pack_propagate(False)

tk.Label(navbar, text="⬡  SHADOWNET",
         bg=BG2, fg=ACCENT, font=(FONT, 13, "bold")).pack(side="left", padx=20, pady=10)

tk.Frame(navbar, bg=SUBTEXT, width=1).pack(side="left", fill="y", pady=10)

#  Top divider 
tk.Frame(root, bg="#474754", height=1).pack(fill="x")

#  Notebook
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)


#  TAB 1 — NETWORK SCANNER

scanner_tab = tk.Frame(notebook, bg=BG)
notebook.add(scanner_tab, text="  🔍 NETWORK SCANNER  ")

# Page title 
title_bar = tk.Frame(scanner_tab, bg=BG, pady=18)
title_bar.pack(fill="x", padx=30)

tk.Label(title_bar, text="Network Scanner",
         bg=BG, fg=TEXT, font=(FONT, 18, "bold")).pack(anchor="w")

#  Input card 
input_card = tk.Frame(scanner_tab, bg=BG3, padx=20, pady=18)
input_card.pack(fill="x", padx=30, pady=(0, 10))

def make_input(parent, label, default, col):
    tk.Label(parent, text=label, bg=BG3, fg=SUBTEXT,
             font=(FONT, 7, "bold")).grid(row=0, column=col, sticky="w",
                                          padx=(0, 40), pady=(0, 4))
    e = tk.Entry(parent, width=24, font=(FONT, 12),
                 bg=BG, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", highlightthickness=1,
                 highlightcolor=ACCENT, highlightbackground="#474754")
    e.insert(0, default)
    e.grid(row=1, column=col, sticky="w", padx=(0, 40), ipady=10)
    return e

ip_entry         = make_input(input_card, "TARGET IP ADDRESS", "192.168.1.1", 0)
start_port_entry = make_input(input_card, "START PORT",        "1",           1)
end_port_entry   = make_input(input_card, "END PORT",          "65535",       2)

#  Buttons 
btn_row = tk.Frame(scanner_tab, bg=BG)
btn_row.pack(anchor="w", padx=30, pady=8)

def flat_btn(parent, text, bg, cmd):
    return tk.Button(parent, text=text, bg=bg, fg=BG,
                     font=(FONT, 10, "bold"), relief="flat",
                     padx=22, pady=10, cursor="hand2", bd=0,
                     activebackground=bg, activeforeground=BG,
                     command=cmd)

#  Console 
console_wrap = tk.Frame(scanner_tab, bg=BG3)
console_wrap.pack(fill="both", expand=True, padx=30, pady=(0, 5))

console_header = tk.Frame(console_wrap, bg=BG4, pady=7)
console_header.pack(fill="x")
tk.Label(console_header,
         text="●  LIVE SYSTEM OUTPUT // CONSOLE.LOG",
         bg=BG4, fg=ACCENT, font=(FONT, 8, "bold")).pack(side="left", padx=14)

results_box = tk.Text(console_wrap, bg=BG, fg="#00d4ff",
                      font=(FONT, 10), state="disabled",
                      relief="flat", padx=14, pady=10,
                      insertbackground=ACCENT, selectbackground=PURPLE)
results_box.pack(side="left", fill="both", expand=True)

scroll = tk.Scrollbar(console_wrap, command=results_box.yview, bg=BG2)
scroll.pack(side="right", fill="y")
results_box.config(yscrollcommand=scroll.set)

# Status label 
status_label = tk.Label(scanner_tab, text="●  IDLE — Ready to scan",
                        bg=BG, fg=SUBTEXT, font=(FONT, 9))
status_label.pack(anchor="w", padx=30, pady=(2, 8))

#  Scanner Logic 
scanning = False

SERVICES = {
    21: "FTP",    22: "SSH",      23: "Telnet",   25: "SMTP",
    53: "DNS",    80: "HTTP",    110: "POP3",     143: "IMAP",
    443: "HTTPS", 3306: "MySQL", 3389: "RDP",    8080: "HTTP-Alt"
}

def log(msg):
    results_box.config(state="normal")
    results_box.insert("end", msg + "\n")
    results_box.see("end")
    results_box.config(state="disabled")

def scan_ports():
    global scanning
    scanning = True
    results_box.config(state="normal")
    results_box.delete("1.0", "end")
    results_box.config(state="disabled")

    ip    = ip_entry.get()
    start = int(start_port_entry.get())
    end   = int(end_port_entry.get())
    open_ports = []

    status_label.config(text=f"●  SCANNING  {ip}", fg=ACCENT)
    log(f"[INFO] Target: {ip}")
    log(f"[INFO] Scanning range: {start} - {end}")
    log("─" * 52)

    for port in range(start, end + 1):
        if not scanning:
            log("\n⛔  Scan stopped by user.")
            break
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        s.close()
        if result == 0:
            svc = SERVICES.get(port, "unknown")
            open_ports.append(port)
            log(f"Port {port} ({svc}): OPEN")

    if scanning:
        log("─" * 52)
        log(f"✅  Scan complete. {len(open_ports)} open port(s) found.")
        status_label.config(
            text=f"●  DONE — {len(open_ports)} open port(s)", fg="#00ff88")
    scanning = False

def start_scan():
    t = threading.Thread(target=scan_ports)
    t.daemon = True
    t.start()

def stop_scan():
    global scanning
    scanning = False
    status_label.config(text="●  STOPPING...", fg=DANGER)

flat_btn(btn_row, "▶  START SCAN", ACCENT, start_scan).pack(side="left", padx=(0, 10))
flat_btn(btn_row, "⬛  STOP SCAN",  DANGER, stop_scan).pack(side="left")


#  TAB 2 — PASSWORD MANAGER

password_tab = tk.Frame(notebook, bg=BG)
notebook.add(password_tab, text="  🔐 PASSWORD MANAGER  ")
build_password_tab(password_tab)

# To Run 
root.mainloop()