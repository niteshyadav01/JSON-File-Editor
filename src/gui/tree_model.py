import sys
import json

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QStyledItemDelegate,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox
)

from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel

from .win_main import Ui_MainWindow

class TreeNode:

    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.children = []

    def add_child(self, node):
        self.children.append(node)


class JsonModel(QAbstractItemModel):

    def __init__(self, data=None):
        super().__init__()

        self.root = TreeNode("root", data)

        if data is not None:
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

    def flags(self, index):

        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        node = index.internalPointer()

        if index.column() == 1:

            if isinstance(node.value, (str, int, float, bool)):
                flags |= Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role=Qt.EditRole):

        if role != Qt.EditRole:
            return False

        node = index.internalPointer()

        if isinstance(node.value, bool):
            node.value = bool(value)

        elif isinstance(node.value, int):
            node.value = int(value)

        elif isinstance(node.value, float):
            node.value = float(value)

        elif isinstance(node.value, str):
            node.value = str(value)

        else:
            return False

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


class JsonDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):

        if index.column() != 1:
            return None

        node = index.data(Qt.UserRole)

        if isinstance(node.value, bool):
            return QCheckBox(parent)

        if isinstance(node.value, int):
            box = QSpinBox(parent)
            box.setMinimum(-2147483648)
            box.setMaximum(2147483647)
            return box

        if isinstance(node.value, float):
            box = QDoubleSpinBox(parent)
            box.setDecimals(6)
            return box

        if isinstance(node.value, str):
            return QLineEdit(parent)

        return None

    def setEditorData(self, editor, index):

        node = index.data(Qt.UserRole)
        value = node.value

        if isinstance(editor, QCheckBox):
            editor.setChecked(value)

        elif isinstance(editor, QSpinBox):
            editor.setValue(value)

        elif isinstance(editor, QDoubleSpinBox):
            editor.setValue(value)

        elif isinstance(editor, QLineEdit):
            editor.setText(value)

    def setModelData(self, editor, model, index):

        if isinstance(editor, QCheckBox):
            value = editor.isChecked()

        elif isinstance(editor, QSpinBox):
            value = editor.value()

        elif isinstance(editor, QDoubleSpinBox):
            value = editor.value()

        elif isinstance(editor, QLineEdit):
            value = editor.text()

        else:
            return

        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = None
        self.file_name = ""

        self.ui.actionopen.triggered.connect(self.open_file)
        self.ui.actionedit.triggered.connect(self.save_file)
        self.ui.actionSave_As.triggered.connect(self.save_as)

    def open_file(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open JSON File",
            "",
            "JSON Files (*.json)"
        )

        if not file_name:
            return

        try:

            with open(file_name, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.model = JsonModel(data)

            self.ui.listView.setModel(self.model)

            delegate = JsonDelegate(self.ui.listView)
            self.ui.listView.setItemDelegate(delegate)

            self.ui.listView.setColumnWidth(0, 250)
            self.ui.listView.setColumnWidth(1, 400)

            self.file_name = file_name

            self.ui.statusbar.showMessage(
                "File loaded successfully"
            )

            self.setWindowTitle(
                "JSON Editor - " + file_name
            )

        except json.JSONDecodeError:
            QMessageBox.critical(
                self,
                "Error",
                "Invalid JSON file"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def save_file(self):

        if self.model is None:
            QMessageBox.warning(
                self,
                "Warning",
                "Please open a JSON file first"
            )
            return

        if not self.file_name:
            self.save_as()
            return

        try:

            data = self.model.get_json()

            with open(
                self.file_name,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            self.ui.statusbar.showMessage(
                "File saved successfully"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def save_as(self):

        if self.model is None:
            QMessageBox.warning(
                self,
                "Warning",
                "Please open a JSON file first"
            )
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON File",
            "",
            "JSON Files (*.json)"
        )

        if not file_name:
            return

        if not file_name.endswith(".json"):
            file_name += ".json"

        try:

            data = self.model.get_json()

            with open(
                file_name,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            self.file_name = file_name

            self.ui.statusbar.showMessage(
                "File saved successfully"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )


