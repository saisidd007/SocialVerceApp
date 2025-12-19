class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class Version:
    def __init__(self, head=None, note="Initial version"):
        self.head = head
        self.note = note

    def view(self):
        values = []
        current = self.head
        while current:
            values.append(current.data)
            current = current.next
        return values


class PersistentLinkedList:
    def __init__(self):
        self.versions = [Version()]
        self.undo_stack = []
        self.redo_stack = []

    def add(self, version_index, data):
        old = self.versions[version_index]
        new_head = Node(data, old.head)
        self.versions.append(Version(new_head, f"Added '{data}'"))
        self.undo_stack.append(version_index)
        self.redo_stack.clear()

    def add_post(self, data):
        """Convenience method to add to the latest version"""
        self.add(self.latest_version(), data)


    def delete(self, version_index):
        old = self.versions[version_index]
        if old.head is None:
            new = Version(None, "Delete attempted on empty list")
        else:
            deleted = old.head.data
            new = Version(old.head.next, f"Deleted '{deleted}'")
        self.versions.append(new)
        self.undo_stack.append(version_index)
        self.redo_stack.clear()

    def view(self, version_index):
        if version_index >= len(self.versions):
            print(f"Version {version_index} does not exist.")
            return
        version = self.versions[version_index]
        print(f"\nVersion {version_index}: {version.note}")
        values = version.view()
        if values:
            print(" -> ".join(str(v) for v in values))
        else:
            print("(Empty List)")

    def latest_version(self):
        return len(self.versions) - 1

    def undo(self):
        if not self.undo_stack:
            print("Nothing to undo.")
            return
        last = self.undo_stack.pop()
        current = self.latest_version()
        reverted = self.versions[last]
        self.versions.append(Version(reverted.head, f"Undo → version {last}"))
        self.redo_stack.append(current)

    def redo(self):
        if not self.redo_stack:
            print("Nothing to redo.")
            return
        redo_v = self.redo_stack.pop()
        reapplied = self.versions[redo_v]
        self.versions.append(Version(reapplied.head, f"Redo → version {redo_v}"))
        self.undo_stack.append(redo_v)

    def compare(self, v1, v2):
        if v1 >= len(self.versions) or v2 >= len(self.versions):
            print("Invalid version numbers.")
            return
        list1 = self.versions[v1].view()
        list2 = self.versions[v2].view()
        added = [x for x in list2 if x not in list1]
        removed = [x for x in list1 if x not in list2]
        print(f"\nComparing Version {v1} and Version {v2}:")
        if not added and not removed:
            print("No changes.")
        else:
            if added:
                print(f"Added: {added}")
            if removed:
                print(f"Removed: {removed}")

