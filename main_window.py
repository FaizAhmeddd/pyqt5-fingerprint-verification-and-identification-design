import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QToolBar, QComboBox, 
                             QStatusBar, QCheckBox, QLabel, QWidget, QVBoxLayout, 
                             QTextEdit, QSplitter, QFrame, QGridLayout, QSizePolicy, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from functions import Functions

class ImagePane(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(1)
        
        layout = QVBoxLayout(self)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

    def set_image(self, pixmap):
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finger Print SDK")
        self.setGeometry(100, 100, 1000, 600)

        # Set the window icon
        self.setWindowIcon(QIcon('src/fingerprint.png'))  # Update the path to your icon file

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top area with image panes
        top_splitter = QSplitter(Qt.Horizontal)
        self.left_pane = ImagePane()
        self.right_pane = ImagePane()
        top_splitter.addWidget(self.left_pane)
        top_splitter.addWidget(self.right_pane)
        top_splitter.setSizes([500, 500])
        main_layout.addWidget(top_splitter, 3)  # Give more space to the top area

        # Bottom area with a vertical splitter
        bottom_splitter = QSplitter(Qt.Horizontal)
        
        # Message area (left side)
        self.message_area1 = QTextEdit()
        self.message_area1.setReadOnly(True)
        bottom_splitter.addWidget(self.message_area1)
        
        # Score and ID columns (right side)
        score_id_widget = QWidget()
        score_id_layout = QVBoxLayout(score_id_widget)

        score_id_grid = QGridLayout()
        score_id_grid.addWidget(QLabel("Score"), 0, 0)
        score_id_grid.addWidget(QLabel("ID"), 0, 1)
        self.score_label = QLabel()
        self.id_label = QLabel()
        score_id_grid.addWidget(self.score_label, 1, 0)
        score_id_grid.addWidget(self.id_label, 1, 1)
        score_id_layout.addLayout(score_id_grid)

        score_id_widget.setLayout(score_id_layout)
        
        # Message area (right side) - Changed to QTableWidget
        self.message_area2 = QTableWidget()
        self.message_area2.setColumnCount(2)
        self.message_area2.setHorizontalHeaderLabels(["Score", "ID"])
        self.message_area2.setEditTriggers(QTableWidget.NoEditTriggers)
        self.message_area2.horizontalHeader().setStretchLastSection(True)
        bottom_splitter.addWidget(self.message_area2)

        # Add bottom_splitter to the main layout
        main_layout.addWidget(bottom_splitter, 1)  # Give less space to the bottom area

        self.functions = Functions(self)

        self.create_menu_bar()
        self.create_tool_bar()
        self.create_status_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu('File')
        open_action = QAction('Open Image', self)
        open_action.triggered.connect(self.functions.open_file)
        save_action = QAction('Save Results', self)
        save_action.triggered.connect(self.functions.save_results)
        exit_action = QAction('Exit', self, triggered=self.close)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        # Tools menu
        tools_menu = menu_bar.addMenu('Tools')
        enroll_action = QAction('Enroll Fingerprint', self)
        enroll_action.triggered.connect(self.functions.enroll)
        identify_action = QAction('Identify Fingerprint', self)
        identify_action.triggered.connect(self.functions.identify)
        verify_action = QAction('Verify Fingerprint', self)
        verify_action.triggered.connect(self.functions.verify)
        match_action = QAction('Match Fingerprints', self)
        match_action.triggered.connect(self.functions.match)
        preprocess_action = QAction('Preprocess Image', self)
        preprocess_action.triggered.connect(self.functions.preprocess)
        enhance_action = QAction('Enhance Image', self)
        enhance_action.triggered.connect(self.functions.enhance)
        segment_action = QAction('Segment Image', self)
        segment_action.triggered.connect(self.functions.segment)
        
        tools_menu.addAction(enroll_action)
        tools_menu.addAction(identify_action)
        tools_menu.addAction(verify_action)
        tools_menu.addAction(match_action)
        tools_menu.addAction(preprocess_action)
        tools_menu.addAction(enhance_action)
        tools_menu.addAction(segment_action)

        # Help menu
        help_menu = menu_bar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.functions.about)
        help_menu.addAction(about_action)

    def create_tool_bar(self):
        tool_bar = QToolBar("Main Toolbar")
        self.addToolBar(tool_bar)

        enroll_action = QAction('Enroll', self)
        enroll_action.triggered.connect(self.functions.enroll)
        identify_action = QAction('Identify', self)
        identify_action.triggered.connect(self.functions.identify)
        verify_action = QAction('Verify', self)
        verify_action.triggered.connect(self.functions.verify)
        save_image_action = QAction('Save image...', self)
        save_image_action.triggered.connect(self.functions.save_image)

        tool_bar.addAction(enroll_action)
        tool_bar.addAction(identify_action)
        tool_bar.addAction(verify_action)
        
        tool_bar.addSeparator()  # Add separator

        self.check_duplicates_check_box = QCheckBox("Check for duplicates")
        tool_bar.addWidget(self.check_duplicates_check_box)

        self.from_file_combo = QComboBox()
        self.from_file_combo.addItem('From file...')
        self.from_file_combo.currentIndexChanged.connect(self.functions.from_file_changed)
        tool_bar.addWidget(self.from_file_combo)

        tool_bar.addAction(save_image_action)
        
        tool_bar.addSeparator()  # Add separator

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready")

    def update_message_area1(self, message):
        self.message_area1.append(message)

    def set_left_image(self, pixmap):
        self.left_pane.set_image(pixmap)

    def set_right_image(self, pixmap):
        self.right_pane.set_image(pixmap)

    def update_score_id(self, score, id):
        self.score_label.setText(str(score))
        self.id_label.setText(str(id))

    def add_row_to_message_area2(self, score, id):
        row_position = self.message_area2.rowCount()
        self.message_area2.insertRow(row_position)
        self.message_area2.setItem(row_position, 0, QTableWidgetItem(str(score)))
        self.message_area2.setItem(row_position, 1, QTableWidgetItem(str(id)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
