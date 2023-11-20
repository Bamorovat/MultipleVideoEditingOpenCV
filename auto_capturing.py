"""
Multiple Video Editing tool  
@author Mohammad Abadi <m.bamorovvat@gmail.com>
"""


import cv2
import os
import numpy as np
from time import sleep

cap1 = None  # robot
cap2 = None  # living room RGB
cap3 = None  # living room omni
cap4 = None  # Sofa

out1 = None
out2 = None
out3 = None
out4 = None

check = None
status = None

robot_view_trimming = 0
living_room_view_trimming = 0
omni_view_trimming = 50
sofa_view_trimming = 0

livingroom_frame_number = 260

tots = 0
frame_rate = 30
off = 0
frame_start = 0
frame_end = 0

robot_view_frames_tots = 0
rgbd_livingroom_frames_tots = 0
omni_livingroom_frames_tots = 0
rgbd_sofa_frames_tots = 0

controls = np.zeros((50, 750, 3), np.uint8)

video_path = '/home/abbas/phd/dataset/video/'
robot_view_path = video_path + 'robot_view/' #'/home/abbas/phd/dataset/video/robot_view/'
rgbd_livingroom_path = video_path + 'rgbd_livingroom/' # '/home/abbas/phd/dataset/video/rgbd_livingroom/'
omni_livingroom_path = video_path + 'omni_livingroom/' # '/home/abbas/phd/dataset/video/omni_livingroom/'
rgbd_sofa_path = video_path + 'rgbd_sofa/' # '/home/abbas/phd/dataset/video/rgbd_sofa/'

action_path = '/home/abbas/phd/dataset/action/'
action_robot_view_path = action_path + 'robot_view/' # '/home/abbas/phd/dataset/action/robot_view/'
action_rgbd_livingroom_path = action_path + 'rgbd_livingroom/' #  '/home/abbas/phd/dataset/action/rgbd_livingroom/'
action_omni_livingroom_path = action_path + 'omni_livingroom/' # '/home/abbas/phd/dataset/action/omni_livingroom/'
action_rgbd_sofa_path = action_path + 'rgbd_sofa/' # '/home/abbas/phd/dataset/action/rgbd_sofa/'


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def get_videos(cap_name):
    global cap1, cap2, cap3, cap4
    cap1 = cv2.VideoCapture(os.path.join(robot_view_path, (cap_name + '.avi')))
    cap2 = cv2.VideoCapture(os.path.join(rgbd_livingroom_path, (cap_name + '.avi')))
    cap3 = cv2.VideoCapture(os.path.join(omni_livingroom_path, (cap_name + '.avi')))
    cap4 = cv2.VideoCapture(os.path.join(rgbd_sofa_path, (cap_name + '.avi')))


def frame_count():
    global cap1, cap2, cap3, cap4
    global robot_view_frames_tots
    global rgbd_livingroom_frames_tots
    global omni_livingroom_frames_tots
    global rgbd_sofa_frames_tots

    robot_view_frames_tots = cap1.get(cv2.CAP_PROP_FRAME_COUNT)
    rgbd_livingroom_frames_tots = cap2.get(cv2.CAP_PROP_FRAME_COUNT)
    omni_livingroom_frames_tots = cap3.get(cv2.CAP_PROP_FRAME_COUNT)
    rgbd_sofa_frames_tots = cap4.get(cv2.CAP_PROP_FRAME_COUNT)
    # print(robot_view_frames_tots, rgbd_livingroom_frames_tots, omni_livingroom_frames_tots)
    return


def track_bar(frame_total, frame_name1, frame_name2, image_name):
    frame_name1 = frame_name1
    frame_name2 = frame_name2
    image_name = image_name
    cv2.createTrackbar(frame_name1, image_name, 0, int(frame_total) - 1, flick)
    cv2.createTrackbar(frame_name2, image_name, 1, 100, flick)
    cv2.setTrackbarPos(frame_name1, image_name, 0)
    cv2.setTrackbarPos(frame_name2, image_name, frame_rate)
    return


def flick(y):
    pass


