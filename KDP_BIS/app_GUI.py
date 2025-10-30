from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, 
                             QFormLayout, QLineEdit, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import KDP_BIS

# Only needed for access to command line arguments
import sys

class DropLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("\n\n Drop KDP Excel File Here or MY SW.csv File\n\n")
        self.setStyleSheet("QLabel{border: 4px dashed #aaa;}")
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.file_path = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    # ensure your dropEvent() method does not return any value
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.setText(f"File dropped: {file_path}")
            if file_path.endswith((".xlsx", ".xls", ".csv")):
                self.setText(f"✅ Loaded: {file_path}")
                self.file_path = file_path
            else:
                self.setText("❌ Not an Excel file")
        else:
            event.ignore()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KDP to BIS Comparator")
        self.setGeometry(200, 200, 600, 400)

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Snowflake Credentials form
        self.form_layout = QFormLayout()
        self.user_input = QLineEdit()
        self.form_layout.addRow("Snowflake Account:", self.user_input)

        # Drag and Drop area
        self.drop_label = DropLabel()
        
        
        # Process Button
        self.process_button = QPushButton("Run Comparison")
        self.process_button.clicked.connect(self.run_comparison)

        # Status Bar
        self.status_bar = self.statusBar()
        self.setStatusBar(self.status_bar)

        # Main layout assembly
        main_layout.addWidget(self.drop_label)
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.process_button)
    
    def run_comparison(self):
        try: 
            if not self.drop_label.file_path:
                raise ValueError("No file dropped. Please drop an Excel file.")
            else: 
                self.kdp_file_path = self.drop_label.file_path
                output_directory = KDP_BIS.Comparison(self.kdp_file_path, self.user_input.text()).run_process()
                self.statusBar().showMessage("Process completed successfully. Output saved to: " + output_directory)
        except Exception as e:
            if str(e)[:5] == "25001":
                self.statusBar().showMessage("Snowflake connection error. Please check your credentials.")
            else:
                self.statusBar().showMessage(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    window = MainApp()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.
    window.setWindowIcon(QIcon('favicon.ico'))
    # Start the event loop.
    app.exec()
