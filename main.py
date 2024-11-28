import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QProgressBar, QDialog, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import shutil
import os
import schedule
import threading
import time

class ProgressWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Backup Progress')
        self.setGeometry(150, 150, 400, 100)

        self.layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.message_label = QLabel('')
        self.layout.addWidget(self.message_label)

        self.setLayout(self.layout)

    def update_progress(self, value, total):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(value)
        self.progress_bar.setFormat(f'%p% ({value}/{total})')

    def set_complete(self):
        self.message_label.setText('Backup Complete')

class BackupApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.backup_directory = None
        self.restore_directory = None
        self.dark_mode = False
        self.initUI()

        # Start the scheduler in a separate thread
        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def initUI(self):
        self.setWindowTitle('Backup App')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Company logo and name
        logo_label = QLabel()
        logo_pixmap = QPixmap('assets/IMG_4246.jpg')  
        logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        company_name_label = QLabel('Drimtech')
        company_name_label.setAlignment(Qt.AlignCenter)
        company_name_label.setStyleSheet('font-size: 36px;')
        self.layout.addWidget(company_name_label)

        self.theme_button = QPushButton()
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setFixedSize(50, 50)
        self.theme_button.setStyleSheet('border: none;')
        self.update_theme_button()
        self.layout.addWidget(self.theme_button, alignment=Qt.AlignRight)

        # Buttons
        self.button_layout = QHBoxLayout()

        backup_button = QPushButton('Select Backup Path')
        backup_button.clicked.connect(self.select_backup_directory)
        self.button_layout.addWidget(backup_button)

        restore_button = QPushButton('Select Restore Path')
        restore_button.clicked.connect(self.select_restore_directory)
        self.button_layout.addWidget(restore_button)

        start_button = QPushButton('Start Backup')
        start_button.clicked.connect(self.start_backup)
        self.button_layout.addWidget(start_button)

        self.layout.addLayout(self.button_layout)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.apply_theme()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.update_theme_button()

    def update_theme_button(self):
        if self.dark_mode:
            self.theme_button.setText('🌞')  # Sun symbol for light mode
        else:
            self.theme_button.setText('🌜')  # Moon symbol for dark mode

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet('''
                QMainWindow {
                    background-color: #121212;
                }
                QPushButton {
                    background-color: #ffffff;
                    color: black;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QProgressBar {
                    border: 2px solid grey;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #1E88E5;
                    width: 20px;
                }
                QLabel {
                    font-size: 16px;
                    color: #ffffff;
                }
            ''')
        else:
            self.setStyleSheet('''
                QMainWindow {
                    background-color: #f0f0f0;
                }
                QPushButton {
                    background-color: #000000;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
                QProgressBar {
                    border: 2px solid grey;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #1E88E5;
                    width: 20px;
                }
                QLabel {
                    font-size: 16px;
                    color: #333;
                }
            ''')

    def show_message_box(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        if self.dark_mode:
            msg_box.setStyleSheet('''
                QMessageBox {
                    background-color: #121212;
                    color: white;
                }
                QPushButton {
                    background-color: #ffffff;
                    color: black;
                }
            ''')
        else:
            msg_box.setStyleSheet('''
                QMessageBox {
                    background-color: #f0f0f0;
                    color: black;
                }
                QPushButton {
                    background-color: #000000;
                    color: white;
                }
            ''')
        msg_box.exec_()

    def select_backup_directory(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select File to Backup", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file:
            self.backup_directory = file
            self.show_message_box("Backup", f"Backup file selected: {file}")
        else:
            directory = QFileDialog.getExistingDirectory(self, "Select Directory to Backup", options=options)
            if directory:
                self.backup_directory = directory
                self.show_message_box("Backup", f"Backup directory selected: {directory}")

    def select_restore_directory(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Restore Directory", options=options)
        if directory:
            self.restore_directory = directory
            self.show_message_box("Restore", f"Restore directory selected: {directory}")

    def start_backup(self):
        if not self.backup_directory or not self.restore_directory:
            self.show_message_box("Warning", "Please select both backup and restore directories.")
            return

        # Assume a transfer speed of 10 MB/s for estimation
        transfer_speed = 10 * 1024 * 1024  # 10 MB/s in bytes

        items = os.listdir(self.backup_directory) if os.path.isdir(self.backup_directory) else [self.backup_directory]
        total_items = len(items)

        total_size = sum(os.path.getsize(os.path.join(self.backup_directory, item)) for item in items) if os.path.isdir(self.backup_directory) else os.path.getsize(self.backup_directory)

        estimated_time = total_size / transfer_speed

        progress_window = None
        if estimated_time > 10:
            progress_window = ProgressWindow()
            progress_window.show()

        for i, item in enumerate(items, start=1):
            source_item = os.path.join(self.backup_directory, item) if os.path.isdir(self.backup_directory) else self.backup_directory
            destination_item = os.path.join(self.restore_directory, os.path.basename(item))
            if os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item, dirs_exist_ok=True)
            else:
                shutil.copy2(source_item, destination_item)
            if estimated_time > 10:
                progress_window.update_progress(i, total_items)

        if estimated_time > 10:
            progress_window.set_complete()
        self.show_message_box("Backup Complete", "Backup process completed successfully.")
        os.system(f'open {self.restore_directory}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BackupApp()
    window.show()
    sys.exit(app.exec_())