def player_init():
    global status
    global controls

    cv2.namedWindow('robot_view')
    cv2.namedWindow('rgbd_livingroom')
    cv2.namedWindow('omni_livingroom')
    cv2.namedWindow('rgbd_sofa')
    cv2.namedWindow('controls')
    cv2.moveWindow('controls', 500, 40)

    cv2.putText(controls, "W: Play | S: Stay | A: Prev | D: Next | Z: Frame_Start | X: Frame_End | C: Snap | Esc: Exit",
                (40, 30), cv2.FONT_HERSHEY_COMPLEX, 0.45, (100, 140, 60))

    frame_count()

    track_bar(robot_view_frames_tots, 'Frame_number', 'Frame_rate', 'robot_view')
    track_bar(rgbd_livingroom_frames_tots, 'Frame_number', 'Frame_rate', 'rgbd_livingroom')
    track_bar(omni_livingroom_frames_tots, 'Frame_number', 'Frame_rate', 'omni_livingroom')
    track_bar(rgbd_sofa_frames_tots, 'Frame_number', 'Frame_rate', 'rgbd_sofa')

    status = 'stay'


def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


def getTrackbarPos():
    frame_rate1 = cv2.getTrackbarPos('Frame_rate', 'robot_view')
    frame_rate2 = cv2.getTrackbarPos('Frame_rate', 'rgbd_livingroom')
    frame_rate3 = cv2.getTrackbarPos('Frame_rate', 'omni_livingroom')
    frame_rate4 = cv2.getTrackbarPos('Frame_rate', 'rgbd_sofa')

    sleep((0.1 - frame_rate1 / 1000.0) ** 21021)
    sleep((0.1 - frame_rate2 / 1000.0) ** 21021)
    sleep((0.1 - frame_rate3 / 1000.0) ** 21021)
    sleep((0.1 - frame_rate4 / 1000.0) ** 21021)
    return


def setTrackbarPos(name, ii):
    if name == 'S':
        cv2.setTrackbarPos('Frame_number', 'robot_view', (ii + robot_view_trimming))
        cv2.setTrackbarPos('Frame_number', 'rgbd_livingroom', (ii + living_room_view_trimming))
        cv2.setTrackbarPos('Frame_number', 'omni_livingroom', (ii + omni_view_trimming))
        cv2.setTrackbarPos('Frame_number', 'rgbd_sofa', (ii + sofa_view_trimming))
    elif name == 'F':
        cv2.setTrackbarPos('Frame_rate', 'robot_view', ii)
        cv2.setTrackbarPos('Frame_rate', 'rgbd_livingroom', ii)
        cv2.setTrackbarPos('Frame_rate', 'omni_livingroom', ii)
        cv2.setTrackbarPos('Frame_rate', 'rgbd_sofa', ii)
    return


def record_init():
    global out1, out2, out3, out4
    # name_path = '/home/abbas/phd/dataset/action/robot_view/'
    class_name = getClassName()
    # print('record_init: ', class_name)
    file_name = getNextFilePath(action_robot_view_path, class_name)
    file_name = str(file_name)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # 'X','V','I','D' _ (*'MJPG') _ *'XVID'
    # out = cv2.VideoWriter(os.path.join(path, (output_name + '.avi')), fourcc, 30.0, frame_size)
    out1 = cv2.VideoWriter(os.path.join(action_robot_view_path, class_name, (file_name + '.avi')), fourcc, 30.0,
                           (640, 480))
    out2 = cv2.VideoWriter(os.path.join(action_rgbd_livingroom_path, class_name, (file_name + '.avi')), fourcc, 30.0,
                           (640, 480))
    out3 = cv2.VideoWriter(os.path.join(action_omni_livingroom_path, class_name, (file_name + '.avi')), fourcc, 30.0,
                           (512, 486))
    out4 = cv2.VideoWriter(os.path.join(action_rgbd_sofa_path, class_name, (file_name + '.avi')), fourcc, 30.0,
                           (640, 480))


def create_class_folder(class_name):
    dir_path_robot_view = os.path.join(action_robot_view_path, class_name)
    dir_path_rgbd_livingroom = os.path.join(action_rgbd_livingroom_path, class_name)
    dir_path_omni_livingroom = os.path.join(action_omni_livingroom_path, class_name)
    dir_path_rgbd_sofa = os.path.join(action_rgbd_sofa_path, class_name)
    os.mkdir(dir_path_robot_view)
    os.mkdir(dir_path_rgbd_livingroom)
    os.mkdir(dir_path_omni_livingroom)
    os.mkdir(dir_path_rgbd_sofa)
    print("Successfully Created the Class Directory")
    return


