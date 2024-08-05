import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QToolBar, QComboBox, 
                             QStatusBar, QCheckBox, QLabel, QWidget, QVBoxLayout, 
                             QTextEdit, QSplitter, QFrame, QSizePolicy, 
                             QTableWidget, QTableWidgetItem, QHBoxLayout, QScrollArea)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from functions import Functions

class ImagePane(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(1)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(0)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        
        self.scroll_area.setWidget(self.image_label)
        self.layout.addWidget(self.scroll_area)
        
        self.original_pixmap = None

    def set_image(self, pixmap):
        self.original_pixmap = pixmap
        self.update_image()

    def update_image(self):
        if self.original_pixmap:
            scaled_pixmap = self.original_pixmap.scaled(
                self.scroll_area.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()

    def clear_image(self):
        self.image_label.clear()
        self.original_pixmap = None

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Finger Print SDK")
        self.setGeometry(100, 100, 1000, 600)

        self.setWindowIcon(QIcon('src/fingerprint.png'))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Main splitter
        self.main_splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(self.main_splitter)

        # Top area with image panes
        top_splitter = QSplitter(Qt.Horizontal)
        self.left_pane = ImagePane()
        self.right_pane = ImagePane()
        top_splitter.addWidget(self.left_pane)
        top_splitter.addWidget(self.right_pane)
        top_splitter.setSizes([500, 500])
        self.main_splitter.addWidget(top_splitter)

        # Bottom area with a horizontal splitter
        bottom_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(bottom_splitter)

        # Message area 1 (left side)
        self.message_area1 = QTextEdit()
        self.message_area1.setReadOnly(True)
        bottom_splitter.addWidget(self.message_area1)

        # Right side widget (Message area 2 + Score and ID)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)

        # Score and ID area
        score_id_widget = QWidget()
        score_id_layout = QHBoxLayout(score_id_widget)
        score_id_layout.setContentsMargins(5, 5, 5, 5)
        score_id_layout.setSpacing(10)

        # Message area 2 (right side) - Changed to QTableWidget
        self.message_area2 = QTableWidget()
        self.message_area2.setColumnCount(2)
        self.message_area2.setHorizontalHeaderLabels(["Score", "ID"])
        self.message_area2.setEditTriggers(QTableWidget.NoEditTriggers)
        self.message_area2.horizontalHeader().setStretchLastSection(True)
        right_layout.addWidget(self.message_area2)

        bottom_splitter.addWidget(right_widget)

        # Set initial sizes for main splitter and bottom splitter
        self.main_splitter.setSizes([400, 200])
        bottom_splitter.setSizes([500, 500])

        self.functions = Functions(self)

        self.create_menu_bar()
        self.create_tool_bar()
        self.create_status_bar()

        # Apply custom styles
        self.apply_styles()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.main_splitter.setSizes([self.height() * 0.7, self.height() * 0.3])

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

        # Add Back button
        back_action = QAction('Back', self)
        back_action.triggered.connect(self.functions.back)

        tool_bar.addAction(back_action)
        tool_bar.addAction(enroll_action)
        tool_bar.addAction(identify_action)
        tool_bar.addAction(verify_action)
        
        tool_bar.addSeparator()

        self.check_duplicates_check_box = QCheckBox("Check for duplicates")
        tool_bar.addWidget(self.check_duplicates_check_box)

        self.from_file_combo = QComboBox()
        self.from_file_combo.addItem('From file...')
        self.from_file_combo.currentIndexChanged.connect(self.functions.from_file_changed)
        tool_bar.addWidget(self.from_file_combo)

        tool_bar.addAction(save_image_action)
        
        tool_bar.addSeparator()

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready")

    def apply_styles(self):
        # Apply styles to the image panes
        image_pane_style = """
            QFrame {
                border: 2px solid #4E81EB; /* Outer border color */
                border-radius: 2px;
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 rgba(78, 129, 235, 255), 
                                            stop:1 rgba(153, 221, 255, 255));
            }
            QScrollArea {
                border: 1px solid white; /* Inner border color */
            }
        """
        self.left_pane.setStyleSheet(image_pane_style)
        self.right_pane.setStyleSheet(image_pane_style)

        # Apply styles to the message areas
        message_area_style = """
            QTextEdit {
                border: 2px solid #4E81EB; /* Outer border color */
                border-radius: 2px;
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 rgba(78, 129, 235, 255), 
                                            stop:1 rgba(153, 221, 255, 255));
                color: white;
                padding: 10px;
            }
            QTableWidget {
                border: 2px solid #4E81EB; /* Outer border color */
                border-radius: 2px;
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 rgba(78, 129, 235, 255), 
                                            stop:1 rgba(153, 221, 255, 255));
                color: white;
            }
            QTableWidget::item {
                padding: 4px; /* Padding around the items */
            }
            QHeaderView::section {
                background: #4E81EB;
                color: white;
                padding: 2px;
                border: 1px solid white; /* Inner border color */
            }
        """
        self.message_area1.setStyleSheet(message_area_style)
        self.message_area2.setStyleSheet(message_area_style)

    def update_message_area1(self, message):
        self.message_area1.append(message)

    def set_left_image(self, pixmap):
        self.left_pane.set_image(pixmap)

    def set_right_image(self, pixmap):
        self.right_pane.set_image(pixmap)

    def update_score_id(self, score, id):
        # Assuming you have defined these labels somewhere
        if hasattr(self, 'score_label') and hasattr(self, 'id_label'):
            self.score_label.setText(str(score))
            self.id_label.setText(str(id))

    def add_row_to_message_area2(self, score, id):
        row_position = self.message_area2.rowCount()
        self.message_area2.insertRow(row_position)
        self.message_area2.setItem(row_position, 0, QTableWidgetItem(str(score)))
        self.message_area2.setItem(row_position, 1, QTableWidgetItem(str(id)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())