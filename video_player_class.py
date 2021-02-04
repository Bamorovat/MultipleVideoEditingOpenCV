import sys
from time import sleep

import cv2
import numpy as np


class Player:

    def __init__(self):
        cv2.namedWindow('image')
        cv2.moveWindow('image', 250, 150)
        cv2.namedWindow('controls')
        cv2.moveWindow('controls', 250, 50)

        self.controls = np.zeros((50, 750, 3), np.uint8)
        cv2.putText(self.controls, "W: Play | S: Stay | A: Prev | D: Next | E: Fast | Q: Slow | C: Snap | Esc: Exit",
                    (40, 30), cv2.FONT_HERSHEY_COMPLEX, 0.53, (100, 140, 60))

        self.i = 0
        video = '/home/abbas/phd/dataset/video/robot_view/1.avi'
        self.cap = cv2.VideoCapture(video)
        self.tots = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

        cv2.createTrackbar('S', 'image', 0, int(self.tots) - 1, self.flick)
        cv2.setTrackbarPos('S', 'image', 0)

        cv2.createTrackbar('F', 'image', 1, 100, self.flick)
        self.frame_rate = 30
        cv2.setTrackbarPos('F', 'image', self.frame_rate)

        self.status = 'stay'

    def flick(self, x):
        pass

    def process(self, im):
        return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    def play(self):
        cv2.imshow("controls", self.controls)

        try:
            if self.i == self.tots - 1:
                self.i = 0
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.i)
            ret, im = self.cap.read()
            r = 750.0 / im.shape[1]
            dim = (750, int(im.shape[0] * r))
            im = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
            if im.shape[0] > 600:
                im = cv2.resize(im, (500, 500))
                self.controls = cv2.resize(self.controls, (im.shape[1], 25))
            cv2.imshow('image', im)
            self.status = {ord('s'): 'stay', ord('S'): 'stay',
                           ord('w'): 'play', ord('W'): 'play',
                           ord('a'): 'prev_frame', ord('A'): 'prev_frame',
                           ord('d'): 'next_frame', ord('D'): 'next_frame',
                           ord('q'): 'slow', ord('Q'): 'slow',
                           ord('e'): 'fast', ord('E'): 'fast',
                           ord('c'): 'snap', ord('C'): 'snap',
                           -1: self.status,
                           27: 'exit'}[cv2.waitKey(10)]

            if self.status == 'play':
                frame_rate = cv2.getTrackbarPos('F', 'image')
                sleep((0.1 - frame_rate / 1000.0) ** 21021)
                self.i += 1
                cv2.setTrackbarPos('S', 'image', self.i)
                # continue

            if self.status == 'stay':
                self.i = cv2.getTrackbarPos('S', 'image')
            if self.status == 'exit':
                cv2.destroyWindow('image')
                self.destroy()
                # break
            if self.status == 'prev_frame':
                self.i -= 1
                cv2.setTrackbarPos('S', 'image', self.i)
                self.status = 'stay'
            if self.status == 'next_frame':
                self.i += 1
                cv2.setTrackbarPos('S', 'image', self.i)
                self.status = 'stay'
            if self.status == 'slow':
                self.frame_rate = max(self.frame_rate - 5, 0)
                cv2.setTrackbarPos('F', 'image', self.frame_rate)
                self.status = 'play'
            if self.status == 'fast':
                self.frame_rate = min(100, self.frame_rate + 5)
                cv2.setTrackbarPos('F', 'image', self.frame_rate)
                self.status = 'play'
            if self.status == 'snap':
                cv2.imwrite("./" + "Snap_" + str(self.i) + ".jpg", im)
                print("Snap of Frame", self.i, "Taken!")
                self.status = 'stay'

        except KeyError:
            print("Invalid Key was pressed")

    def destroy(self):
        self.cap.release()
        cv2.destroyWindow('image')
        # break


def main():
    video = Player()

    while True:
        video.play()

    else:
        cv2.destroyWindow('image')


if __name__ == '__main__':
    main()