def getClassName():
    global check
    class_name_confirmation = 'n'

    while class_name_confirmation != 'y':
        class_list = open('/home/abbas/phd/dataset/action/Class_List.txt', 'r+')
        class_list_readline = class_list.readlines()
        print(Color.BOLD + Color.DARKCYAN + 'Existing Classes Are: ' + Color.END)
        for i, line in enumerate(class_list_readline, start=1):
            # print(Color.DARKCYAN + str(line) + Color.END, sep=', ')    # '\n'
            print('{} = {}'.format(Color.CYAN + str(i), Color.CYAN + line.strip() + Color.END))
        class_name = input("What is The Class Name or Number:")
        if class_name.isdigit():
            print('You Enter the Class Number ...')
            for iii, line in enumerate(class_list_readline, start=1):
                if iii == int(class_name):
                    class_name = line.strip()
                    break
        print("The Class name is: " + Color.BOLD + Color.RED + Color.UNDERLINE + class_name + Color.END)
        class_name_confirmation = input('Is it the correct class name (y/n)? ')
        if class_name_confirmation == 'y':
            print(" Checking for the class ...")
            for line in class_list_readline:
                if class_name not in line:
                    check = True
                elif class_name in line:
                    check = False
                    print("The Class is Existed")
                    break

            if check:
                print(" The New Class is Adding ...")
                create_class_folder(class_name)
                class_list.write(class_name + '\n')
                print("The New Class is Added")
                return class_name
        elif class_name_confirmation == 'n':
            pass
        else:
            print('Error: Enter (y/n) ...')

    class_list.close()
    return class_name


def getNextFilePath(folder_path, class_name):
    action_class_path = os.path.join(folder_path, (class_name + "/"))
    # print("action_class_path is: ", action_class_path)
    highest_num = 0
    for f in os.listdir(action_class_path):
        if os.path.isfile(os.path.join(action_class_path, f)):
            file_name = os.path.splitext(f)[0]
            try:
                file_num = int(file_name)
                if file_num > highest_num:
                    highest_num = file_num
            except ValueError:
                'The file name "%s" is not an integer. Skipping' % file_name

    output_file = (highest_num + 1)
    return output_file


def record():
    # global out1, out2, out3
    # print(frame_start, frame_end)
    record_init()
    length = frame_end - frame_start
    i = frame_start
    # print(i)
    cap1.set(cv2.CAP_PROP_POS_FRAMES, i + robot_view_trimming)
    cap2.set(cv2.CAP_PROP_POS_FRAMES, i + living_room_view_trimming)
    cap3.set(cv2.CAP_PROP_POS_FRAMES, i + omni_view_trimming)
    cap4.set(cv2.CAP_PROP_POS_FRAMES, i + sofa_view_trimming)
    for i in range(length):
        # print(i)
        ret1, frame1 = cap1.read()
        out1.write(frame1)
        ret2, frame2 = cap2.read()
        out2.write(frame2)
        ret3, frame3 = cap3.read()
        out3.write(frame3)
        ret4, frame4 = cap4.read()
        out4.write(frame4)

    out1.release()
    out2.release()
    out3.release()
    out4.release()
    return


def image_write(i, im1, im2, im3, im4, image_name):
    cv2.imwrite("./" + "Snap_" + "robot_view_" + image_name + ".jpg", im1)
    cv2.imwrite("./" + "Snap_" + "living_room_" + image_name + ".jpg", im2)
    cv2.imwrite("./" + "Snap_" + "omni_view_" + image_name + ".jpg", im3)
    cv2.imwrite("./" + "Snap_" + "sofa_view_" + image_name + ".jpg", im4)

    # cv2.imwrite("./" + "Snap_" + "robot_view" + str(i + robot_view_trimming) + ".jpg", im1)
    # cv2.imwrite("./" + "Snap_" + "living_room" + str(i + living_room_view_trimming) + ".jpg", im2)
    # cv2.imwrite("./" + "Snap_" + "omni_view" + str(i + omni_view_trimming) + ".jpg", im3)
    # cv2.imwrite("./" + "Snap_" + "sofa_view" + str(i + sofa_view_trimming) + ".jpg", im4)
    # print("Snap of Frame", livingroom_frame_number, "Taken!")
    return


