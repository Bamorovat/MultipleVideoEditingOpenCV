"""
Multiple Video Editing tool  
@author Mohammad Abadi <m.bamorovvat@gmail.com>
"""

import cv2
import os

# global cap1, cap2, cap3
cap1 = None
cap2 = None
cap3 = None

robot_view_path = '/home/abbas/phd/dataset/video/robot_view/'
rgbd_livingroom_path = '/home/abbas/phd/dataset/video/rgbd_livingroom/'
omni_livingroom_path = '/home/abbas/phd/dataset/video/omni_livingroom/'


def get_videos(cap_name):
    global cap1, cap2, cap3
    cap1 = cv2.VideoCapture(os.path.join(robot_view_path, (cap_name + '.avi')))
    cap2 = cv2.VideoCapture(os.path.join(rgbd_livingroom_path, (cap_name + '.avi')))
    cap3 = cv2.VideoCapture(os.path.join(omni_livingroom_path, (cap_name + '.avi')))


def capture_action():
    # global cap1, cap2, cap3
    # Check if camera opened successfully
    if not cap1.isOpened() or not cap2.isOpened() or not cap3.isOpened():
        print("Error opening video stream or file")

    # Read until video is completed
    while cap1.isOpened():

        # Capture frame-by-frame
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()

        if ret1 or ret2 or ret3:

            # Display the resulting frame
            cv2.imshow('robot_view', frame1)
            cv2.imshow('rgbd_livingroom', frame2)
            cv2.imshow('omni_livingroom', frame3)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cap1.release()
                cap2.release()
                cap3.release()
                # Closes all the frames
                cv2.destroyAllWindows()
                break


def main():
    cap_name = '1'
    get_videos(cap_name)
    capture_action()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
