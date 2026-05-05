import tkinter as tk
from tkinter import ttk, messagebox
import csv, datetime, os
from db_connection import conn, cursor

root = tk.Tk()
root.title("ClientFlow")
root.geometry("1260x740")
root.configure(bg="#0d0d0f")

# colors
BG     = "#0d0d0f"
SIDE   = "#131317"
CARD   = "#18181c"
RAISED = "#222228"
TEXT   = "#f0f0f2"       # brighter white
MUTED  = "#9a9aa8"       # lighter muted so labels are readable
ACC    = "#3d3d44"
BORDER = "#2e2e36"
RED    = "#ff5f5f"
GREEN  = "#56c98a"
AMBER  = "#f0a840"

# fonts
TITLE = ("Microgramma D Extended", 20, "bold")
SUB   = ("Microgramma D Extended", 12, "bold")
UI    = ("Helvetica", 11)
UI_SM = ("Helvetica", 10)
UI_B  = ("Helvetica", 10, "bold")

# treeview style
sty = ttk.Style()
sty.theme_use("default")
sty.configure("T.Treeview", background=RAISED, foreground="#f0f0f2", fieldbackground=RAISED, rowheight=34, borderwidth=0, font=("Helvetica", 11))
sty.configure("T.Treeview.Heading", background="#2a2a32", foreground="#c8c8d8", font=("Helvetica", 10, "bold"), relief="flat")
sty.map("T.Treeview", background=[("selected", "#4a4a58")], foreground=[("selected", "#ffffff")])

# layout
sidebar = tk.Frame(root, bg=SIDE, width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)
content = tk.Frame(root, bg=BG)
content.pack(side="right", expand=True, fill="both")

tk.Label(sidebar, text="ClientFlow",        font=("Microgramma D Extended", 13, "bold"), bg=SIDE, fg="#f0f0f2").pack(pady=(28,2), padx=20, anchor="w")
tk.Label(sidebar, text="Video Editing CRM", font=UI_SM,                                  bg=SIDE, fg="#9a9aa8").pack(padx=20, anchor="w")
tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=16)

nav_btns = {}

# helpers
def clear():
    for w in content.winfo_children(): w.destroy()

def card():
    f = tk.Frame(content, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    f.pack(fill="both", expand=True, padx=24, pady=20)
    return f

def hdr(p, title, sub=""):
    tk.Label(p, text=title, font=TITLE, bg=CARD, fg="#f0f0f2").pack(anchor="w", padx=28, pady=(24,2))
    if sub: tk.Label(p, text=sub, font=("Microgramma D Extended", 9), bg=CARD, fg="#9a9aa8").pack(anchor="w", padx=28)
    tk.Frame(p, bg=BORDER, height=1).pack(fill="x", padx=28, pady=(14,20))

def field(parent, label):
    tk.Label(parent, text=label, font=("Helvetica", 10, "bold"), bg=CARD, fg="#b0b0c0").pack(anchor="w", padx=28, pady=(8,2))
    e = tk.Entry(parent, font=("Helvetica", 12), relief="flat", bg="#2a2a32", fg="#f0f0f2", insertbackground="#f0f0f2", width=30, highlightbackground="#3a3a48", highlightthickness=1, highlightcolor="#7a7a9a")
    e.pack(anchor="w", padx=28, pady=(0,4), ipady=9)
    return e

def btn(parent, text, cmd, bg=RAISED, fg="#f0f0f2"):
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg, font=UI_B, relief="flat", padx=18, pady=9, cursor="hand2", activebackground="#4a4a58", activeforeground="#ffffff", bd=0)
    b.pack(side="left", padx=(0,8))
    return b

def table(parent, cols, widths, h=16):
    f = tk.Frame(parent, bg=CARD)
    sb = ttk.Scrollbar(f, orient="vertical")
    sb.pack(side="right", fill="y")
    t = ttk.Treeview(f, columns=cols, show="headings", height=h, style="T.Treeview", yscrollcommand=sb.set)
    sb.config(command=t.yview)
    for c, w in zip(cols, widths):
        t.heading(c, text=c)
        t.column(c, anchor="center", width=w)
    t.pack(side="left", fill="both", expand=True)
    return f, t

