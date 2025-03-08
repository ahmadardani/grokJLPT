import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from design import Ui_MainWindow  # Import the generated UI file

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect button actions
        self.pushButton.clicked.connect(self.open_file_dialog)
        self.pushButton_2.clicked.connect(self.start_grouping)

    def open_file_dialog(self):
        """Opens a file dialog to select a .txt file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt)")
        if file_path:
            QMessageBox.information(self, "File Selected", f"Selected: {file_path}")

    def start_grouping(self):
        """Placeholder function for grouping logic"""
        QMessageBox.information(self, "Processing", "Kanji grouping process started!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
