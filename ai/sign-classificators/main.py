# This is a sample Python script.
import os.path

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    reposDir = os.path.abspath('./../../..')
    znakiDir = os.path.abspath(reposDir + '/znaki-sandbox/znaki')
    znakPath = os.path.abspath(znakiDir + "/D-3.png")

    
    znakImage = cv2.imread(znakPath)
    cv2.imshow("znak", znakImage)
    cv2.waitKey(0)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
