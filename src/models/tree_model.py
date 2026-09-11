from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel

from models.tree_node import TreeNode


class TreeModel(QAbstractItemModel):

    def __init__(self):
        super().__init__()

        self.root = TreeNode("root", None)

    def createTree(self, parent, data):

        if isinstance(data, dict):

            for key, value in data.items():

                node = TreeNode(key, value, parent)
                parent.add_child(node)

                if isinstance(value, (dict, list)):
                    self.createTree(node, value)

        elif isinstance(data, list):

            for i, value in enumerate(data):

                node = TreeNode(str(i), value, parent)
                parent.add_child(node)

                if isinstance(value, (dict, list)):
                    self.createTree(node, value)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def rowCount(self, parent=QModelIndex()):

        if not parent.isValid():
            node = self.root
        else:
            node = parent.internalPointer()

        return len(node.children)

    def index(self, row, column, parent=QModelIndex()):

        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if parent.isValid():
            node = parent.internalPointer()
        else:
            node = self.root

        child = node.children[row]

        return self.createIndex(row, column, child)

    def parent(self, index):

        if not index.isValid():
            return QModelIndex()

        node = index.internalPointer()
        parent = node.parent

        if parent is None or parent == self.root:
            return QModelIndex()

        row = parent.parent.children.index(parent)

        return self.createIndex(row, 0, parent)

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == Qt.UserRole:
            return node

        if role == Qt.DisplayRole:

            if index.column() == 0:
                return node.key

            if index.column() == 1:

                if isinstance(node.value, dict):
                    return "{ }"

                if isinstance(node.value, list):
                    return "[ ]"

                if node.value is None:
                    return "null"

                if isinstance(node.value, bool):
                    return str(node.value).lower()

                return str(node.value)

        return None

    def flags(self, aIndex):

        if not aIndex.isValid():
            return Qt.NoItemFlags

        if aIndex.column() == 1:
            return (
                Qt.ItemFlag.ItemIsEditable |
                Qt.ItemFlag.ItemIsEnabled |
                Qt.ItemFlag.ItemIsSelectable
            )

        return (
            Qt.ItemFlag.ItemIsEnabled |
            Qt.ItemFlag.ItemIsSelectable
        )

    def setData(self, index, value, role=Qt.EditRole):

        if role != Qt.EditRole:
            return False

        node = index.internalPointer()
        node.value = value

        self.dataChanged.emit(index, index)

        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:

            if section == 0:
                return "Key"

            if section == 1:
                return "Value"

        return None

    def get_json(self, node=None):

        if node is None:
            node = self.root

        if isinstance(node.value, dict):

            data = {}

            for child in node.children:
                data[child.key] = self.get_json(child)

            return data

        if isinstance(node.value, list):

            data = []

            for child in node.children:
                data.append(self.get_json(child))

            return data

        return node.value
