import json

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QPlainTextEdit,
    QLabel,
    QFileDialog,
    QMessageBox,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_file = None

        self.setWindowTitle("JSON Editor")
        self.resize(1000, 700)

        self.create_ui()

    def create_ui(self):

    
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)

    
        buttons = QHBoxLayout()

        self.upload_button = QPushButton("Upload JSON")
        self.save_button = QPushButton("Save")

        buttons.addWidget(self.upload_button)
        buttons.addWidget(self.save_button)

        layout.addLayout(buttons)

       
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText(
            "Upload a JSON file..."
        )

        layout.addWidget(self.editor)

        
        self.file_label = QLabel("File: No file selected")
        self.status_label = QLabel("Status: Ready")

        layout.addWidget(self.file_label)
        layout.addWidget(self.status_label)

     
        self.upload_button.clicked.connect(self.upload_json)
        self.save_button.clicked.connect(self.save_json)

  
        self.save_button.setEnabled(False)

    def upload_json(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select JSON File",
            "",
            "JSON Files (*.json)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.editor.setPlainText(
                json.dumps(data, indent=4, ensure_ascii=False)
            )

            self.current_file = file_path

            self.file_label.setText(
                f"File: {file_path}"
            )

            self.status_label.setText(
                "Status: JSON loaded"
            )

            self.save_button.setEnabled(True)

        except json.JSONDecodeError as error:

            QMessageBox.critical(
                self,
                "Invalid JSON",
                f"Invalid JSON file.\n\n{error}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Could not open file.\n\n{error}"
            )

    def save_json(self):

        if not self.current_file:
            return

        try:

          
            data = json.loads(
                self.editor.toPlainText()
            )

            with open(
                self.current_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            self.status_label.setText(
                "Status: Saved successfully"
            )

            QMessageBox.information(
                self,
                "Saved",
                "JSON file updated successfully."
            )

        except json.JSONDecodeError as error:

            QMessageBox.critical(
                self,
                "Invalid JSON",
                f"Your JSON has an error.\n\n{error}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Save Error",
                f"Could not save file.\n\n{error}"
            )