def active(name):
    for n, b in nav_btns.items():
        b.config(bg=ACC if n == name else SIDE, fg="#ffffff" if n == name else "#c0c0cc")

# add client
def add_client():
    active("Add Client"); clear()
    c = card(); hdr(c, "ADD CLIENT", "Register a new client")
    row = tk.Frame(c, bg=CARD); row.pack(fill="x")
    L = tk.Frame(row, bg=CARD); L.pack(side="left", expand=True, fill="both")
    R = tk.Frame(row, bg=CARD); R.pack(side="right", expand=True, fill="both")
    n = field(L, "Client Name")
    p = field(L, "Phone")
    e = field(R, "Email")
    co = field(R, "Company")
    def save():
        if not n.get() or not p.get() or not e.get():
            messagebox.showwarning("Missing", "Name, phone and email are required.")
            return
        try:
            cursor.execute("INSERT INTO Clients(client_name,phone,email,company_name,joined_date) VALUES(%s,%s,%s,%s,CURDATE())", (n.get(), p.get(), e.get(), co.get()))
            conn.commit()
            for x in (n, p, e, co): x.delete(0, tk.END)
            messagebox.showinfo("Done", "Client saved!")
        except Exception as ex: messagebox.showerror("Error", str(ex))
    bf = tk.Frame(c, bg=CARD); bf.pack(anchor="w", padx=28, pady=(16,24))
    btn(bf, "Save Client", save)

# view clients
def view_clients():
    active("View Clients"); clear()
    c = card(); hdr(c, "CLIENTS")
    tf, t = table(c, ("ID","Name","Phone","Email","Company","Joined"), (55,165,125,210,160,100), 18)
    tf.pack(fill="both", expand=True, padx=28, pady=(0,14))
    def load():
        t.delete(*t.get_children())
        cursor.execute("SELECT client_id,client_name,phone,email,company_name,joined_date FROM Clients ORDER BY client_id DESC")
        for r in cursor.fetchall(): t.insert("", tk.END, values=r)
    load()
    def delete():
        s = t.selection()
        if not s: messagebox.showwarning("None", "Select a client first."); return
        cid = t.item(s[0])["values"][0]
        if messagebox.askyesno("Delete?", "This will also delete their projects."):
            try:
                cursor.execute("DELETE FROM Projects WHERE client_id=%s", (cid,))
                cursor.execute("DELETE FROM Clients WHERE client_id=%s", (cid,))
                conn.commit(); t.delete(s[0])
            except Exception as ex: messagebox.showerror("Error", str(ex))
    bf = tk.Frame(c, bg=CARD); bf.pack(anchor="w", padx=28, pady=(0,20))
    btn(bf, "Refresh", load)
    btn(bf, "Delete Selected", delete, bg="#3a1a1a", fg=RED)

# add project
def add_project():
    active("Add Project"); clear()
    c = card(); hdr(c, "ADD PROJECT", "Attach a project to a client")
    row = tk.Frame(c, bg=CARD); row.pack(fill="x")
    L = tk.Frame(row, bg=CARD); L.pack(side="left", expand=True, fill="both")
    R = tk.Frame(row, bg=CARD); R.pack(side="right", expand=True, fill="both")
    ci = field(L, "Client ID")
    pn = field(L, "Project Name")
    bu = field(L, "Budget (Rs.)")
    pt = field(R, "Project Type")
    dl = field(R, "Deadline (YYYY-MM-DD)")
    tk.Label(R, text="Status", font=("Helvetica", 10, "bold"), bg=CARD, fg="#b0b0c0").pack(anchor="w", padx=28, pady=(8,2))
    sv = tk.StringVar(value="Pending")
    ttk.Combobox(R, textvariable=sv, values=["Pending","In Progress","Completed","Cancelled"], state="readonly", width=28, font=UI).pack(anchor="w", padx=28, ipady=6)
    def save():
        if not ci.get() or not pn.get() or not dl.get() or not bu.get():
            messagebox.showwarning("Missing", "Please fill all fields.")
            return
        try:
            cursor.execute("INSERT INTO Projects(client_id,project_name,project_type,start_date,deadline,status,budget) VALUES(%s,%s,%s,CURDATE(),%s,%s,%s)", (ci.get(), pn.get(), pt.get(), dl.get(), sv.get(), bu.get()))
            conn.commit()
            for x in (ci, pn, pt, dl, bu): x.delete(0, tk.END)
            messagebox.showinfo("Done", "Project saved!")
        except Exception as ex: messagebox.showerror("Error", str(ex))
    bf = tk.Frame(c, bg=CARD); bf.pack(anchor="w", padx=28, pady=(16,24))
    btn(bf, "Save Project", save)

