from PyQt5.QtWidgets import (QWidget,
                             QApplication,
                             QGridLayout,
                             QFormLayout,
                             QVBoxLayout,
                             QHBoxLayout,
                             QTabWidget,
                             QCheckBox,
                             QTextEdit,
                             QLineEdit,
                             QComboBox,
                             QSlider,
                             QPushButton,
                             QLabel,
                             QAction,
                             QWidgetAction,
                             QMenuBar,
                             QDoubleSpinBox,
                             QGraphicsView,
                             QGraphicsScene,
                             QGraphicsItem,
                             QGraphicsPixmapItem,
                             QGraphicsLineItem,
                             QGroupBox,
                             QTableWidget,
                             QMainWindow,
                             QDockWidget,
                             QFileDialog,
                             QDialog,
                             QInputDialog,
                             QMessageBox,
                             QStyle)
from PyQt5.QtWidgets import QListWidget,QListWidgetItem,QShortcut
from PyQt5.QtGui import QImage, QPixmap,QBrush,QPen,QColor,QFont,QKeySequence
from PyQt5.QtCore import Qt,QSize,QRectF,QLineF,QPointF,QTimer,QDir
# TODO: use only minimal imports
from .interface import ThorCamRecorder
import sys
import cv2
from skimage import img_as_ubyte
import time
import numpy as np

class ThorCamISI(QMainWindow):
    app = None
    def __init__(self, app = None):
        super(ThorCamISI,self).__init__()
        # init the cam
        print('Starting the camera.',flush=True)
        self.cam = ThorCamRecorder()
        self.is_acquiring = False
        self.cam.play_camera()
        print('Waiting for the first image.',flush=True)        
        while not len(self.cam.image):
            time.sleep(0.1)
        mainw = QWidget()
        self.setWindowTitle('ThorCam Intrinsic Signal Imaging')
        self.setCentralWidget(mainw)
        lay = QFormLayout()
        mainw.setLayout(lay)

        self.pixmap = QPixmap()
        self.scene = QGraphicsScene(0,0,self.cam.image.shape[1],
                                    self.cam.image.shape[0],self)
        self.view = QGraphicsView(self.scene, self)
        

        lay.addRow(self.view)

        self.record_isi = QPushButton('Run triggered acquisition')
        self.record_isi.clicked.connect(self.run_triggered_acquisition)
        lay.addRow(self.record_isi)
        self.updateimg = QTimer()
        self.updateimg.timeout.connect(self.update_image)
        self.updateimg.start(30)
        self.show()
    def run_triggered_acquisition(self):
        if not self.is_acquiring:
            # then it is not recording
            self.cam.stop_playing_camera()

            # get the filename
            filename, _ = QFileDialog.getSaveFileName(self,"Select a filename to save acquisition")
            if not filename is None:
                if not filename.endswith('.h5'):
                    filename += '.h5'

                # set hardware trigger
                self.cam.set_setting('trigger_type','HW Trigger')
                self.cam.filename = filename
                self.cam.is_saving = True
                
            self.cam.play_camera()

            self.record_isi.setText('STOP')
            self.is_acquiring = True
        else:
            # then stop recording
            self.cam.stop_playing_camera()
            self.cam.filename = None
            self.cam.is_saving = False
            print('Stopped recording')
            self.is_acquiring = False

            time.sleep(1)
            self.cam.set_setting('trigger_type','SW Trigger')
            time.sleep(5)
            self.cam.play_camera()
            self.record_isi.setText('Run triggered acquisition')
    def closeEvent(self,*args,**kwargs):
        self.updateimg.stop()
        self.cam.stop_playing_camera()
        self.cam.close_camera()
        self.cam.stop_cam_process(join = True)
        super(ThorCamISI, self).closeEvent(*args, **kwargs)
        
    def update_image(self):
        if len(self.cam.image):
            img = img_as_ubyte(self.cam.image)
            frame = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            cv2.putText(frame,str(self.cam.frame), (10,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, 255,2)
            img = QImage(frame, frame.shape[1], frame.shape[0], 
                                 frame.strides[0], QImage.Format_RGB888)
            self.scene.addPixmap(QPixmap.fromImage(img))
            self.scene.update()


if __name__ == '__main__':
    main()
    
def main():
    app = QApplication(sys.argv)
    instance =  ThorCamISI()
    instance.show()
    sys.exit(app.exec_())
