from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QInputDialog,
)
from models.json_model import JsonModel
from delegates.json_delegate import JsonDelegate
from services.json_service import JsonService
from .win_main import Ui_MainWindow


class MainWindow(QMainWindow):
    """GUI controller: wires Designer widgets to model and JSON service."""

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = None
        self.file_name = ""

        self.ui.listView.setItemDelegate(JsonDelegate(self.ui.listView))
        self.ui.splitter.setStretchFactor(0, 3)
        self.ui.splitter.setStretchFactor(1, 2)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open JSON File",
            "",
            "JSON Files (*.json)",
        )
        if not file_name:
            return

        try:
            data = JsonService.load(file_name)
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))
            return

        self._set_model(data)
        self.file_name = file_name
        self.setWindowTitle(f"JSON Editor - {file_name}")
        self.ui.statusbar.showMessage("File loaded successfully")

    def save_file(self):
        if self.model is None:
            QMessageBox.warning(self, "Warning", "Please open a JSON file first")
            return

        if not self.file_name:
            self.save_as()
            return

        try:
            JsonService.save(self.file_name, self.model.get_json())
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))
            return

        self.ui.statusbar.showMessage("File saved successfully")

    def save_as(self):
        if self.model is None:
            QMessageBox.warning(self, "Warning", "Please open a JSON file first")
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON File",
            "",
            "JSON Files (*.json)",
        )
        if not file_name:
            return

        try:
            saved_path = JsonService.save(file_name, self.model.get_json())
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))
            return

        self.file_name = saved_path
        self.setWindowTitle(f"JSON Editor - {saved_path}")
        self.ui.statusbar.showMessage("File saved successfully")

    def add_item(self):
        if self.model is None:
            QMessageBox.warning(self, "Warning", "Please open a JSON file first")
            return

        current = self.ui.listView.currentIndex()
        parent_index = self.model.container_index_for_add(current)
        if parent_index is None:
            QMessageBox.warning(
                self,
                "Warning",
                "Select an object or array (or one of its children) to add into",
            )
            return

        parent_node = (
            parent_index.internalPointer()
            if parent_index.isValid()
            else self.model.root
        )

        type_name, ok = QInputDialog.getItem(
            self,
            "Add Value",
            "Type:",
            JsonModel.type_names(),
            0,
            False,
        )
        if not ok:
            return

        key = ""
        if isinstance(parent_node.value, dict):
            key, ok = QInputDialog.getText(self, "Add Value", "Key:")
            if not ok or not key.strip():
                return
            key = key.strip()

        value = JsonModel.default_value_for_type(type_name)
        new_index = self.model.add_child(parent_index, key, value)
        if not new_index.isValid():
            QMessageBox.warning(self, "Warning", "Could not add item (duplicate key?)")
            return

        self.ui.listView.setCurrentIndex(new_index)
        self.ui.listView.expand(parent_index)
        self.ui.statusbar.showMessage("Item added")

    def delete_item(self):
        if self.model is None:
            QMessageBox.warning(self, "Warning", "Please open a JSON file first")
            return

        index = self.ui.listView.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Warning", "Select an item to delete")
            return

        if not self.model.remove_node(index):
            QMessageBox.warning(self, "Warning", "Could not delete the selected item")
            return

        self.ui.statusbar.showMessage("Item deleted")

    def _set_model(self, data):
        self.model = JsonModel(data)
        self.ui.listView.setModel(self.model)
        self.model.dataChanged.connect(self._refresh_preview)
        self.model.rowsInserted.connect(self._refresh_preview)
        self.model.rowsRemoved.connect(self._refresh_preview)
        self.model.modelReset.connect(self._refresh_preview)
        self._refresh_preview()

    def _refresh_preview(self, *args):
        if self.model is None:
            self.ui.jsonPreview.clear()
            return
        self.ui.jsonPreview.setPlainText(JsonService.dumps(self.model.get_json()))
