import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet


#  SETTINGS 

DATA_FILE       = "passwords.json"
KEY_FILE        = "secret.key"
MASTER_PASSWORD = "admin123"   # Just an example

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

# Encryption 
def load_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    with open(KEY_FILE, "rb") as f:
        return Fernet(f.read())

fernet = load_or_create_key()

def load_passwords():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return [{
        "site":     fernet.decrypt(e["site"].encode()).decode(),
        "username": fernet.decrypt(e["username"].encode()).decode(),
        "password": fernet.decrypt(e["password"].encode()).decode(),
    } for e in data]

def save_password(site, username, password):
    existing = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            existing = json.load(f)
    existing.append({
        "site":     fernet.encrypt(site.encode()).decode(),
        "username": fernet.encrypt(username.encode()).decode(),
        "password": fernet.encrypt(password.encode()).decode(),
    })
    with open(DATA_FILE, "w") as f:
        json.dump(existing, f)

def delete_password(index):
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r") as f:
        existing = json.load(f)
    if 0 <= index < len(existing):
        existing.pop(index)
    with open(DATA_FILE, "w") as f:
        json.dump(existing, f)


#  GUI

def build_password_tab(parent):

    #  LOCK SCREEN 
    lock_frame = tk.Frame(parent, bg=BG)
    lock_frame.place(relwidth=1, relheight=1)

    main_frame = tk.Frame(parent, bg=BG)

    lock_frame.grid_rowconfigure(0, weight=1)
    lock_frame.grid_rowconfigure(1, weight=0)
    lock_frame.grid_rowconfigure(2, weight=1)
    lock_frame.grid_columnconfigure(0, weight=1)

    center = tk.Frame(lock_frame, bg=BG)
    center.grid(row=1, column=0)

    # Card
    card = tk.Frame(center, bg=BG3, padx=50, pady=35)
    card.pack()



    # Lock icon box
    icon_box = tk.Frame(card, bg=BG4, width=72, height=72)
    icon_box.pack(pady=(0, 18))
    icon_box.pack_propagate(False)
    tk.Label(icon_box, text="[ # ]", bg=BG4, fg=ACCENT,
             font=(FONT, 14, "bold")).place(relx=0.5, rely=0.5, anchor="center")

    # Title
    tk.Label(card, text="Master Password Required",
             bg=BG3, fg=TEXT, font=(FONT, 15, "bold")).pack()
    

    # Input field
    tk.Label(card, text="ENTRY CREDENTIALS",
             bg=BG3, fg=SUBTEXT, font=(FONT, 7, "bold")).pack(anchor="w")

    entry_frame = tk.Frame(card, bg=BG, padx=10, pady=2,
                           highlightthickness=1, highlightbackground=SUBTEXT)
    entry_frame.pack(fill="x", pady=5)

    tk.Label(entry_frame, text=">", bg=BG, fg=ACCENT,
             font=(FONT, 12, "bold")).pack(side="left", padx=(5, 0))

    master_entry = tk.Entry(entry_frame, show="●", font=(FONT, 12),
                            bg=BG, fg=TEXT, insertbackground=ACCENT,
                            relief="flat", width=26, bd=0)
    master_entry.pack(side="left", ipady=10, padx=8)

    error_label = tk.Label(card, text="",
                           bg=BG3, fg=DANGER, font=(FONT, 9))
    error_label.pack(pady=(4, 0))

    def unlock():
        if master_entry.get() == MASTER_PASSWORD:
            lock_frame.place_forget()
            main_frame.place(relwidth=1, relheight=1)
            build_main.refresh()
        else:
            error_label.config(text="❌  Invalid credentials. Access denied.")

    master_entry.bind("<Return>", lambda e: unlock())

    tk.Button(card, text="UNLOCK VAULT",
              bg=ACCENT, fg=BG, font=(FONT, 11, "bold"),
              relief="flat", pady=12, cursor="hand2",
              activebackground=ACCENT, activeforeground=BG,
              bd=0, width=30, command=unlock).pack(pady=12)

    tk.Label(card, text="FORGOT MASTER KEY?",
             bg=BG3, fg=SUBTEXT, font=(FONT, 8)).pack()

    
    #  MAIN VAULT UI
  
    def build_main():

        #  Page header 
        header = tk.Frame(main_frame, bg=BG, pady=18)
        header.pack(fill="x", padx=30)

        left_head = tk.Frame(header, bg=BG)
        left_head.pack(side="left", fill="y")

        tag_row = tk.Frame(left_head, bg=BG)
        tag_row.pack(anchor="w")
        tk.Label(tag_row, text="02 // ENCRYPTED STORAGE",
                 bg=BG, fg=PURPLE2, font=(FONT, 8, "bold")).pack(side="left")
        tk.Label(tag_row, text="  ●", bg=BG, fg=ACCENT,
                 font=(FONT, 10)).pack(side="left")

        title_row = tk.Frame(left_head, bg=BG)
        title_row.pack(anchor="w")
        tk.Label(title_row, text="Vault Control ",
                 bg=BG, fg=TEXT, font=(FONT, 20, "bold")).pack(side="left")
        tk.Label(title_row, text="Center",
                 bg=BG, fg=ACCENT, font=(FONT, 20, "bold")).pack(side="left")

        # Status badge
        badge = tk.Frame(header, bg=BG2, padx=18, pady=10)
        badge.pack(side="right", anchor="center")
        tk.Label(badge, text="STATUS", bg=BG2, fg=SUBTEXT,
                 font=(FONT, 7)).pack(anchor="e")
        tk.Label(badge, text="[ # ]  ENCRYPTION ACTIVE",
                 bg=BG2, fg=ACCENT, font=(FONT, 10, "bold")).pack()

        tk.Frame(main_frame, bg=SUBTEXT, height=1).pack(fill="x", padx=30)

        #  Content area 
        content = tk.Frame(main_frame, bg=BG)
        content.pack(fill="both", expand=True, padx=30, pady=15)

        # LEFT PANEL 
        left = tk.Frame(content, bg=BG3, padx=20, pady=20, width=290)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        tk.Label(left, text="[ + ]  Initialize Entry",
                 bg=BG3, fg=TEXT, font=(FONT, 11, "bold")).pack(anchor="w", pady=(0, 14))

        def make_field(parent, label, placeholder, hide=False):
            tk.Label(parent, text=label, bg=BG3, fg=SUBTEXT,
                     font=(FONT, 7, "bold")).pack(anchor="w", pady=(10, 2))
            frame = tk.Frame(parent, bg=BG, padx=8,
                             highlightthickness=1, highlightbackground=SUBTEXT)
            frame.pack(fill="x")
            show = "●" if hide else ""
            e = tk.Entry(frame, font=(FONT, 10), bg=BG, fg=TEXT,
                         insertbackground=ACCENT, relief="flat",
                         show=show, width=26)
            e.pack(ipady=8, pady=2)
            if placeholder:
                e.insert(0, placeholder)
                e.config(fg=SUBTEXT)
                def on_focus_in(event, entry=e, ph=placeholder):
                    if entry.get() == ph:
                        entry.delete(0, "end")
                        entry.config(fg=TEXT)
                def on_focus_out(event, entry=e, ph=placeholder):
                    if entry.get() == "":
                        entry.insert(0, ph)
                        entry.config(fg=SUBTEXT)
                e.bind("<FocusIn>",  on_focus_in)
                e.bind("<FocusOut>", on_focus_out)
            return e

        site_entry     = make_field(left, "SITE / SERVICE",  "e.g. quantum-cloud.int")
        username_entry = make_field(left, "ACCESS IDENTITY", "Username / ID")
        pass_entry     = make_field(left, "CIPHER KEY",      "••••••••••••", hide=True)

        def add_password():
            site = site_entry.get().strip()
            user = username_entry.get().strip()
            pwd  = pass_entry.get().strip()
            placeholders = ["e.g. quantum-cloud.int", "Username / ID", "••••••••••••"]
            if site in placeholders or user in placeholders or not site or not user or not pwd:
                messagebox.showwarning("Missing Fields", "Please fill in all fields!")
                return
            save_password(site, user, pwd)
            for e, ph in zip([site_entry, username_entry, pass_entry], placeholders):
                e.delete(0, "end")
                e.insert(0, ph)
                e.config(fg=SUBTEXT)
            build_main.refresh()
            messagebox.showinfo("Vault Updated", f"Entry for '{site}' saved successfully!")

        tk.Button(left, text="ADD PASSWORD",
                  bg=PURPLE, fg="white", font=(FONT, 10, "bold"),
                  relief="flat", pady=11, cursor="hand2", bd=0,
                  activebackground=PURPLE, activeforeground="white",
                  command=add_password).pack(fill="x", pady=14)

        
        # ── RIGHT PANEL ───────────────────────────────
        right = tk.Frame(content, bg=BG3)
        right.pack(side="right", fill="both", expand=True)

        ledger_head = tk.Frame(right, bg=BG4, padx=15, pady=10)
        ledger_head.pack(fill="x")
        ledger_title = tk.Label(ledger_head,
                                text="VAULT LEDGER // 00 ENTRIES FOUND",
                                bg=BG4, fg=SUBTEXT, font=(FONT, 8, "bold"))
        ledger_title.pack(side="left")

        # Treeview styles
        tree_style = ttk.Style()
        tree_style.configure("Vault.Treeview",
                             background=BG3, foreground=TEXT,
                             fieldbackground=BG3, rowheight=34,
                             font=(FONT, 10))
        tree_style.configure("Vault.Treeview.Heading",
                             background=BG4, foreground=SUBTEXT,
                             font=(FONT, 8, "bold"), relief="flat")
        tree_style.map("Vault.Treeview", background=[("selected", PURPLE)])

        # Treeview with Copy column
        cols = ("Site", "Username", "Password", "Copy")
        tree = ttk.Treeview(right, columns=cols, show="headings",
                            style="Vault.Treeview")

        for col, w, anchor in [("Site",     220, "w"),
                                ("Username", 200, "w"),
                                ("Password", 150, "w"),
                                ("Copy",      90, "center")]:
            tree.heading(col, text=col.upper())
            tree.column(col, width=w, anchor=anchor, minwidth=w)

        vsb = ttk.Scrollbar(right, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # ── Footer ────────────────────────────────────
        footer = tk.Frame(main_frame, bg=BG, pady=10)
        footer.pack(fill="x", padx=30)

        selected_label = tk.Label(footer, text="",
                                  bg=BG, fg=SUBTEXT, font=(FONT, 8, "italic"))
        selected_label.pack(side="left")

        def on_select(event):
            selected_label.config(
                text="1 entry selected for deletion" if tree.selection() else "")
        tree.bind("<<TreeviewSelect>>", on_select)

        def copy_password(event):
            region = tree.identify_region(event.x, event.y)
            col    = tree.identify_column(event.x)
            if region == "cell" and col == "#4":
                row_id = tree.identify_row(event.y)
                if not row_id:
                    return
                index   = tree.index(row_id)
                entries = load_passwords()
                if 0 <= index < len(entries):
                    pwd = entries[index]["password"]
                    parent.winfo_toplevel().clipboard_clear()
                    parent.winfo_toplevel().clipboard_append(pwd)
                    orig = tree.item(row_id, "values")
                    tree.item(row_id, values=(orig[0], orig[1],
                                              orig[2], "✔ Copied!"))
                    parent.after(1500, lambda rid=row_id, o=orig:
                                 tree.item(rid, values=(o[0], o[1],
                                                        o[2], "⧉ Copy")))
        tree.bind("<ButtonRelease-1>", copy_password)

        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("No Selection",
                                       "Please select a row to delete.")
                return
            index = tree.index(selected[0])
            if messagebox.askyesno("Confirm",
                                   "Remove this entry from the vault?"):
                delete_password(index)
                build_main.refresh()

        tk.Button(footer, text="DELETE SELECTED",
                  bg=DANGER, fg="white", font=(FONT, 9, "bold"),
                  relief="flat", padx=18, pady=8, cursor="hand2", bd=0,
                  activebackground=DANGER, activeforeground="white",
                  command=delete_selected).pack(side="right")

        #  Refresh 
        def refresh_list():
            for row in tree.get_children():
                tree.delete(row)
            entries = load_passwords()
            ledger_title.config(
                text=f"VAULT LEDGER // {len(entries):02d} ENTRIES FOUND")
            for e in entries:
                tree.insert("", "end",
                            values=(e["site"], e["username"],
                                    "••••••••••", "⧉ Copy"))

        build_main.refresh = refresh_list

    build_main()
