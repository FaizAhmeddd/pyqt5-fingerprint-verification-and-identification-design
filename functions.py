from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap

class Functions:
    def __init__(self, main_window):
        self.main_window = main_window

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self.main_window, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.main_window.set_left_image(pixmap)
            self.main_window.update_message_area1(f"Opened file: {file_name}")

    def enroll(self):
        self.main_window.update_message_area1("Enroll action triggered")
        # Implement enrollment logic here

    def identify(self):
        self.main_window.update_message_area1("Identify action triggered")
        # Implement identification logic here

    def verify(self):
        self.main_window.update_message_area1("Verify action triggered")
        # Implement verification logic here

    def save_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self.main_window, "Save Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            # Implement image saving logic here
            self.main_window.update_message_area1(f"Image saved as: {file_name}")

    def from_file_changed(self, index):
        selected_item = self.main_window.from_file_combo.currentText()
        self.main_window.update_message_area1(f"Selected: {selected_item}")
        # Implement logic for handling file selection