import cv2
import os


class Capturing:

    def __init__(self, video_path, camera_name, video_name):

        self.cap = None

        # Create a VideoCapture object and read from input file
        # If the input is the camera, pass 0 instead of the video file name
        self.cap_path = video_path
        self.cap_name = video_name
        self.cap_camera = camera_name
        self.cap = cv2.VideoCapture(os.path.join(self.cap_path, (self.cap_name + '.avi')))

    def capture_action(self):

        # Check if camera opened successfully
        if not self.cap.isOpened():
            print("Error opening video stream or file")

        # Read until video is completed
        while self.cap.isOpened():
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if ret:
                # Display the resulting frame
                cv2.imshow(self.cap_camera, frame)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    self.cap.release()
                    # Closes all the frames
                    cv2.destroyAllWindows()
                    break


def main():
    robot_view_path = '/home/abbas/phd/dataset/video/robot_view/'
    rgbd_livingroom_path = '/home/abbas/phd/dataset/video/rgbd_livingroom/'
    omni_livingroom_path = '/home/abbas/phd/dataset/video/omni_livingroom/'

    name = '1'

    robot_view = Capturing(robot_view_path, 'robot_view', name)
    rgbd_livingroom = Capturing(rgbd_livingroom_path, 'rgbd_livingroom', name)
    omni_livingroom = Capturing(omni_livingroom_path, 'omni_livingroom', name)

    robot_view.capture_action()
    rgbd_livingroom.capture_action()
    omni_livingroom.capture_action()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
