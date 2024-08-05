import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget, QAction, QToolBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from main_window import MainWindow  # Import the MainWindow class

class FingerPrintSDKApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Set the window title
        self.setWindowTitle('FingerSync')

        # Create a stacked widget to manage navigation
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create the welcome screen widget
        self.welcome_widget = QWidget()
        self.welcome_widget.setObjectName("bgwidget")

        # Set the gradient background for the welcome screen
        self.welcome_widget.setStyleSheet("""
            QWidget#bgwidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 rgba(78, 129, 235, 255), 
                                            stop:1 rgba(153, 221, 255, 255));
            }
        """)

        self.main_layout = QVBoxLayout(self.welcome_widget)

        # Create the heading label
        self.heading = QLabel('Welcome to FingerSync', self.welcome_widget)
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.setWordWrap(True)
        self.heading.setStyleSheet("font-size: 40px; font-weight: bold; color: white; background: transparent;")
        self.setWindowIcon(QIcon('src/fingerprint.png'))

        # Create the button
        self.button = QPushButton('Identify', self.welcome_widget)
        self.button.setFixedSize(200, 50)
        self.button.setStyleSheet("font-size: 18px; background: rgba(255, 255, 255, 0.8);border-radius:20px;")
        self.button.clicked.connect(self.open_main_window)  # Connect the button click to open_main_window method

        # Create a QHBoxLayout to center the button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.button)
        button_layout.addStretch(1)

        # Add the heading and button layout to the main layout
        self.main_layout.addWidget(self.heading)
        self.main_layout.addSpacing(80)  # Add padding between the heading and the button
        self.main_layout.addLayout(button_layout)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Add the welcome widget to the stacked widget
        self.stacked_widget.addWidget(self.welcome_widget)

        # Create an instance of the MainWindow
        self.main_window = MainWindow()

        # Add a toolbar to the main window for navigation
        self.tool_bar = QToolBar("Main Toolbar")
        self.main_window.addToolBar(self.tool_bar)

        # Add the main window widget to the stacked widget
        self.stacked_widget.addWidget(self.main_window)

        # Maximize the window
        self.showMaximized()

    def open_main_window(self):
        # Navigate to the main window widget
        self.stacked_widget.setCurrentWidget(self.main_window)

        # Add a back button to the main window's tool bar if not already added
        if not hasattr(self, 'back_action'):
            self.back_action = QAction(QIcon('src/arrow_back.png'), 'Back', self)  # Use an arrow icon for the back action
            self.back_action.triggered.connect(self.show_welcome_screen)
            if self.tool_bar.actions():
                self.tool_bar.insertAction(self.tool_bar.actions()[0], self.back_action)
            else:
                self.tool_bar.addAction(self.back_action)

    def show_welcome_screen(self):
        # Navigate back to the welcome widget
        self.stacked_widget.setCurrentWidget(self.welcome_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FingerPrintSDKApp()
    sys.exit(app.exec_())
