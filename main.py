import sys
import json
import re
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QClipboard
from PySide6.QtCore import Qt
from design_ui import Ui_MainWindow  # First Window
from design2_ui import Ui_MainWindow as GroupingWindow  # Second Window

# Load the JSON Kanji mapping
with open("kanji_levels.json", "r", encoding="utf-8") as f:
    KANJI_JLPT_MAP = json.load(f)

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file_path = None  # Store the selected file path
        self.pushButton.clicked.connect(self.open_file_dialog)
        self.pushButton_2.clicked.connect(self.start_grouping)

    def open_file_dialog(self):
        """Opens a file dialog to select a .txt file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt)")
        if file_path:
            self.file_path = file_path
            QMessageBox.information(self, "File Selected", f"Selected: {file_path}")

    def start_grouping(self):
        """Processes the selected file and displays grouped Kanji"""
        if not self.file_path:
            QMessageBox.warning(self, "Error", "Please select a text file first!")
            return

        try:
            # Read the Kanji from the file
            with open(self.file_path, "r", encoding="utf-8") as file:
                kanji_text = file.read()

            kanji_list = list(kanji_text.strip())  # Convert text into a list of characters

            # Categorize Kanji based on JLPT levels
            grouped_kanji = {
                "N5": [],
                "N4": [],
                "N3": [],
                "N2": [],
                "N1": [],
                "Outside": []  # For unknown Kanji
            }

            kanji_pattern = re.compile(r'[\u4E00-\u9FFF]')  # Match Kanji only

            for kanji in kanji_list:
                if kanji_pattern.match(kanji):  # Ensure it's a Kanji character
                    level = KANJI_JLPT_MAP.get(kanji, "Outside")
                    grouped_kanji[level].append(kanji)

            # Open the grouping window and display results
            self.grouping_window = GroupingWindowApp(grouped_kanji)
            self.grouping_window.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

class GroupingWindowApp(QMainWindow, GroupingWindow):
    def __init__(self, grouped_kanji):
        super().__init__()
        self.setupUi(self)

        # Define the mapping between JLPT levels and scroll areas
        self.scroll_areas = {
            "N5": self.scrollArea,
            "N4": self.scrollArea_2,
            "N3": self.scrollArea_3,
            "N2": self.scrollArea_4,
            "N1": self.scrollArea_5,
            "Outside": self.scrollArea_6,
        }

        self.copy_buttons = {
            "N5": self.pushButton_2,
            "N4": self.pushButton_3,
            "N3": self.pushButton_4,
            "N2": self.pushButton_5,
            "N1": self.pushButton_6,
            "Outside": self.pushButton_7,
        }

        self.kanji_data = grouped_kanji  # Store Kanji data for copying

        # Populate scroll areas and connect copy buttons
        for level, kanji_list in grouped_kanji.items():
            self.populate_scroll_area(self.scroll_areas[level], kanji_list)
            self.copy_buttons[level].clicked.connect(lambda _, l=level: self.copy_to_clipboard(l))  # Fix lambda scoping issue

    def populate_scroll_area(self, scroll_area, kanji_list):
        """Dynamically adds Kanji to the given scroll area"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        kanji_text = " ".join(kanji_list) if kanji_list else "None"
        label = QLabel(kanji_text)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Enable mouse selection
        layout.addWidget(label)

        widget.setLayout(layout)
        scroll_area.setWidget(widget)

    def copy_to_clipboard(self, level):
        """Copies the Kanji from the selected category to the clipboard"""
        clipboard = QApplication.clipboard()
        kanji_text = " ".join(self.kanji_data[level])
        clipboard.setText(kanji_text)

        # Show confirmation message
        QMessageBox.information(self, "Copied", f"Copied Kanji from {level} to clipboard!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
