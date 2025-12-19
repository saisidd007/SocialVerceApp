"""
socialverse_gui.py - Enhanced Version
Integrated GUI for SocialVerse with ALL Graph Features.
Imports:
 - module1_persistent_graph (PersistentGraph, VersionControl, UnionFind)
 - module2_persistent_linkedlist (PersistentLinkedList)
 - module3_bst (BST)
 - module4_stack_queue (PersistentStack, PersistentQueue, Activity, Notification)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

# ---- Import all 4 modules ----
from module1_persistent_graph import PersistentGraph, VersionControl, UnionFind
from module2_persistent_linkedlist import PersistentLinkedList
from module3_bst import BST
from module4_stack_queue import PersistentStack, PersistentQueue


class SocialVerseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 SocialVerse GUI - Enhanced with Full Graph Features")
        self.root.geometry("1100x700") 
        self.root.configure(bg="#f8f9fa")

        # ---- Core Persistent Structures ----
        self.graph = PersistentGraph()
        self.version_control = VersionControl()
        self.version_control.save(self.graph)  # Save initial version
        self.linked_list = PersistentLinkedList()
        self.user_bst = BST()
        self.activity_stack = PersistentStack()
        self.notification_queue = PersistentQueue()
        self.union_find = UnionFind()
        
        # Pre-populate stack/queue
        self.activity_stack.push("LOGIN", 1, "User logged in")
        self.notification_queue.enqueue("WELCOME", 0, "Welcome to SocialVerse!")

        # ---- Tabs ----
        tab_control = ttk.Notebook(root)
        tab_control.pack(expand=1, fill="both")

        self.tab_users = ttk.Frame(tab_control)
        self.tab_friends = ttk.Frame(tab_control)
        self.tab_communities = ttk.Frame(tab_control)  # NEW
        self.tab_posts = ttk.Frame(tab_control)
        self.tab_stack_queue = ttk.Frame(tab_control)
        self.tab_history = ttk.Frame(tab_control)

        tab_control.add(self.tab_users, text="Users")
        tab_control.add(self.tab_friends, text="Friendships")
        tab_control.add(self.tab_communities, text="Communities")  # NEW
        tab_control.add(self.tab_posts, text="Posts / Feed")
        tab_control.add(self.tab_stack_queue, text="Activity / Notifications")
        tab_control.add(self.tab_history, text="Version History")

        # ---- Setup each tab ----
        self.setup_user_tab()
        self.setup_friend_tab()
        self.setup_communities_tab()  # NEW
        self.setup_post_tab()
        self.setup_stack_queue_tab()
        self.setup_history_tab()

    # =====================================================
    #  USERS TAB
    # =====================================================
    def setup_user_tab(self):
        frame = self.tab_users

        title = tk.Label(frame, text="User Management (BST)", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        form = tk.Frame(frame)
        form.pack(pady=5)

        tk.Label(form, text="User ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(form, text="Email:").grid(row=2, column=0, padx=5, pady=5)

        self.uid_entry = tk.Entry(form)
        self.name_entry = tk.Entry(form)
        self.email_entry = tk.Entry(form)

        self.uid_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add / Update", command=self.add_user, bg="#27ae60", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Search", command=self.search_user, bg="#2980b9", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_user, bg="#c0392b", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Show All", command=self.show_all_users, bg="#8e44ad", fg="white").grid(row=0, column=3, padx=5)

        # Display table
        self.user_tree = ttk.Treeview(frame, columns=("UID", "Name", "Email"), show="headings", height=10)
        self.user_tree.heading("UID", text="User ID")
        self.user_tree.heading("Name", text="Name")
        self.user_tree.heading("Email", text="Email")
        self.user_tree.pack(pady=10, fill="x", padx=20)

    def add_user(self):
        try:
            uid = self.uid_entry.get().strip()
            name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            
            if not uid or not name or not email:
                raise ValueError("All fields are required.")
            
            if self.graph.user_exists(uid):
                messagebox.showwarning("Warning", "User already exists!")
                return
                
            # Add to BST with integer conversion for sorting
            try:
                uid_int = int(uid)
                self.user_bst.insert(uid_int, name, email)
            except ValueError:
                # If UID is not numeric, still add to graph
                pass
                
            # Add to graph (returns new version)
            self.graph = self.graph.add_user(uid, name)
            self.version_control.save(self.graph)
            
            # Initialize in union-find
            self.union_find.make_set(uid)
            
            # Log activity
            self.activity_stack.push("USER_ADD", uid, f"Added user {name} ({email})")
            self.show_activity_log()
            
            messagebox.showinfo("Success", f"User {name} added (Version {self.graph.version})")
            self.clear_user_fields()
            self.show_all_users()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_user(self):
        try:
            uid = self.uid_entry.get().strip()
            if self.graph.user_exists(uid):
                name = self.graph.get_user_name(uid)
                friends = self.graph.get_friends(uid)
                friend_names = [self.graph.get_user_name(f) for f in friends]
                
                info = f"User ID: {uid}\n"
                info += f"Name: {name}\n"
                info += f"Friends ({len(friends)}): {', '.join(friend_names) if friend_names else 'None'}"
                
                messagebox.showinfo("User Found", info)
            else:
                messagebox.showwarning("Not Found", "User ID not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_user(self):
        try:
            uid = self.uid_entry.get().strip()
            if not self.graph.user_exists(uid):
                messagebox.showwarning("Not Found", "User not found.")
                return
                
            name = self.graph.get_user_name(uid)
            
            # Note: The persistent graph doesn't have remove_user method
            # We would need to add this to the module or just log the deletion
            messagebox.showinfo("Info", "User deletion not implemented in persistent graph.\nUse version control to revert changes.")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_all_users(self):
        for i in self.user_tree.get_children():
            self.user_tree.delete(i)
            
        # Show from BST if available
        try:
            for uid, name, email in self.user_bst.inorder():
                self.user_tree.insert("", "end", values=(uid, name, email))
        except:
            # Fallback to graph
            for uid in sorted(self.graph.get_all_users()):
                name = self.graph.get_user_name(uid)
                self.user_tree.insert("", "end", values=(uid, name, "N/A"))

    def clear_user_fields(self):
        self.uid_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    # =====================================================
    #  FRIENDSHIP TAB - ENHANCED
    # =====================================================
    def setup_friend_tab(self):
        frame = self.tab_friends
        tk.Label(frame, text="Friendship Management (Graph)", font=("Arial", 16, "bold")).pack(pady=10)

        # Input form
        form = tk.Frame(frame)
        form.pack(pady=5)
        tk.Label(form, text="User 1 ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form, text="User 2 ID:").grid(row=1, column=0, padx=5, pady=5)
        self.f1 = tk.Entry(form, width=20)
        self.f2 = tk.Entry(form, width=20)
        self.f1.grid(row=0, column=1, padx=5)
        self.f2.grid(row=1, column=1, padx=5)

        btn_frame = tk.Frame(form)
        btn_frame.grid(row=0, column=2, rowspan=2, padx=10)
        tk.Button(btn_frame, text="Add Friendship", bg="#27ae60", fg="white", 
                 command=self.add_friendship, width=15).pack(pady=2)
        tk.Button(btn_frame, text="Remove Friendship", bg="#c0392b", fg="white", 
                 command=self.remove_friendship, width=15).pack(pady=2)
        tk.Button(btn_frame, text="Find Mutual Friends", bg="#3498db", fg="white", 
                 command=self.find_mutual_friends, width=15).pack(pady=2)

        # Display area
        display_frame = tk.Frame(frame)
        display_frame.pack(pady=10, fill="both", expand=True, padx=20)

        tk.Label(display_frame, text="All Friendships:", font=("Arial", 11, "bold")).pack()
        
        self.friend_list = scrolledtext.ScrolledText(display_frame, width=80, height=15, wrap=tk.WORD)
        self.friend_list.pack(pady=5, fill="both", expand=True)

        tk.Button(frame, text="Refresh Friendships", bg="#8e44ad", fg="white", 
                 command=self.show_all_friendships).pack(pady=5)

    def add_friendship(self):
        try:
            u1_input = self.f1.get().strip()
            u2_input = self.f2.get().strip()

            if not u1_input or not u2_input:
                raise ValueError("Both User IDs are required.")

            if not self.graph.user_exists(u1_input):
                raise ValueError(f"User {u1_input} does not exist.")
            if not self.graph.user_exists(u2_input):
                raise ValueError(f"User {u2_input} does not exist.")
            
            # Add friendship (returns new version)
            self.graph = self.graph.add_friendship(u1_input, u2_input)
            self.version_control.save(self.graph)
            
            # Update union-find
            self.union_find.union(u1_input, u2_input)
            
            # Log activity
            self.activity_stack.push("FRIEND_ADD", u1_input, f"Added friendship with {u2_input}")
            self.show_activity_log()
            
            messagebox.showinfo("Success", f"Friendship added between {u1_input} and {u2_input}.\n(Version {self.graph.version})")
            self.show_all_friendships()
        
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_friendship(self):
        try:
            u1 = self.f1.get().strip()
            u2 = self.f2.get().strip()
            
            if not u1 or not u2:
                raise ValueError("Both User IDs are required.")
            
            # Remove friendship (returns new version)
            self.graph = self.graph.remove_friendship(u1, u2)
            self.version_control.save(self.graph)
            
            # Log activity
            self.activity_stack.push("FRIEND_REMOVE", u1, f"Removed friendship with {u2}")
            self.show_activity_log()
            
            messagebox.showinfo("Removed", f"Friendship removed between {u1} and {u2}.\n(Version {self.graph.version})")
            self.show_all_friendships()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def find_mutual_friends(self):
        try:
            u1 = self.f1.get().strip()
            u2 = self.f2.get().strip()
            
            if not u1 or not u2:
                raise ValueError("Both User IDs are required.")
            
            if not self.graph.user_exists(u1) or not self.graph.user_exists(u2):
                raise ValueError("Both users must exist.")
            
            mutual = self.graph.find_mutual_friends(u1, u2)
            
            if mutual:
                mutual_names = [f"{self.graph.get_user_name(u)} ({u})" for u in mutual]
                result = f"Mutual Friends between {self.graph.get_user_name(u1)} and {self.graph.get_user_name(u2)}:\n\n"
                result += "\n".join(mutual_names)
                messagebox.showinfo("Mutual Friends Found", result)
            else:
                messagebox.showinfo("No Mutual Friends", 
                                  f"{self.graph.get_user_name(u1)} and {self.graph.get_user_name(u2)} have no mutual friends.")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_all_friendships(self):
        self.friend_list.delete(1.0, tk.END)
        
        all_users = sorted(self.graph.get_all_users())
        
        if not all_users:
            self.friend_list.insert(tk.END, "No users in the system yet.\n")
            return
        
        total_friendships = 0
        
        for uid in all_users:
            name = self.graph.get_user_name(uid)
            friends = self.graph.get_friends(uid)
            friend_names = [f"{self.graph.get_user_name(f)} ({f})" for f in sorted(friends)]
            
            total_friendships += len(friends)
            
            self.friend_list.insert(tk.END, f"🧑 {name} ({uid})\n", "user")
            if friend_names:
                self.friend_list.insert(tk.END, f"   └─ Friends: {', '.join(friend_names)}\n\n")
            else:
                self.friend_list.insert(tk.END, f"   └─ No friends yet\n\n")
        
        self.friend_list.insert(tk.END, f"\n{'='*60}\n")
        self.friend_list.insert(tk.END, f"Total Users: {len(all_users)} | Total Connections: {total_friendships // 2}\n")
        
        self.friend_list.tag_config("user", foreground="#2c3e50", font=("Arial", 10, "bold"))

    # =====================================================
    #  NEW: COMMUNITIES TAB
    # =====================================================
    def setup_communities_tab(self):
        frame = self.tab_communities
        tk.Label(frame, text="Community Detection (Union-Find)", font=("Arial", 16, "bold")).pack(pady=10)
        
        info_label = tk.Label(frame, text="Communities are groups of connected users based on friendships.", 
                             font=("Arial", 10), fg="#7f8c8d")
        info_label.pack(pady=5)
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="🔍 Detect Communities", command=self.detect_communities, 
                 bg="#27ae60", fg="white", font=("Arial", 11, "bold"), width=20).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="🔄 Refresh", command=self.detect_communities, 
                 bg="#3498db", fg="white", font=("Arial", 11), width=15).grid(row=0, column=1, padx=5)
        
        # Communities display
        self.communities_text = scrolledtext.ScrolledText(frame, width=90, height=20, wrap=tk.WORD, 
                                                          font=("Courier", 10))
        self.communities_text.pack(pady=10, padx=20, fill="both", expand=True)

    def detect_communities(self):
        try:
            # Rebuild union-find from current graph
            self.union_find = UnionFind()
            
            all_users = self.graph.get_all_users()
            
            if not all_users:
                self.communities_text.delete(1.0, tk.END)
                self.communities_text.insert(tk.END, "No users in the system yet.\n")
                return
            
            # Initialize all users
            for u in all_users:
                self.union_find.make_set(u)
            
            # Union all friendships
            for u in all_users:
                for f in self.graph.get_friends(u):
                    self.union_find.union(u, f)
            
            # Get communities
            communities = self.union_find.get_communities()
            
            # Display results
            self.communities_text.delete(1.0, tk.END)
            self.communities_text.insert(tk.END, "="*70 + "\n")
            self.communities_text.insert(tk.END, "               COMMUNITY DETECTION RESULTS\n")
            self.communities_text.insert(tk.END, "="*70 + "\n\n")
            
            self.communities_text.insert(tk.END, f"Total Communities Found: {len(communities)}\n")
            self.communities_text.insert(tk.END, f"Total Users: {len(all_users)}\n\n")
            self.communities_text.insert(tk.END, "-"*70 + "\n\n")
            
            for i, (root, members) in enumerate(sorted(communities.items()), 1):
                member_details = []
                for m in sorted(members):
                    name = self.graph.get_user_name(m)
                    friends_count = len(self.graph.get_friends(m))
                    member_details.append(f"{name} ({m}) - {friends_count} friends")
                
                self.communities_text.insert(tk.END, f"🌐 Community {i} ({len(members)} members)\n", "header")
                self.communities_text.insert(tk.END, f"   Root: {root}\n")
                self.communities_text.insert(tk.END, f"   Members:\n")
                for detail in member_details:
                    self.communities_text.insert(tk.END, f"      • {detail}\n")
                self.communities_text.insert(tk.END, "\n")
            
            self.communities_text.tag_config("header", foreground="#2c3e50", font=("Courier", 10, "bold"))
            
            # Log activity
            self.activity_stack.push("COMMUNITY_DETECT", 0, f"Detected {len(communities)} communities")
            self.show_activity_log()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =====================================================
    #  POST / FEED TAB
    # =====================================================
    def setup_post_tab(self):
        frame = self.tab_posts
        tk.Label(frame, text="User Feed (Persistent Linked List)", font=("Arial", 16, "bold")).pack(pady=10)

        form = tk.Frame(frame)
        form.pack(pady=5)
        tk.Label(form, text="Post Content:").grid(row=0, column=0, padx=5)
        self.post_entry = tk.Entry(form, width=60)
        self.post_entry.grid(row=0, column=1, padx=5)
        tk.Button(form, text="Add Post", bg="#27ae60", fg="white", command=self.add_post).grid(row=0, column=2, padx=5)
        tk.Button(form, text="Undo", bg="#2980b9", fg="white", command=self.undo_post).grid(row=0, column=3, padx=5)
        tk.Button(form, text="Redo", bg="#8e44ad", fg="white", command=self.redo_post).grid(row=0, column=4, padx=5)

        self.feed_box = tk.Listbox(frame, width=90, height=15)
        self.feed_box.pack(pady=10)

    def add_post(self):
        content = self.post_entry.get().strip()
        if content:
            self.linked_list.add_post(content)
            self.activity_stack.push("POST", 1, f"Created a post: '{content[:20]}...'")
            self.show_activity_log()
            self.feed_box.insert(tk.END, f"📝 {content}")
            self.post_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Post content cannot be empty.")

    def undo_post(self):
        post = self.linked_list.undo()
        if post:
            self.activity_stack.push("POST_UNDO", 1, f"Undo post: '{post[:20]}...'")
            self.show_activity_log()
            messagebox.showinfo("Undo", f"Removed: {post}")
            self.show_feed()

    def redo_post(self):
        post = self.linked_list.redo()
        if post:
            self.activity_stack.push("POST_REDO", 1, f"Redo post: '{post[:20]}...'")
            self.show_activity_log()
            messagebox.showinfo("Redo", f"Restored: {post}")
            self.show_feed()

    def show_feed(self):
        self.feed_box.delete(0, tk.END)
        for post in self.linked_list.get_all_posts():
            self.feed_box.insert(tk.END, f"📝 {post}")

    # =====================================================
    #  STACK / QUEUE TAB
    # =====================================================
    def setup_stack_queue_tab(self):
        frame = self.tab_stack_queue
        tk.Label(frame, text="Activity Log (Stack) & Notifications (Queue)", font=("Arial", 16, "bold")).pack(pady=10)

        main_paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=1, padx=10, pady=5)

        # Stack (Activity Log)
        stack_frame = ttk.LabelFrame(main_paned, text=f"Activity Log (Stack: V{self.activity_stack.current_version})", padding="10")
        main_paned.add(stack_frame, weight=1)

        tk.Label(stack_frame, text="Activities (Most Recent Top):").pack(pady=5)
        self.activity_log_box = tk.Listbox(stack_frame, width=50, height=18)
        self.activity_log_box.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

        tk.Button(stack_frame, text="Clear Last Activity (Pop)", command=self.pop_activity, bg="#c0392b", fg="white").pack(pady=5)
        self.show_activity_log()

        # Queue (Notifications)
        queue_frame = ttk.LabelFrame(main_paned, text=f"Notifications (Queue: V{self.notification_queue.current_version})", padding="10")
        main_paned.add(queue_frame, weight=1)

        tk.Label(queue_frame, text="Send New Notification:").pack(pady=5)
        
        notif_form = tk.Frame(queue_frame)
        notif_form.pack(pady=5)
        tk.Label(notif_form, text="Type:").grid(row=0, column=0, padx=2, pady=2)
        tk.Label(notif_form, text="Sender:").grid(row=1, column=0, padx=2, pady=2)
        tk.Label(notif_form, text="Message:").grid(row=2, column=0, padx=2, pady=2)
        
        self.notif_type_entry = tk.Entry(notif_form, width=30)
        self.notif_sender_entry = tk.Entry(notif_form, width=30)
        self.notif_msg_entry = tk.Entry(notif_form, width=30)
        
        self.notif_type_entry.grid(row=0, column=1, padx=5)
        self.notif_sender_entry.grid(row=1, column=1, padx=5)
        self.notif_msg_entry.grid(row=2, column=1, padx=5)

        btn_frame = tk.Frame(queue_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Send (Enqueue)", command=self.enqueue_notification, bg="#27ae60", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Process Next (Dequeue)", command=self.dequeue_notification, bg="#2980b9", fg="white").grid(row=0, column=1, padx=5)

        tk.Label(queue_frame, text="Pending Notifications (Oldest Top):").pack(pady=10)
        self.notif_list_box = tk.Listbox(queue_frame, width=50, height=8)
        self.notif_list_box.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)
        self.show_notifications()

    def show_activity_log(self):
        self.activity_log_box.delete(0, tk.END)
        items = self.activity_stack.get_all()
        for item in items:
            display = f"[{item['type']}] {item['user']}: {item['details']} ({item['time'].split(' ')[1]})"
            self.activity_log_box.insert(tk.END, display)

    def pop_activity(self):
        version, data = self.activity_stack.pop()
        if data:
            messagebox.showinfo("Pop Success", f"Cleared Activity (V{version}): {data['type']} by {data['user']}")
            self.show_activity_log()
        elif version == self.activity_stack.current_version:
            messagebox.showwarning("Warning", "Activity log is empty.")

    def enqueue_notification(self):
        notif_type = self.notif_type_entry.get().strip().upper() or "INFO"
        sender = self.notif_sender_entry.get().strip() or "System"
        message = self.notif_msg_entry.get().strip()
        
        if not message:
            messagebox.showwarning("Warning", "Notification message cannot be empty.")
            return

        version = self.notification_queue.enqueue(notif_type, sender, message)
        
        self.notif_type_entry.delete(0, tk.END)
        self.notif_sender_entry.delete(0, tk.END)
        self.notif_msg_entry.delete(0, tk.END)
        self.show_notifications()
        
        self.activity_stack.push("NOTIFICATION_SENT", sender, f"Sent notif: '{message[:15]}...'")
        self.show_activity_log()

    def dequeue_notification(self):
        version, data = self.notification_queue.dequeue()
        if data:
            messagebox.showinfo("Processed", f"Processed Notification (V{version}): {data['type']} from {data['sender']}")
            self.show_notifications()
            self.activity_stack.push("NOTIFICATION_READ", data['sender'], f"Read notif: '{data['message'][:15]}...'")
            self.show_activity_log()
        elif version == self.notification_queue.current_version:
            messagebox.showwarning("Warning", "No pending notifications.")

    def show_notifications(self):
        self.notif_list_box.delete(0, tk.END)
        for item in self.notification_queue.get_all():
            display = f"[{item['type']}] From {item['sender']}: {item['message']} ({item['time'].split(' ')[1]})"
            self.notif_list_box.insert(tk.END, display)

    # =====================================================
    #  HISTORY TAB - ENHANCED WITH TIME TRAVEL
    # =====================================================
    def setup_history_tab(self):
        frame = self.tab_history
        tk.Label(frame, text="Graph Version History & Time Travel", font=("Arial", 16, "bold")).pack(pady=10)
        
        info = tk.Label(frame, text="View and restore previous versions of the social graph.", 
                       font=("Arial", 10), fg="#7f8c8d")
        info.pack(pady=5)
        
        # Current version info
        self.version_label = tk.Label(frame, text=f"Current Version: {self.graph.version}", 
                                     font=("Arial", 12, "bold"), fg="#27ae60")
        self.version_label.pack(pady=5)
        
        # Buttons
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="🔄 Refresh History", command=self.show_versions, 
                 bg="#3498db", fg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="⏮️ Time Travel to Selected", command=self.time_travel, 
                 bg="#9b59b6", fg="white", font=("Arial", 10)).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="📊 View Selected Version", command=self.preview_version, 
                 bg="#16a085", fg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        
        # Version history table
        columns = ("Version", "Users", "Friendships", "Timestamp")
        self.history_tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        
        self.history_tree.heading("Version", text="Version")
        self.history_tree.heading("Users", text="Users")
        self.history_tree.heading("Friendships", text="Friendships")
        self.history_tree.heading("Timestamp", text="Saved At")
        
        self.history_tree.column("Version", width=100, anchor="center")
        self.history_tree.column("Users", width=100, anchor="center")
        self.history_tree.column("Friendships", width=120, anchor="center")
        self.history_tree.column("Timestamp", width=200, anchor="center")
        
        self.history_tree.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Details panel
        detail_frame = ttk.LabelFrame(frame, text="Version Details", padding="10")
        detail_frame.pack(pady=10, padx=20, fill="x")
        
        self.version_detail_text = scrolledtext.ScrolledText(detail_frame, width=90, height=8, 
                                                             wrap=tk.WORD, font=("Courier", 9))
        self.version_detail_text.pack(fill="both", expand=True)
        
        # Bind selection event
        self.history_tree.bind('<<TreeviewSelect>>', self.on_version_select)
        
        self.show_versions()

    def show_versions(self):
        """Display all saved versions in the history table."""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Update current version label
        self.version_label.config(text=f"Current Version: {self.graph.version}")
        
        # Populate table
        for version_id in sorted(self.version_control.versions.keys()):
            g = self.version_control.versions[version_id]
            users = len(g.adj)
            friendships = sum(len(data["friends"]) for data in g.adj.values()) // 2
            
            # Create timestamp (using version as placeholder since we don't store actual timestamps)
            timestamp = f"Version {version_id}"
            
            # Highlight current version
            tag = "current" if version_id == self.graph.version else ""
            
            self.history_tree.insert("", "end", values=(version_id, users, friendships, timestamp), 
                                    tags=(tag,))
        
        # Style current version
        self.history_tree.tag_configure("current", background="#d5f4e6", foreground="#27ae60", 
                                       font=("Arial", 10, "bold"))

    def on_version_select(self, event):
        """Handle version selection in the tree."""
        selection = self.history_tree.selection()
        if not selection:
            return
        
        item = self.history_tree.item(selection[0])
        version_id = int(item['values'][0])
        
        # Show details
        self.show_version_details(version_id)

    def show_version_details(self, version_id):
        """Display detailed information about a specific version."""
        self.version_detail_text.delete(1.0, tk.END)
        
        g = self.version_control.get(version_id)
        if not g:
            self.version_detail_text.insert(tk.END, "Version not found.")
            return
        
        self.version_detail_text.insert(tk.END, f"{'='*70}\n")
        self.version_detail_text.insert(tk.END, f"VERSION {version_id} DETAILS\n")
        self.version_detail_text.insert(tk.END, f"{'='*70}\n\n")
        
        self.version_detail_text.insert(tk.END, f"Total Users: {len(g.adj)}\n")
        
        friendships = sum(len(data["friends"]) for data in g.adj.values()) // 2
        self.version_detail_text.insert(tk.END, f"Total Friendships: {friendships}\n\n")
        
        if g.adj:
            self.version_detail_text.insert(tk.END, f"{'-'*70}\n")
            self.version_detail_text.insert(tk.END, "Users and Their Friends:\n\n")
            
            for user_id in sorted(g.adj.keys()):
                data = g.adj[user_id]
                name = data["name"]
                friends = sorted(data["friends"])
                
                self.version_detail_text.insert(tk.END, f"• {name} ({user_id})\n")
                if friends:
                    friend_names = [f"{g.adj[f]['name']} ({f})" for f in friends]
                    self.version_detail_text.insert(tk.END, f"  Friends: {', '.join(friend_names)}\n")
                else:
                    self.version_detail_text.insert(tk.END, f"  Friends: None\n")
                self.version_detail_text.insert(tk.END, "\n")
        else:
            self.version_detail_text.insert(tk.END, "No users in this version.\n")

    def preview_version(self):
        """Preview the selected version without making it current."""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a version to preview.")
            return
        
        item = self.history_tree.item(selection[0])
        version_id = int(item['values'][0])
        
        self.show_version_details(version_id)

    def time_travel(self):
        """Restore a previous version as the current graph."""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a version to restore.")
            return
        
        item = self.history_tree.item(selection[0])
        version_id = int(item['values'][0])
        
        if version_id == self.graph.version:
            messagebox.showinfo("Already Current", "This version is already the current version.")
            return
        
        # Confirm action
        result = messagebox.askyesno("Time Travel Confirmation", 
                                     f"Are you sure you want to restore Version {version_id}?\n\n"
                                     f"This will make Version {version_id} your current working version.\n"
                                     f"Your current Version {self.graph.version} will remain in history.")
        
        if result:
            # Get the version from history
            old_graph = self.version_control.get(version_id)
            if old_graph:
                # Set it as current
                self.graph = old_graph
                
                # Rebuild union-find from this version
                self.union_find = UnionFind()
                for u in self.graph.get_all_users():
                    self.union_find.make_set(u)
                    for f in self.graph.get_friends(u):
                        self.union_find.union(u, f)
                
                # Log activity
                self.activity_stack.push("TIME_TRAVEL", 0, f"Restored to Version {version_id}")
                self.show_activity_log()
                
                messagebox.showinfo("Time Travel Complete", 
                                  f"Successfully restored to Version {version_id}!\n\n"
                                  f"All tabs now reflect this version.")
                
                # Refresh all displays
                self.show_versions()
                self.show_all_users()
                self.show_all_friendships()
            else:
                messagebox.showerror("Error", "Could not retrieve version from history.")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SocialVerseApp(root)
    root.mainloop()