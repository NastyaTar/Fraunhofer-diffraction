# дифракция Фраунгофера объектов произвольной формы
import shutil

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv2
import os
import uuid

drawing = False
pt1_x, pt1_y = None, None

current_directory = os.getcwd()

# создается папка для объектов, которые рисует пользователь
input_dir = os.path.join(current_directory, r'input')
if not os.path.exists(input_dir):
    os.makedirs(input_dir)

# создается папка для дифракций
output_dir = os.path.join(current_directory, r'output')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(output_dir):
    file_path = os.path.join(output_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


# Функция для рисования
def line_drawing(event, x, y, flags, param):
    global pt1_x, pt1_y, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        pt1_x, pt1_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(img, (pt1_x, pt1_y), (x, y), color=(255, 255, 255), thickness=7)
            pt1_x, pt1_y = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img, (pt1_x, pt1_y), (x, y), color=(255, 255, 255), thickness=7)


# Запуск окна для рисования
img = np.zeros((300, 300, 3), np.uint8)
cv2.namedWindow('physics second model')
cv2.setMouseCallback('physics second model', line_drawing)

# Пока не нажата кнопка escape окно открыто с возможностью рисования
while 1:
    cv2.imshow('physics second model', img)
    if cv2.waitKey(1) & 0xFF == 27:
        cv2.imwrite(os.path.join(current_directory, r'input', 'picture.png'), img)
        break

cv2.destroyAllWindows()

f = []

for path in os.listdir(input_dir):
    full_path = os.path.join(input_dir, path)
    if os.path.isfile(full_path):
        f.append(full_path)

# Дифракция созданного изображения 
for p in f:
    img_path = p
    image = cv2.imread(img_path, 0).astype(float) * .001
    res = len(image)
    img_fft = np.abs(np.fft.fftshift(np.fft.fft2(image)))
    plt.imshow(img_fft, cmap=cm.plasma)
    plt.savefig(os.path.join(output_dir, str(uuid.uuid4().hex)))
