from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
import os

class Functions:
    def __init__(self, main_window):
        self.main_window = main_window

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.main_window, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif);;All Files (*)", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            if pixmap.isNull():
                QMessageBox.critical(self.main_window, "Open Image", "Could not open the image file.")
            else:
                self.main_window.set_left_image(pixmap)
                self.main_window.update_message_area1(f"Opened file: {file_name}")

    def save_results(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.main_window, "Save Results", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    score = self.main_window.score_label.text()
                    id = self.main_window.id_label.text()
                    results = f"Score: {score}\nID: {id}\n"
                    file.write(results)
                QMessageBox.information(self.main_window, "Save Results", f"Results saved to {file_name}")
            except Exception as e:
                QMessageBox.critical(self.main_window, "Save Results", f"Could not save the results: {e}")

    def enroll(self):
        print("Enroll fingerprint action triggered")

    def identify(self):
        print("Identify fingerprint action triggered")

    def verify(self):
        print("Verify fingerprint action triggered")

    def match(self):
        print("Match fingerprints action triggered")

    def preprocess(self):
        print("Preprocess image action triggered")

    def enhance(self):
        print("Enhance image action triggered")

    def segment(self):
        print("Segment image action triggered")

    def about(self):
        QMessageBox.about(self.main_window, "About", "Fingerprint SDK Application\nVersion 1.0")

    def back(self):
        # Implement back button functionality
        pass

    def save_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.main_window, "Save Image", "", "Images (*.png *.jpg *.bmp *.gif);;All Files (*)", options=options)
        if file_name:
            right_pane_pixmap = self.main_window.right_pane.image_label.pixmap()
            if right_pane_pixmap:
                right_pane_pixmap.save(file_name)
                QMessageBox.information(self.main_window, "Save Image", f"Image saved to {file_name}")
            else:
                QMessageBox.critical(self.main_window, "Save Image", "No image to save.")

    def from_file_changed(self, index):
        print(f"From file changed action triggered with index {index}")

    def __init__(self, main_window):
        self.main_window = main_window
        # ... other initialization code ...

    def reset(self):
        # Reset any stored data or state
        # For example:
        self.current_image = None
        self.enrolled_fingerprints = []
        # ... reset any other attributes ...

    # ... other methods ...