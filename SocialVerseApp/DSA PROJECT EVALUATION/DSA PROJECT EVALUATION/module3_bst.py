"""
module3_bst.py
Binary Search Tree implementation for SocialVerse.
Handles user data with (uid, name, email).
"""

class BSTNode:
    def __init__(self, uid, name, email):
        self.uid = uid
        self.name = name
        self.email = email
        self.left = None
        self.right = None

    def __repr__(self):
        return f"BSTNode({self.uid}, {self.name}, {self.email})"


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    # ------------------ INSERT ------------------
    def insert(self, uid, name, email):
        """Insert or update a node in the BST."""
        def _insert(node, uid, name, email):
            if node is None:
                self.size += 1
                return BSTNode(uid, name, email)
            if uid < node.uid:
                node.left = _insert(node.left, uid, name, email)
            elif uid > node.uid:
                node.right = _insert(node.right, uid, name, email)
            else:
                node.name = name
                node.email = email  # update existing
            return node

        self.root = _insert(self.root, uid, name, email)

    # ------------------ SEARCH ------------------
    def search(self, uid):
        """Search for a node by uid."""
        node = self.root
        while node:
            if uid == node.uid:
                return node
            elif uid < node.uid:
                node = node.left
            else:
                node = node.right
        return None

    # ------------------ DELETE ------------------
    def delete(self, uid):
        """Delete a node by uid."""
        def _min_value_node(node):
            current = node
            while current.left:
                current = current.left
            return current

        def _delete(node, uid):
            if node is None:
                return node
            if uid < node.uid:
                node.left = _delete(node.left, uid)
            elif uid > node.uid:
                node.right = _delete(node.right, uid)
            else:
                if node.left is None:
                    self.size -= 1
                    return node.right
                elif node.right is None:
                    self.size -= 1
                    return node.left
                temp = _min_value_node(node.right)
                node.uid, node.name, node.email = temp.uid, temp.name, temp.email
                node.right = _delete(node.right, temp.uid)
            return node

        self.root = _delete(self.root, uid)

    # ------------------ INORDER TRAVERSAL ------------------
    def inorder(self):
        """Return list of tuples (uid, name, email) in sorted order."""
        result = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append((node.uid, node.name, node.email))
                _inorder(node.right)
        _inorder(self.root)
        return result

    def __len__(self):
        return self.size