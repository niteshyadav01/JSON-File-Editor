from PySide6.QtWidgets import (
    QStyledItemDelegate,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
)
from PySide6.QtCore import Qt


class JsonDelegate(QStyledItemDelegate):
    """Type-safe editors for JSON leaf values."""

    def createEditor(self, parent, option, index):
        if index.column() != 1:
            return None

        node = index.data(Qt.UserRole)
        if node is None:
            return None

        value = node.value

        if isinstance(value, bool):
            return QCheckBox(parent)

        if isinstance(value, int) and not isinstance(value, bool):
            box = QSpinBox(parent)
            box.setMinimum(-2147483648)
            box.setMaximum(2147483647)
            return box

        if isinstance(value, float):
            box = QDoubleSpinBox(parent)
            box.setDecimals(6)
            box.setRange(-1e12, 1e12)
            return box

        if isinstance(value, str):
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
