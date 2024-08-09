import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QPushButton, QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import cv2
import numpy as np
from pollinator import Pollinator

class PollinateThread(QThread):
    finished = pyqtSignal()

    def __init__(self, pollinator):
        super().__init__()
        self.pollinator = pollinator

    def run(self):
        self.pollinator.pollinate()
        self.finished.emit()

class CameraThread(QThread):
    update_image = pyqtSignal(QImage)
    update_depth = pyqtSignal(QImage)

    def __init__(self, pollinator):
        super().__init__()
        self.pollinator = pollinator

    def run(self):
        while True:
            color_image, depth_image = self.pollinator.get_latest_frame()
            
            # Update image tab
            rgb_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            qt_image = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
            self.update_image.emit(qt_image)

            # Update depth tab
            if len(depth_image.shape) == 2:
                # Depth image is already grayscale
                qt_depth_image = QImage(depth_image.data, depth_image.shape[1], depth_image.shape[0], QImage.Format_Grayscale8)
            else:
                # Depth image is in color format, convert to grayscale
                grayscale_depth = cv2.cvtColor(depth_image, cv2.COLOR_BGR2GRAY)
                qt_depth_image = QImage(grayscale_depth.data, grayscale_depth.shape[1], grayscale_depth.shape[0], QImage.Format_Grayscale8)
            self.update_depth.emit(qt_depth_image)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI with 3 Tabs")
        self.setStyleSheet("background-color: #ff9900;")  # Orange theme

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("background-color: #ff9900;")  # Orange theme

        # Tab 1: Button
        self.tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        self.button = QPushButton("Pollinate")
        self.button.clicked.connect(self.start_pollination)
        tab1_layout.addWidget(self.button, alignment=Qt.AlignCenter)
        self.tab1.setLayout(tab1_layout)

        # Tab 2: Image
        self.tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        self.image_label = QLabel()
        tab2_layout.addWidget(self.image_label)
        self.tab2.setLayout(tab2_layout)

        # Tab 3: Depth Map
        self.tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        self.depth_label = QLabel()
        tab3_layout.addWidget(self.depth_label)
        self.tab3.setLayout(tab3_layout)

        # Add tabs to tab widget
        self.tab_widget.addTab(self.tab1, "Tab 1")
        self.tab_widget.addTab(self.tab2, "Tab 2")
        self.tab_widget.addTab(self.tab3, "Tab 3")

        # Create and start pollinator, pollinate thread, and camera thread
        self.pollinator = Pollinator()
        self.pollinate_thread = PollinateThread(self.pollinator)
        self.pollinate_thread.finished.connect(self.pollinate_finished)
        self.camera_thread = CameraThread(self.pollinator)
        self.camera_thread.update_image.connect(self.update_image_tab)
        self.camera_thread.update_depth.connect(self.update_depth_tab)
        self.camera_thread.start()

        # Set layout and show window
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        self.show()

    def start_pollination(self):
        self.button.setEnabled(False)
        self.pollinate_thread.start()

    def pollinate_finished(self):
        self.button.setEnabled(True)

    def update_image_tab(self, image):
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def update_depth_tab(self, image):
        self.depth_label.setPixmap(QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())