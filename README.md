# SocialVerceApp
🌐 SocialVerse – Data Structures Based Social Network Simulator

SocialVerse is a GUI-based social network simulation system built using Python and Tkinter, designed to demonstrate the practical application of core Data Structures and Algorithms (DSA).
The project integrates graphs, disjoint sets, trees, stacks, queues, and persistent data structures into a single cohesive application.

🚀 Features
👤 User Management (Binary Search Tree)

Add, search, and display users efficiently

Users are stored using a Binary Search Tree (BST) for fast lookup and traversal

🤝 Friendship Management (Graph)

Users and friendships are modeled using a graph data structure

Add and remove friendships dynamically

Find mutual friends between users

Visual representation of all friendships

🌐 Community Detection (Disjoint Set Union – Union-Find)

Automatically detects communities (connected components) in the social graph

Uses Union-Find (Disjoint Sets) for efficient grouping

Displays each community with its members and friend counts

📝 Posts & Feed (Persistent Linked List)

Users can create posts

Supports undo and redo functionality

Implemented using a persistent linked list

📌 Activity Log (Stack)

Tracks user activities such as:

User creation

Friend addition/removal

Community detection

Time travel actions

Implemented using a stack (LIFO)

🔔 Notifications (Queue)

Notification system for system/user messages

FIFO processing using a queue

Supports enqueue and dequeue operations

🕒 Version Control & Time Travel (Persistent Graph)

Every graph modification creates a new version

View all previous versions of the social graph

Restore any previous version using time travel

Ensures immutability and persistence

🧠 Data Structures Used
Feature	Data Structure
User Storage	Binary Search Tree (BST)
Friendships	Graph
Community Detection	Disjoint Set Union (Union-Find)
Feed System	Persistent Linked List
Activity Log	Stack
Notifications	Queue
Version History	Persistent Graph
🛠️ Technologies Used

Python 3

Tkinter (GUI)

Object-Oriented Programming (OOP)

Persistent Data Structures

📂 Project Structure
DSA_PROJECT_EVALUATION/
│
├── main.py                          # Main GUI application
├── module1_persistent_graph.py      # Graph, Version Control, Union-Find
├── module2_persistent_linkedlist.py # Persistent Linked List (Feed)
├── module3_bst.py                   # Binary Search Tree (Users)
├── module4_stack_queue.py           # Stack (Activity) & Queue (Notifications)
└── README.md

▶️ How to Run

Make sure Python 3 is installed

Clone or download the project

Navigate to the project directory

Run the application:

python main.py

📸 Application Modules

Users Tab – Manage users using BST

Friendships Tab – Add/remove friendships, find mutual friends

Communities Tab – Detect communities using Union-Find

Posts / Feed Tab – Add posts with undo/redo

Activity / Notifications Tab – Stack & Queue operations

Version History Tab – Time travel across graph versions

🎯 Learning Outcomes

Hands-on understanding of core data structures

Real-world application of graphs and disjoint sets

Experience with persistent data structures

Improved understanding of DSA integration with GUI applications

Practical exposure to modular and scalable system design

📌 Academic Relevance

This project was developed as part of a Data Structures & Algorithms (DSA) course evaluation and demonstrates the use of multiple data structures in a unified, real-world-inspired application.

👨‍💻 Author

K Sai Siddhartha Reddy

(Data Structures & Algorithms Project)
