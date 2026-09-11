class TreeNode:

    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.children = []

    def add_child(self, node):
        self.children.append(node)
