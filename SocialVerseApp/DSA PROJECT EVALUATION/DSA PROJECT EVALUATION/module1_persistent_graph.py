"""
SocialVerse - Simplified Persistent Graph with Union-Find
References:
- Driscoll et al. (1989). "Making Data Structures Persistent"
- Conchon & Filliâtre (2007). "A Persistent Union-Find Data Structure"
"""

from typing import Dict, Set
from copy import deepcopy


class PersistentGraph:
    """Persistent Graph using Path Copying (each update → new version)."""

    def __init__(self, version=0):
        self.version = version
        self.adj: Dict[str, Dict] = {}

    def _copy(self):
        new_graph = PersistentGraph(self.version)
        new_graph.adj = deepcopy(self.adj)
        return new_graph

    def add_user(self, user_id, name):
        new_graph = self._copy()
        new_graph.version += 1
        new_graph.adj[user_id] = {"name": name, "friends": set()}
        return new_graph

    def add_friendship(self, user1, user2):
        if user1 not in self.adj or user2 not in self.adj:
            raise ValueError("Both users must exist.")
        new_graph = self._copy()
        new_graph.version += 1
        new_graph.adj[user1]["friends"].add(user2)
        new_graph.adj[user2]["friends"].add(user1)
        return new_graph

    def remove_friendship(self, user1, user2):
        if user1 not in self.adj or user2 not in self.adj:
            raise ValueError("Both users must exist.")
        new_graph = self._copy()
        new_graph.version += 1
        new_graph.adj[user1]["friends"].discard(user2)
        new_graph.adj[user2]["friends"].discard(user1)
        return new_graph

    def get_friends(self, user_id):
        return self.adj.get(user_id, {}).get("friends", set())

    def find_mutual_friends(self, user1, user2):
        return self.get_friends(user1) & self.get_friends(user2)

    def user_exists(self, user_id):
        return user_id in self.adj

    def get_user_name(self, user_id):
        return self.adj.get(user_id, {}).get("name")

    def get_all_users(self):
        return list(self.adj.keys())

    def display(self):
        print("\n" + "=" * 60)
        print(f"[GRAPH] VERSION {self.version}")
        print("=" * 60)

        total_users = len(self.adj)
        total_friendships = sum(len(d["friends"]) for d in self.adj.values()) // 2
        print(f"Users: {total_users} | Friendships: {total_friendships}\n")

        for user, data in sorted(self.adj.items()):
            friends = [self.adj[f]["name"] for f in sorted(data["friends"])]
            if friends:
                print(f"  {data['name']:12} -> {', '.join(friends)}")
            else:
                print(f"  {data['name']:12} -> No friends yet")


class UnionFind:
    """Persistent Union-Find (unchanged)."""

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, user):
        self.parent[user] = user
        self.rank[user] = 0

    def find(self, user):
        if user not in self.parent:
            return None
        if self.parent[user] != user:
            self.parent[user] = self.find(self.parent[user])
        return self.parent[user]

    def union(self, user1, user2):
        root1 = self.find(user1)
        root2 = self.find(user2)

        if root1 is None or root2 is None or root1 == root2:
            return

        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1

    def get_communities(self):
        communities = {}
        for user in self.parent:
            root = self.find(user)
            if root not in communities:
                communities[root] = []
            communities[root].append(user)
        return communities

    def display(self):
        print("\n" + "=" * 60)
        print("[COMMUNITIES] Union-Find Results")
        print("=" * 60)

        communities = self.get_communities()
        print(f"Total Communities: {len(communities)}\n")

        for i, members in enumerate(communities.values(), 1):
            print(f"  Community {i}: {', '.join(sorted(members))}")


class VersionControl:
    """Manages different graph versions."""

    def __init__(self):
        self.versions = {}
        self.current = 0

    def save(self, graph):
        self.versions[graph.version] = graph
        self.current = graph.version

    def get(self, version_id):
        return self.versions.get(version_id)

    def list(self):
        print("\n" + "=" * 60)
        print("[VERSION HISTORY]")
        print("=" * 60)
        for vid, g in sorted(self.versions.items()):
            friends = sum(len(d["friends"]) for d in g.adj.values()) // 2
            print(f"  Version {vid}: {len(g.adj)} users, {friends} friendships")


def main():
    print("=" * 60)
    print("     SocialVerse - Persistent Graph System")
    print("=" * 60)

    current_graph = PersistentGraph(0)
    vc = VersionControl()
    vc.save(current_graph)

    while True:
        print("\n" + "=" * 60)
        print("[MENU]")
        print("=" * 60)
        print("1. Add User")
        print("2. Add Friendship")
        print("3. Remove Friendship")
        print("4. Display Graph")
        print("5. Find Mutual Friends")
        print("6. Detect Communities")
        print("7. View Version History")
        print("8. Time Travel to Version")
        print("9. Exit")

        choice = input("\nEnter your choice (1-9): ").strip()

        if choice == '1':
            user_id = input("Enter User ID: ").strip()
            name = input("Enter Name: ").strip()

            if current_graph.user_exists(user_id):
                print("User already exists!")
            else:
                current_graph = current_graph.add_user(user_id, name)
                vc.save(current_graph)
                print(f"Added {name} (Version {current_graph.version})")

        elif choice == '2':
            u1 = input("Enter User 1 ID: ").strip()
            u2 = input("Enter User 2 ID: ").strip()

            try:
                current_graph = current_graph.add_friendship(u1, u2)
                vc.save(current_graph)
                print(f"Friendship added between {u1} and {u2} (Version {current_graph.version})")
            except ValueError as e:
                print(e)

        elif choice == '3':
            u1 = input("Enter User 1 ID: ").strip()
            u2 = input("Enter User 2 ID: ").strip()

            try:
                current_graph = current_graph.remove_friendship(u1, u2)
                vc.save(current_graph)
                print(f"Friendship removed between {u1} and {u2} (Version {current_graph.version})")
            except ValueError as e:
                print(e)

        elif choice == '4':
            current_graph.display()

        elif choice == '5':
            u1 = input("Enter User 1 ID: ").strip()
            u2 = input("Enter User 2 ID: ").strip()
            mutual = current_graph.find_mutual_friends(u1, u2)

            if mutual:
                mutual_names = [current_graph.get_user_name(u) for u in mutual]
                print("Mutual Friends:", ', '.join(mutual_names))
            else:
                print("No mutual friends found.")

        elif choice == '6':
            uf = UnionFind()
            for u in current_graph.get_all_users():
                uf.make_set(u)
            for u in current_graph.get_all_users():
                for f in current_graph.get_friends(u):
                    uf.union(u, f)
            uf.display()

        elif choice == '7':
            vc.list()

        elif choice == '8':
            vc.list()
            v = input("Enter version number: ").strip()

            if v.isdigit() and int(v) in vc.versions:
                graph = vc.get(int(v))
                graph.display()
                if input("Make this current? (y/n): ").lower() == 'y':
                    current_graph = graph
            else:
                print("Invalid version.")

        elif choice == '9':
            print("\nExiting SocialVerse. All versions preserved.")
            break

        else:
            print("Invalid choice! Enter a number between 1-9.")


if __name__ == "__main__":
    main()