# view projects
def view_projects():
    active("View Projects"); clear()
    c = card(); hdr(c, "PROJECTS")
    bar = tk.Frame(c, bg=CARD); bar.pack(fill="x", padx=28, pady=(0,12))
    tk.Label(bar, text="Filter:", font=("Helvetica", 10, "bold"), bg=CARD, fg="#b0b0c0").pack(side="left", padx=(0,8))
    fv = tk.StringVar(value="All")
    ttk.Combobox(bar, textvariable=fv, values=["All","Pending","In Progress","Completed","Cancelled"], state="readonly", width=14, font=UI_SM).pack(side="left")
    tf, t = table(c, ("ID","Client","Project","Type","Start","Deadline","Status","Budget"), (50,145,175,115,95,95,105,105), 15)
    tf.pack(fill="both", expand=True, padx=28, pady=(0,14))
    def load(*_):
        t.delete(*t.get_children())
        q = "SELECT p.project_id,c.client_name,p.project_name,p.project_type,p.start_date,p.deadline,p.status,p.budget FROM Projects p JOIN Clients c ON p.client_id=c.client_id"
        f = fv.get()
        if f != "All": cursor.execute(q + " WHERE p.status=%s ORDER BY p.project_id DESC", (f,))
        else: cursor.execute(q + " ORDER BY p.project_id DESC")
        for r in cursor.fetchall(): t.insert("", tk.END, values=r)
    fv.trace_add("write", load); load()
    def update():
        s = t.selection()
        if not s: messagebox.showwarning("None", "Select a project first."); return
        pid = t.item(s[0])["values"][0]
        w = tk.Toplevel(root); w.title("Update Status"); w.geometry("300x170"); w.configure(bg=CARD); w.grab_set()
        tk.Label(w, text="NEW STATUS", font=("Microgramma D Extended", 11, "bold"), bg=CARD, fg="#f0f0f2").pack(pady=(22,6))
        sv2 = tk.StringVar(value="In Progress")
        ttk.Combobox(w, textvariable=sv2, values=["Pending","In Progress","Completed","Cancelled"], state="readonly", width=22, font=UI).pack(pady=6)
        def apply():
            try:
                cursor.execute("UPDATE Projects SET status=%s WHERE project_id=%s", (sv2.get(), pid))
                conn.commit(); w.destroy(); load()
            except Exception as ex: messagebox.showerror("Error", str(ex))
        bf2 = tk.Frame(w, bg=CARD); bf2.pack(pady=12)
        btn(bf2, "Apply", apply)
    def delete():
        s = t.selection()
        if not s: messagebox.showwarning("None", "Select a project first."); return
        pid = t.item(s[0])["values"][0]
        if messagebox.askyesno("Delete?", "Remove this project?"):
            try:
                cursor.execute("DELETE FROM Projects WHERE project_id=%s", (pid,))
                conn.commit(); t.delete(s[0])
            except Exception as ex: messagebox.showerror("Error", str(ex))
    bf = tk.Frame(c, bg=CARD); bf.pack(anchor="w", padx=28, pady=(0,20))
    btn(bf, "Refresh", load)
    btn(bf, "Update Status", update, bg="#2a2a10", fg=AMBER)
    btn(bf, "Delete", delete, bg="#3a1a1a", fg=RED)

