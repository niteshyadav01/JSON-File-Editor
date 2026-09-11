from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
)

from models.tree_model import TreeModel
from models.tree_node import TreeNode
from delegates.json_delegate import JsonDelegate
from services.json_service import JsonService
from win_main_ui import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.mUi = Ui_MainWindow()
        self.mUi.setupUi(self)

        self.mModel = None
        self.mFileName = ""

        self.mUi.listView.setItemDelegate(JsonDelegate(self.mUi.listView))

        self.mUi.actionopen.triggered.connect(self.openFile)
        self.mUi.actionedit.triggered.connect(self.saveFile)
        self.mUi.actionSave_As.triggered.connect(self.saveAs)

    def openFile(self):

        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open JSON File",
            "",
            "JSON Files (*.json)"
        )

        if not fileName:
            return

        try:
            data = JsonService.load(fileName)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.mModel = TreeModel()
        self.mModel.root = TreeNode("root", data)
        self.mModel.createTree(self.mModel.root, data)
        self.mUi.listView.setModel(self.mModel)

        self.mFileName = fileName
        self.setWindowTitle("JSON Editor - " + fileName)
        self.mUi.statusbar.showMessage("File loaded successfully")

    def saveFile(self):

        if self.mModel is None:
            QMessageBox.warning(
                self,
                "Warning",
                "Please open a JSON file first"
            )
            return

        if not self.mFileName:
            self.saveAs()
            return

        try:
            JsonService.save(self.mFileName, self.mModel.get_json())
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.mUi.statusbar.showMessage("File saved successfully")

    def saveAs(self):

        if self.mModel is None:
            QMessageBox.warning(
                self,
                "Warning",
                "Please open a JSON file first"
            )
            return

        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON File",
            "",
            "JSON Files (*.json)"
        )

        if not fileName:
            return

        try:
            savedPath = JsonService.save(fileName, self.mModel.get_json())
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.mFileName = savedPath
        self.setWindowTitle("JSON Editor - " + savedPath)
        self.mUi.statusbar.showMessage("File saved successfully")
