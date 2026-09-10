import json

from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel

from gui.win_main import Ui_MainWindow


class TreeNode:

    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.children = []

    def addChild(self, node):
        self.children.append(node)


class JsonModel(QAbstractItemModel):

    def __init__(self, data=None):
        super().__init__()
        self.root = TreeNode("root", data)
        if data is not None:
            self.buildTree(self.root, data)

    def buildTree(self, parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                node = TreeNode(key, value, parent)
                parent.addChild(node)
                if isinstance(value, (dict, list)):
                    self.buildTree(node, value)

        elif isinstance(data, list):
            for i, value in enumerate(data):
                node = TreeNode(str(i), value, parent)
                parent.addChild(node)
                if isinstance(value, (dict, list)):
                    self.buildTree(node, value)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            node = parent.internalPointer()
        else:
            node = self.root
        return len(node.children)

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if parent.isValid():
            node = parent.internalPointer()
        else:
            node = self.root

        return self.createIndex(row, column, node.children[row])

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

   
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None

        if index.column() == 0:
            return node.key

        if isinstance(node.value, dict):
            return "{ }"
        if isinstance(node.value, list):
            return "[ ]"
        if node.value is None:
            return "null"
        if isinstance(node.value, bool):
            return str(node.value).lower()

        return str(node.value)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        node = index.internalPointer()

        # only leaf values are editable
        if index.column() == 1 and isinstance(node.value, (str, int, float, bool)):
            flags |= Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole or not index.isValid():
            return False

        node = index.internalPointer()

        try:
            if isinstance(node.value, bool):
                if isinstance(value, bool):
                    node.value = value
                else:
                    text = str(value).strip().lower()
                    if text not in ("true", "false", "1", "0"):
                        return False
                    node.value = text in ("true", "1")
            elif isinstance(node.value, int):
                node.value = int(value)
            elif isinstance(node.value, float):
                node.value = float(value)
            elif isinstance(node.value, str):
                node.value = str(value)
            else:
                return False
        except (ValueError, TypeError):
            return False

        self.dataChanged.emit(index, index)
        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None
        if section == 0:
            return "Key"
        if section == 1:
            return "Value"
        return None

    def getJson(self, node=None):
        if node is None:
            node = self.root

        if isinstance(node.value, dict):
            data = {}
            for child in node.children:
                data[child.key] = self.getJson(child)
            return data

        if isinstance(node.value, list):
            data = []
            for child in node.children:
                data.append(self.getJson(child))
            return data

        return node.value


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = None
        self.fileName = ""

        self.ui.actionopen.triggered.connect(self.uploadFile)
        self.ui.actionedit.triggered.connect(self.saveFile)
        self.ui.actionSave_As.triggered.connect(self.saveAs)

    def uploadFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open JSON File",
            "",
            "JSON Files (*.json)"
        )

        if not fileName:
            return

        try:
            with open(fileName, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.model = JsonModel(data)
            self.ui.listView.setModel(self.model)
            self.ui.listView.setColumnWidth(0, 250)
            self.ui.listView.setColumnWidth(1, 400)

            self.fileName = fileName
            self.setWindowTitle("JSON Editor - " + fileName)
            self.ui.statusbar.showMessage("File loaded")

        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Invalid JSON file")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def saveFile(self):
        if self.model is None:
            QMessageBox.warning(self, "Warning", "Upload a JSON file first")
            return

        if not self.fileName:
            self.saveAs()
            return

        try:
            with open(self.fileName, "w", encoding="utf-8") as f:
                json.dump(self.model.getJson(), f, indent=4, ensure_ascii=False)
            self.ui.statusbar.showMessage("File saved")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def saveAs(self):
        if self.model is None:
            QMessageBox.warning(self, "Warning", "Upload a JSON file first")
            return

        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON File",
            "",
            "JSON Files (*.json)"
        )

        if not fileName:
            return

        if not fileName.endswith(".json"):
            fileName += ".json"

        try:
            with open(fileName, "w", encoding="utf-8") as f:
                json.dump(self.model.getJson(), f, indent=4, ensure_ascii=False)

            self.fileName = fileName
            self.setWindowTitle("JSON Editor - " + fileName)
            self.ui.statusbar.showMessage("File saved")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
