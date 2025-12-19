"""
SocialVerse - Module 4 GUI
Persistent Stack & Queue Visualization using Tkinter
Author: Antham Abhinav Reddy
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# ------------------ Persistent Stack ------------------
class StackNode:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


class PersistentStack:
    def __init__(self):
        self.versions = {0: None}
        self.current_version = 0

    def push(self, activity_type, user, details):
        self.current_version += 1
        activity = {
            'type': activity_type,
            'user': user,
            'details': details,
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        old_head = self.versions[self.current_version - 1]
        self.versions[self.current_version] = StackNode(activity, old_head)

    def pop(self):
        old_head = self.versions[self.current_version]
        if not old_head:
            return None
        self.current_version += 1
        self.versions[self.current_version] = old_head.next
        return old_head.data

    def get_all(self, version=None):
        ver = version or self.current_version
        result, node = [], self.versions.get(ver)
        while node:
            result.append(node.data)
            node = node.next
        return result

    def size(self, version=None):
        return len(self.get_all(version))


# ------------------ Persistent Queue ------------------
class PersistentQueue:
    def __init__(self):
        self.versions = {0: {'front': [], 'rear': []}}
        self.current_version = 0

    def enqueue(self, notif_type, sender, message):
        self.current_version += 1
        notif = {
            'type': notif_type,
            'sender': sender,
            'message': message,
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        old = self.versions[self.current_version - 1]
        new_front = old['front'][:]
        new_rear = old['rear'][:] + [notif]
        self.versions[self.current_version] = {'front': new_front, 'rear': new_rear}

    def dequeue(self):
        old = self.versions[self.current_version]
        front, rear = old['front'][:], old['rear'][:]
        if not front and not rear:
            return None
        if not front:
            front, rear = rear[::-1], []
        removed = front.pop(0)
        self.current_version += 1
        self.versions[self.current_version] = {'front': front, 'rear': rear}
        return removed

    def get_all(self, version=None):
        ver = version or self.current_version
        state = self.versions.get(ver, {'front': [], 'rear': []})
        return state['front'] + state['rear'][::-1]

    def size(self, version=None):
        return len(self.get_all(version))


# ------------------ GUI Application ------------------
class SocialVerseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SocialVerse - Persistent Stack & Queue (Module 4)")
        self.root.geometry("900x600")
        self.root.configure(bg="#f5f5f5")

        self.activity_log = PersistentStack()
        self.notifications = PersistentQueue()

        self.setup_ui()

    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        self.activity_frame = ttk.Frame(notebook)
        self.notification_frame = ttk.Frame(notebook)

        notebook.add(self.activity_frame, text="Activity Log (Stack)")
        notebook.add(self.notification_frame, text="Notifications (Queue)")

        self.build_activity_tab()
        self.build_notification_tab()

    # ------------------ ACTIVITY LOG TAB ------------------
    def build_activity_tab(self):
        frame = self.activity_frame
        frm_top = ttk.LabelFrame(frame, text="Add Activity")
        frm_top.pack(fill="x", padx=10, pady=5)

        ttk.Label(frm_top, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(frm_top, text="User:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(frm_top, text="Details:").grid(row=0, column=4, padx=5, pady=5)

        self.type_entry = ttk.Entry(frm_top, width=10)
        self.user_entry = ttk.Entry(frm_top, width=15)
        self.details_entry = ttk.Entry(frm_top, width=30)
        self.type_entry.grid(row=0, column=1)
        self.user_entry.grid(row=0, column=3)
        self.details_entry.grid(row=0, column=5)

        ttk.Button(frm_top, text="Push", command=self.push_activity).grid(row=0, column=6, padx=10)
        ttk.Button(frm_top, text="Pop", command=self.pop_activity).grid(row=0, column=7)

        self.activity_list = tk.Listbox(frame, height=20)
        self.activity_list.pack(fill="both", padx=10, pady=10, expand=True)

        ttk.Button(frame, text="View Version History", command=self.show_activity_versions).pack(pady=5)

    def push_activity(self):
        t = self.type_entry.get().strip()
        u = self.user_entry.get().strip()
        d = self.details_entry.get().strip()
        if not (t and u and d):
            messagebox.showerror("Error", "All fields required!")
            return
        self.activity_log.push(t.upper(), u, d)
        self.refresh_activities()

    def pop_activity(self):
        data = self.activity_log.pop()
        if not data:
            messagebox.showinfo("Info", "Activity log empty!")
        else:
            messagebox.showinfo("Popped", f"{data['type']} by {data['user']}: {data['details']}")
        self.refresh_activities()

    def refresh_activities(self):
        self.activity_list.delete(0, tk.END)
        for a in self.activity_log.get_all():
            self.activity_list.insert(tk.END, f"[{a['type']}] {a['user']}: {a['details']} ({a['time']})")

    def show_activity_versions(self):
        versions = "\n".join([f"V{v}: {self.activity_log.size(v)} activities"
                              for v in sorted(self.activity_log.versions.keys())])
        messagebox.showinfo("Activity Version History", versions)

    # ------------------ NOTIFICATION TAB ------------------
    def build_notification_tab(self):
        frame = self.notification_frame
        frm_top = ttk.LabelFrame(frame, text="Add Notification")
        frm_top.pack(fill="x", padx=10, pady=5)

        ttk.Label(frm_top, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(frm_top, text="Sender:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(frm_top, text="Message:").grid(row=0, column=4, padx=5, pady=5)

        self.ntype_entry = ttk.Entry(frm_top, width=15)
        self.sender_entry = ttk.Entry(frm_top, width=15)
        self.message_entry = ttk.Entry(frm_top, width=30)
        self.ntype_entry.grid(row=0, column=1)
        self.sender_entry.grid(row=0, column=3)
        self.message_entry.grid(row=0, column=5)

        ttk.Button(frm_top, text="Enqueue", command=self.add_notification).grid(row=0, column=6, padx=10)
        ttk.Button(frm_top, text="Dequeue", command=self.read_notification).grid(row=0, column=7)

        self.notif_list = tk.Listbox(frame, height=20)
        self.notif_list.pack(fill="both", padx=10, pady=10, expand=True)

        ttk.Button(frame, text="View Version History", command=self.show_notification_versions).pack(pady=5)

    def add_notification(self):
        t = self.ntype_entry.get().strip()
        s = self.sender_entry.get().strip()
        m = self.message_entry.get().strip()
        if not (t and s and m):
            messagebox.showerror("Error", "All fields required!")
            return
        self.notifications.enqueue(t.upper(), s, m)
        self.refresh_notifications()

    def read_notification(self):
        data = self.notifications.dequeue()
        if not data:
            messagebox.showinfo("Info", "Queue empty!")
        else:
            messagebox.showinfo("Dequeued", f"{data['type']} from {data['sender']}: {data['message']}")
        self.refresh_notifications()

    def refresh_notifications(self):
        self.notif_list.delete(0, tk.END)
        for n in self.notifications.get_all():
            self.notif_list.insert(tk.END, f"[{n['type']}] {n['sender']}: {n['message']} ({n['time']})")

    def show_notification_versions(self):
        versions = "\n".join([f"V{v}: {self.notifications.size(v)} notifications"
                              for v in sorted(self.notifications.versions.keys())])
        messagebox.showinfo("Notification Version History", versions)


# ------------------ MAIN ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SocialVerseGUI(root)
    root.mainloop()
