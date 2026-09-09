from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel


class TreeNode:

    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.children = []

    def add_child(self, node):
        self.children.append(node)


class JsonModel(QAbstractItemModel):
    """Hierarchical model for JSON objects, arrays, and leaf values."""

    VALUE_TYPES = (
        ("object", {}),
        ("array", []),
        ("string", ""),
        ("integer", 0),
        ("float", 0.0),
        ("boolean", False),
        ("null", None),
    )

    def __init__(self, data=None, parent=None):
        super().__init__(parent)

        if data is None:
            data = {}

        self.root = TreeNode("root", data)
        self.create_tree(self.root, data)

    def create_tree(self, parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                node = TreeNode(key, value, parent)
                parent.add_child(node)
                if isinstance(value, (dict, list)):
                    self.create_tree(node, value)

        elif isinstance(data, list):
            for i, value in enumerate(data):
                node = TreeNode(str(i), value, parent)
                parent.add_child(node)
                if isinstance(value, (dict, list)):
                    self.create_tree(node, value)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def rowCount(self, parent=QModelIndex()):
        node = self._node_from_index(parent)
        return len(node.children)

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        node = self._node_from_index(parent)
        child = node.children[row]
        return self.createIndex(row, column, child)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        node = index.internalPointer()
        parent = node.parent

        if parent is None or parent is self.root:
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

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        node = index.internalPointer()

        if index.column() == 1 and self._is_editable_leaf(node.value):
            flags |= Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole or not index.isValid():
            return False

        node = index.internalPointer()

        if isinstance(node.value, bool):
            node.value = bool(value)
        elif isinstance(node.value, int) and not isinstance(node.value, bool):
            node.value = int(value)
        elif isinstance(node.value, float):
            node.value = float(value)
        elif isinstance(node.value, str):
            node.value = str(value)
        else:
            return False

        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None

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
            return [self.get_json(child) for child in node.children]

        return node.value

    def add_child(self, parent_index: QModelIndex, key: str, value):
        parent = self._node_from_index(parent_index)

        if not isinstance(parent.value, (dict, list)):
            return QModelIndex()

        if isinstance(parent.value, list):
            key = str(len(parent.children))
        elif key in {child.key for child in parent.children}:
            return QModelIndex()

        row = len(parent.children)
        self.beginInsertRows(parent_index, row, row)

        child = TreeNode(key, value, parent)
        parent.add_child(child)
        if isinstance(value, (dict, list)):
            self.create_tree(child, value)

        self.endInsertRows()
        return self.createIndex(row, 0, child)

    def remove_node(self, index: QModelIndex) -> bool:
        if not index.isValid():
            return False

        node = index.internalPointer()
        parent = node.parent
        if parent is None:
            return False

        row = parent.children.index(node)
        parent_index = self.parent(index)

        self.beginRemoveRows(parent_index, row, row)
        parent.children.pop(row)

        if isinstance(parent.value, list):
            for i, child in enumerate(parent.children):
                child.key = str(i)

        self.endRemoveRows()

        if isinstance(parent.value, list) and parent.children:
            first = self.index(0, 0, parent_index)
            last = self.index(len(parent.children) - 1, 0, parent_index)
            self.dataChanged.emit(first, last, [Qt.DisplayRole])

        return True

    def container_index_for_add(self, index: QModelIndex) -> QModelIndex:
        """Return an object/array index suitable for inserting a child."""
        if not index.isValid():
            if isinstance(self.root.value, (dict, list)):
                return QModelIndex()
            return None

        node = index.internalPointer()
        if isinstance(node.value, (dict, list)):
            return index

        return self.parent(index)

    @staticmethod
    def default_value_for_type(type_name: str):
        for name, value in JsonModel.VALUE_TYPES:
            if name == type_name:
                if isinstance(value, (dict, list)):
                    return value.__class__()
                return value
        return ""

    @staticmethod
    def type_names():
        return [name for name, _ in JsonModel.VALUE_TYPES]

    @staticmethod
    def _is_editable_leaf(value) -> bool:
        if value is None:
            return False
        if isinstance(value, (dict, list)):
            return False
        return isinstance(value, (str, int, float, bool))

    def _node_from_index(self, index: QModelIndex) -> TreeNode:
        if index.isValid():
            return index.internalPointer()
        return self.root
