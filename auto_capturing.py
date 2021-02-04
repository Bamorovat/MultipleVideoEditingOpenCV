import cv2
import os
import numpy as np
from time import sleep

cap1 = None
cap2 = None
cap3 = None
cap4 = None

out1 = None
out2 = None
out3 = None
out4 = None

check = None

status = None

livingroom_frame_number = 0
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

robot_view_path = '/home/abbas/phd/dataset/video/robot_view/'
rgbd_livingroom_path = '/home/abbas/phd/dataset/video/rgbd_livingroom/'
omni_livingroom_path = '/home/abbas/phd/dataset/video/omni_livingroom/'
rgbd_sofa_path = '/home/abbas/phd/dataset/video/rgbd_sofa/'

action_robot_view_path = '/home/abbas/phd/dataset/action/robot_view/'
action_rgbd_livingroom_path = '/home/abbas/phd/dataset/action/rgbd_livingroom/'
action_omni_livingroom_path = '/home/abbas/phd/dataset/action/omni_livingroom/'
action_rgbd_sofa_path = '/home/abbas/phd/dataset/action/rgbd_sofa/'


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
    # cv2.moveWindow('image', 250, 150)
    # cv2.moveWindow('controls', 250, 50)

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
        cv2.setTrackbarPos('Frame_number', 'robot_view', ii)
        cv2.setTrackbarPos('Frame_number', 'rgbd_livingroom', ii)
        cv2.setTrackbarPos('Frame_number', 'omni_livingroom', ii)
        cv2.setTrackbarPos('Frame_number', 'rgbd_sofa', ii)
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
    file_name = getNextFilePath(action_robot_view_path, class_name)
    file_name = str(file_name)
    # folder_name =
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # 'X','V','I','D' _ (*'MJPG') _ *'XVID'
    # out = cv2.VideoWriter(os.path.join(path, (output_name + '.avi')), fourcc, 30.0, frame_size)
    out1 = cv2.VideoWriter(os.path.join(action_robot_view_path, class_name, (file_name + '.avi')), fourcc, 30.0, (640, 480))
    out2 = cv2.VideoWriter(os.path.join(action_rgbd_livingroom_path, class_name, (file_name + '.avi')), fourcc, 30.0, (640, 480))
    out3 = cv2.VideoWriter(os.path.join(action_omni_livingroom_path, class_name, (file_name + '.avi')), fourcc, 30.0, (512, 486))
    out4 = cv2.VideoWriter(os.path.join(action_rgbd_sofa_path, class_name, (file_name + '.avi')), fourcc, 30.0, (640, 480))


def create_class_folder(class_name):
    dir_path_robot_view = os.path.join(action_robot_view_path, class_name)
    dir_path_rgbd_livingroom = os.path.join(action_rgbd_livingroom_path, class_name)
    dir_path_omni_livingroom = os.path.join(action_omni_livingroom_path, class_name)
    dir_path_rgbd_sofa = os.path.join(action_rgbd_sofa_path, class_name)
    os.mkdir(dir_path_robot_view)
    os.mkdir(dir_path_rgbd_livingroom)
    os.mkdir(dir_path_omni_livingroom)
    os.mkdir(dir_path_rgbd_sofa)
    print("Successfully created the directory")
    return


def getClassName():
    global check
    class_name = input("What is The Class Name:")
    print("The Class name is " + class_name)
    class_list = open('/home/abbas/phd/dataset/action/Class_List.txt', 'r+')
    class_list_readline = class_list.readlines()
    # print(class_list_readline)
    print("Checking for the class ...")
    for line in class_list_readline:
        if class_name not in line:
            check = True
        elif class_name in line:
            check = False
            print("The Class is Existed")
            break

    if check:
        print("The New Class is Adding ...")
        create_class_folder(class_name)
        class_list.write(class_name + '\n')
        print("The New Class Added")

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
    cap1.set(cv2.CAP_PROP_POS_FRAMES, i + 1)
    cap2.set(cv2.CAP_PROP_POS_FRAMES, i)
    cap3.set(cv2.CAP_PROP_POS_FRAMES, i+120)
    cap4.set(cv2.CAP_PROP_POS_FRAMES, i)
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
        cap1.set(cv2.CAP_PROP_POS_FRAMES, livingroom_frame_number+1)
        cap2.set(cv2.CAP_PROP_POS_FRAMES, livingroom_frame_number)
        cap3.set(cv2.CAP_PROP_POS_FRAMES, livingroom_frame_number+120)
        cap4.set(cv2.CAP_PROP_POS_FRAMES, livingroom_frame_number)

        ret1, im1 = cap1.read()
        ret2, im2 = cap2.read()
        ret3, im3 = cap3.read()
        ret4, im4 = cap4.read()

        cv2.imshow('robot_view', im1)
        cv2.imshow('rgbd_livingroom', im2)
        cv2.imshow('omni_livingroom', im3)
        cv2.imshow('rgbd_sofa', im4)

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
            print("The Start Frame Number is : ", frame_start)
            status = 'stay'
        if status == 'Frame_End':
            frame_end = cv2.getTrackbarPos('Frame_number', 'rgbd_livingroom')
            print("The Last Frame Number is: ", frame_end)
            print('Please Wait: The videos are recording ...')
            record()
            print('Continue: The videos are recorded')
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
            cv2.imwrite("./" + "Snap_" + str(livingroom_frame_number) + ".jpg", im1)
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
    cap_name = '2'
    get_videos(cap_name)
    player_init()

    while off == 0:
        play()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()



'''
r11 = 750.0 / im1.shape[1]
dim1 = (750, int(im1.shape[0] * r11))
im1 = cv2.resize(im1, dim1, interpolation=cv2.INTER_AREA)

r22 = 750.0 / im2.shape[1]
dim2 = (750, int(im2.shape[0] * r22))
im2 = cv2.resize(im2, dim2, interpolation=cv2.INTER_AREA)

r33 = 750.0 / im3.shape[1]
dim3 = (750, int(im3.shape[0] * r33))
im3 = cv2.resize(im3, dim3, interpolation=cv2.INTER_AREA)

if im1.shape[0] > 600:
    im1 = cv2.resize(im1, (500, 500))
    controls = cv2.resize(controls, (im1.shape[1], 25))

if im2.shape[0] > 600:
    im2 = cv2.resize(im2, (500, 500))
    # controls = cv2.resize(controls, (im2.shape[1], 25))

if im3.shape[0] > 600:
    im3 = cv2.resize(im3, (500, 500))
    # controls = cv2.resize(controls, (im3.shape[1], 25))
    
    
    if not class_list_readline:
        print("The New Class is Adding ...")
        create_class_folder(class_name)
        class_list.write(class_name + '\n')
        print("The New Class Added")
    elif class_list_readline:

'''
