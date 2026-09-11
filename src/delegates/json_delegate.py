from PySide6.QtWidgets import (
    QStyledItemDelegate,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
)
from PySide6.QtCore import Qt


class JsonDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):

        if index.column() != 1:
            return None

        node = index.data(Qt.UserRole)

        if isinstance(node.value, bool):
            return QCheckBox(parent)

        if isinstance(node.value, int):
            return QSpinBox(parent)

        if isinstance(node.value, float):
            box = QDoubleSpinBox(parent)
            box.setDecimals(2)
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