def play():
    global livingroom_frame_number
    global tots
    global status
    global controls
    global frame_rate
    global frame_start, frame_end

    cv2.imshow("controls", controls)

    try:
        if livingroom_frame_number == tots - 1:
            livingroom_frame_number = 0
        cap1.set(cv2.CAP_PROP_POS_FRAMES, livingroom_frame_number + robot_view_trimming)
        cap2.set(cv2.CAP_PROP_POS_FRAMES, livingroom_frame_number + living_room_view_trimming)
        cap3.set(cv2.CAP_PROP_POS_FRAMES, livingroom_frame_number + omni_view_trimming)
        cap4.set(cv2.CAP_PROP_POS_FRAMES, livingroom_frame_number + sofa_view_trimming)

        ret1, im1 = cap1.read()
        ret2, im2 = cap2.read()
        ret3, im3 = cap3.read()
        ret4, im4 = cap4.read()

        cv2.imshow('robot_view', im1)
        cv2.moveWindow('robot_view', 100, 40)
        cv2.imshow('rgbd_livingroom', im2)
        cv2.moveWindow('rgbd_livingroom', 750, 40)
        cv2.imshow('omni_livingroom', im3)
        cv2.moveWindow('omni_livingroom', 1400, 40)
        cv2.imshow('rgbd_sofa', im4)
        cv2.moveWindow('rgbd_sofa', 1400, 700)

        status = {ord('s'): 'stay', ord('S'): 'stay',
                  ord('w'): 'play', ord('W'): 'play',
                  ord('a'): 'prev_frame', ord('A'): 'prev_frame',
                  ord('d'): 'next_frame', ord('D'): 'next_frame',
                  ord('q'): 'slow', ord('Q'): 'slow',
                  ord('e'): 'fast', ord('E'): 'fast',
                  ord('c'): 'snap', ord('C'): 'snap',
                  ord('z'): 'Frame_Start', ord('Z'): 'Frame_Start',
                  ord('x'): 'Frame_End', ord('X'): 'Frame_End',
                  -1: status,
                  27: 'exit'}[cv2.waitKey(10)]

        setTrackbarPos('S', livingroom_frame_number)

        if status == 'play':
            getTrackbarPos()
            livingroom_frame_number += 1
            setTrackbarPos('S', livingroom_frame_number)
        if status == 'stay':
            livingroom_frame_number = cv2.getTrackbarPos('Frame_number', 'rgbd_livingroom')
        if status == 'exit':
            destroy()
        if status == 'prev_frame':
            livingroom_frame_number -= 1
            setTrackbarPos('S', livingroom_frame_number)
            status = 'stay'
        if status == 'next_frame':
            livingroom_frame_number += 1
            setTrackbarPos('S', livingroom_frame_number)
            status = 'stay'
        if status == 'Frame_Start':
            frame_start = cv2.getTrackbarPos('Frame_number', 'rgbd_livingroom')
            print(Color.BLUE + "################## Start Capturing ################# " + Color.END)
            print("The Start Frame Number is : " + Color.BOLD + Color.PURPLE + str(frame_start) + Color.END)
            # print("The Start Frame Number is : ", frame_start)
            status = 'stay'
        if status == 'Frame_End':
            frame_end = cv2.getTrackbarPos('Frame_number', 'rgbd_livingroom')
            print("The Last Frame Number is: " + Color.BOLD + Color.PURPLE + str(frame_end) + Color.END)
            print(' Please Wait ... ')
            print(' The Videos Are Saving ... ')
            record()
            print('The Videos Are Saved ')
            print(Color.YELLOW + "################## End Capturing ################# " + Color.END)
            status = 'stay'
        if status == 'slow':
            frame_rate = max(frame_rate - 5, 0)
            setTrackbarPos('F', frame_rate)
            status = 'play'
        if status == 'fast':
            frame_rate = min(100, frame_rate + 5)
            setTrackbarPos('F', frame_rate)
            status = 'play'
        if status == 'snap':
            image_name = input('what is the action name ')
            image_write(livingroom_frame_number, im1, im2, im3, im4, image_name)
            # cv2.imwrite("./" + "Snap_" + str(livingroom_frame_number) + ".jpg", im1)
            print("Snap of Frame", livingroom_frame_number, "Taken!")
            status = 'stay'

    except KeyError:
        print("Invalid Key was pressed")


def destroy():
    global off
    off = 1
    cap1.release()
    cap2.release()
    cap3.release()
    cap4.release()

    cv2.destroyWindow('robot_view')
    cv2.destroyWindow('rgbd_livingroom')
    cv2.destroyWindow('omni_livingroom')
    cv2.destroyWindow('rgbd_sofa')
    cv2.destroyWindow('controls')


def main():
    cap_name = '10'
    get_videos(cap_name)
    player_init()

    while off == 0:
        play()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

