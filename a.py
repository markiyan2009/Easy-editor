from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import*
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import*
import os
app = QApplication([])
main_win = QWidget()

main_win.resize(700,500)
main_win.setWindowTitle("Easy Editor")
papka = QPushButton("Папка")
list_image = QListWidget()
left = QPushButton("Ліворуч")
right = QPushButton("Праворуч")
mirrow = QPushButton("Дзеркало")
blur = QPushButton('Різкість')
button = QPushButton("Ч/Б")
label = QLabel("Картинка")


line1 = QHBoxLayout()

line2 = QVBoxLayout()
line3 = QVBoxLayout()
line4 = QHBoxLayout()

line2.addWidget(papka)
line2.addWidget(list_image)
line3.addWidget(label)
line4.addWidget(left)
line4.addWidget(right)
line4.addWidget(mirrow)
line4.addWidget(blur)
line4.addWidget(button)

line2.addLayout(line4)
line1.addLayout(line1,20)
line1.addLayout(line2,80)
main_win.setLayout(line1)
workdkir = ""
def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result
def chooseWorkdir():
    global workdkir
    workdkir = QFileDialog.getExistingDirectory()
def showFilenamesList():
    extensions = [".jpg",".jpeg",".png",".gif",".bmp"]
    chooseWorkdir()
    filenames=filter(os.listdir(workdkir), extensions)
    list_image.clear()
    for filename in filenames:
        list_image.addItem(filename)
papka.clicked.connect(showFilenamesList)
class ImageProccessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def loadImage(self, dir, filename):

        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdkir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdkir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdkir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdkir, self.save_dir, self.filename)
        self.showImage(image_path)


    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path) 
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def showImage(self, path):
        label.hide()
        pixmapimage = QPixmap(path)
        w, h = label.width(), label.height()
        pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio)
        label.setPixmap(pixmapimage)
        label.show()
    
def showChosenImage():
    if list_image.currentRow() >= 0:
        filename = list_image.currentItem().text()
        workimage.loadImage(workdkir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProccessor()
list_image.currentRowChanged.connect(showChosenImage)
button.clicked.connect(workimage.do_bw)
left.clicked.connect(workimage.do_left)
right.clicked.connect(workimage.do_right)
blur.clicked.connect(workimage.do_sharpen)
mirrow.clicked.connect(workimage.do_flip)

        





main_win.show()
app.exec_()