# full report
def full_report():
    active("Full Report"); clear()
    c = card(); hdr(c, "REPORT", "Business overview")
    try:
        cursor.execute("SELECT COUNT(*) FROM Clients");                                         cl = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Projects");                                        pr = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Projects WHERE status='Completed'");               dn = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Projects WHERE status='In Progress'");             ac = cursor.fetchone()[0]
        cursor.execute("SELECT IFNULL(SUM(budget),0) FROM Projects WHERE status='Completed'"); rv = cursor.fetchone()[0]
    except Exception as ex: messagebox.showerror("Error", str(ex)); return

    kf = tk.Frame(c, bg=CARD); kf.pack(fill="x", padx=28, pady=(0,22))
    for val, label, col in [(cl,"Clients","#e0e0f0"),(pr,"Projects","#e0e0f0"),(dn,"Completed",GREEN),(ac,"Active",AMBER),(f"Rs.{rv:,.0f}","Revenue",GREEN)]:
        tile = tk.Frame(kf, bg=RAISED, highlightbackground="#3a3a48", highlightthickness=1)
        tile.pack(side="left", expand=True, fill="x", padx=(0,10))
        tk.Label(tile, text=str(val), font=("Microgramma D Extended", 20, "bold"), bg=RAISED, fg=col).pack(pady=(16,2))
        tk.Label(tile, text=label,    font=("Helvetica", 10, "bold"),              bg=RAISED, fg="#9a9ab0").pack(pady=(0,14))

    tk.Label(c, text="BY STATUS",       font=SUB, bg=CARD, fg="#e0e0f0").pack(anchor="w", padx=28, pady=(0,8))
    sf, st = table(c, ("Status","Count","Total Budget"), (160,100,180), 4)
    sf.pack(fill="x", padx=28, pady=(0,18))
    cursor.execute("SELECT status,COUNT(*),IFNULL(SUM(budget),0) FROM Projects GROUP BY status")
    for r in cursor.fetchall(): st.insert("", tk.END, values=(r[0], r[1], f"{r[2]:,.0f}"))

    tk.Label(c, text="RECENT PROJECTS", font=SUB, bg=CARD, fg="#e0e0f0").pack(anchor="w", padx=28, pady=(0,8))
    rf, rt = table(c, ("ID","Client","Project","Status","Deadline","Budget"), (50,160,190,110,105,110), 8)
    rf.pack(fill="both", expand=True, padx=28, pady=(0,14))
    cursor.execute("SELECT p.project_id,c.client_name,p.project_name,p.status,p.deadline,p.budget FROM Projects p JOIN Clients c ON p.client_id=c.client_id ORDER BY p.project_id DESC LIMIT 10")
    for r in cursor.fetchall(): rt.insert("", tk.END, values=r)

    def export():
        path = os.path.join(os.path.expanduser("~"), f"clientflow_{datetime.date.today()}.csv")
        try:
            cursor.execute("SELECT p.project_id,c.client_name,p.project_name,p.project_type,p.start_date,p.deadline,p.status,p.budget FROM Projects p JOIN Clients c ON p.client_id=c.client_id ORDER BY p.project_id")
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["ID","Client","Project","Type","Start","Deadline","Status","Budget"])
                w.writerows(cursor.fetchall())
            messagebox.showinfo("Exported", f"Saved to {path}")
        except Exception as ex: messagebox.showerror("Error", str(ex))

    bf = tk.Frame(c, bg=CARD); bf.pack(anchor="w", padx=28, pady=(0,20))
    btn(bf, "Refresh", full_report)
    btn(bf, "Export CSV", export, bg="#182a1e", fg=GREEN)

# sidebar
for label, cmd in [("Add Client",add_client),("View Clients",view_clients),("Add Project",add_project),("View Projects",view_projects),("Full Report",full_report)]:
    b = tk.Button(sidebar, text=f"  {label}", command=cmd, bg=SIDE, fg="#c0c0cc", font=UI_SM, relief="flat", anchor="w", padx=10, pady=12, cursor="hand2", activebackground=ACC, activeforeground="#ffffff", bd=0)
    b.pack(fill="x", padx=10, pady=1)
    nav_btns[label] = b

tk.Frame(sidebar, bg=SIDE).pack(expand=True)
tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=8)
tk.Button(sidebar, text="  Exit", command=root.destroy, bg=SIDE, fg=RED, font=UI_SM, relief="flat", anchor="w", padx=10, pady=12, cursor="hand2", activebackground="#3a1a1a", activeforeground=RED, bd=0).pack(fill="x", padx=10, pady=(0,16))

view_clients()
root.mainloop()