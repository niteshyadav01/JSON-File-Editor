from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
)

from models.tree_model import TreeModel
from delegates.json_delegate import JsonDelegate
from services.json_service import JsonService
from win_main_ui import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = None
        self.file_name = ""

        self.ui.listView.setItemDelegate(JsonDelegate(self.ui.listView))

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
            data = JsonService.load(file_name)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.model = TreeModel(data)
        self.ui.listView.setModel(self.model)
        self.ui.listView.setColumnWidth(0, 250)
        self.ui.listView.setColumnWidth(1, 400)

        self.file_name = file_name
        self.setWindowTitle("JSON Editor - " + file_name)
        self.ui.statusbar.showMessage("File loaded successfully")

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
            JsonService.save(self.file_name, self.model.get_json())
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.ui.statusbar.showMessage("File saved successfully")

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

        try:
            saved_path = JsonService.save(file_name, self.model.get_json())
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.file_name = saved_path
        self.setWindowTitle("JSON Editor - " + saved_path)
        self.ui.statusbar.showMessage("File saved successfully")
