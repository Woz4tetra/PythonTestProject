import time
import sys
import os
import cv2

def get_platform():
    """Use for platform specific operations"""
    if sys.platform.startswith('darwin'):  # OS X
        return "mac"
    elif (sys.platform.startswith('linux') or sys.platform.startswith(
            'cygwin')):
        return "linux"
    elif sys.platform.startswith('win'):  # Windows
        return "win"
    else:
        return None

class Capture:
    """A general class for reading from live cameras or video files"""
    def __init__(self, width, height, window_name, enable_draw, update_fn=None,
                 fn_params=None):

        # each platform has its own key codes
        platform = get_platform()
        if platform == "linux":
            self.key_codes = {
                65362: "up",
                65364: "down",
                65361: "left",
                65363: "right",
                'esc': 'esc',
                10: "enter"
            }
        elif platform == "mac":
            self.key_codes = {
                63232: "up",
                63233: "down",
                63234: "left",
                63235: "right",
                13: "enter"
            }
        else:
            raise NotImplementedError

        self.width = width
        self.height = height

        self.window_name = window_name
        self.enable_draw = enable_draw

        self.frame = None

        # object wrapper for a video recorded from the current stream
        # Yes. It's possible to make videos from other video files
        self.recording = None
        self.recorder_width, self.recorder_height = 0, 0
        self.recorder_output_dir = ""
        self.is_recording = False

        # keep track of the frame number. Used for slider behavior
        self.frame_num = 0
        self.slider_num = 0

        # Capture status variables
        self.paused = False
        self.stopped = False

        # Capture runs on a thread. You may provide extra code to run inside
        # that thread
        self.update_fn = update_fn
        self.fn_params = fn_params

    def get_frame(self):
        """Get the current frame from the stream"""
        pass

    def set_frame(self, position):
        """Only applicable for videos. Jump the stream to a specific frame"""
        pass

    def current_pos(self):
        """Current frame number"""
        pass

    def increment_frame(self):
        """Jump the stream forward one frame"""
        pass

    def decrement_frame(self):
        """Jump the stream backward one frame"""
        pass

    def key_pressed(self, delay=1):
        """Get any keyboard events from opencv"""
        key = cv2.waitKey(delay)
        if key in self.key_codes:
            return self.key_codes[key]
        elif key > -1:
            if 0 <= key < 0x100:
                return chr(key)
            else:
                print(("Unrecognized key: " + str(key)))
        else:
            return key

    def save_frame(self, frame=None, image_name=None, add_timestamp=True,
                   directory=None):
        """
        Save the current (or provided) frame as a png. By default it
        saves it to the images directory
        """

        # you can add a timestamp to the image or make the timestamp the name
        if image_name is None:
            image_name = ""
        elif image_name is not None and add_timestamp:
            image_name += " "
        if add_timestamp:
            image_name += time.strftime("%c").replace(":", ";")

        if not image_name.endswith(".png"):
            image_name += ".png"

        print("Frame saved as " + str(image_name), end=" ")

        # select default directory
        if directory is None:
            directory = os.path.abspath(".")
        print("in directory:\n" + directory)

        if not os.path.isdir(directory):
            os.makedirs(directory)
        if directory[-1] != "/":
            directory += "/"

        # if no frame is provided, use the last frame
        if frame is None:
            frame = self.frame

        cv2.imwrite(directory + image_name, frame)

    def show_frame(self, frame=None):
        """
        Display the frame in the Capture's window using cv2.imshow. If no
        frame is provided, the previous frame is displayed
        """
        if self.enable_draw:
            if frame is not None:
                print(self.window_name)
                cv2.imshow(self.window_name, frame)
            elif self.frame is not None:
                cv2.imshow(self.window_name, self.frame)

    def start_recording(self, fps=32, video_name=None, add_timestamp=True,
                        output_dir=None, width=None, height=None,
                        with_frame=None):
        """
        Initialize the Capture's video writer.

        :param fps: The playback FPS of the video. This number can be finicky as
                the capture's current FPS may not match the video's output FPS.
                This is because video playback takes less computation than
                analyzing the video in this setting.
        :param video_name: The name of the video. If "", a time stamp will
                automatically be inserted
        :param add_timestamp: An optional parameter specifying whether the
                time should be included. True by default
        :param output_dir: directory to put video in
        :param width: provide a width and force the video to that size
        :param width: provide a height and force the video to that size
        :param with_frame: A numpy array containing a frame of the stream.
            This frame will be used to define the size of the video

        :return: None
        """
        video_format = 'avi'
        codec = 'MJPG'

        if video_name is None:
            video_name = ""
        elif video_name is not None and add_timestamp:
            video_name += " "

        if add_timestamp:
            video_name += time.strftime("%c").replace(":", ";")

        video_name += "." + video_format

        if output_dir is None:
            output_dir = os.path.abspath(".")
        else:
            output_dir += "/"

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        output_dir += video_name

        fourcc = cv2.VideoWriter_fourcc(*codec)
        self.recording = cv2.VideoWriter()

        if width is None and with_frame is None:
            self.recorder_width = self.width
        else:
            if width is not None:
                self.recorder_width = width
            elif with_frame is not None:
                self.recorder_width = with_frame.shape[1]

        if height is None and with_frame is None:
            self.recorder_height = self.height
        else:
            if height is not None:
                self.recorder_height = height
            elif with_frame is not None:
                self.recorder_height = with_frame.shape[0]

        print(self.recorder_width, self.recorder_height)
        self.recording.open(output_dir, fourcc, fps,
                            (self.recorder_width, self.recorder_height), True)
        self.recorder_output_dir = output_dir
        print("Initialized video named '%s'." % video_name)

        self.is_recording = True

    def record_frame(self, frame=None):
        """Write the frame to the Capture's initialized video capture"""
        if frame is None:
            frame = self.frame

        if frame.shape[0:2] != (self.recorder_height, self.recorder_width):
            frame = cv2.resize(frame,
                               (self.recorder_height, self.recorder_width))
        if len(frame.shape) == 2:
            self.recording.write(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))
        else:
            self.recording.write(frame)

    def stop_recording(self):
        """Close the initialized video capture"""
        if self.recording is not None:
            self.recording.release()
            print("Video written to:\n" + self.recorder_output_dir)

            self.recording = None

            self.is_recording = False

    def stop(self):
        """Stop the capture. If a recording is running, end it."""
        self.stop_recording()
        if self.enable_draw:
            cv2.destroyWindow(self.window_name)

        # indicate that the thread should be stopped
        self.stopped = True


class Video(Capture):
    """
    A wrapper class for opencv's video capture functionality.
    Only accepts the avi, mov, and mp4 video formats
    """
    def __init__(self, video_name, directory=None, enable_draw=True,
                 start_frame=0, width=None, height=None, frame_skip=0,
                 loop_video=False):
        """
        :param video_name: the file name of the video
        :param directory: directory of the video. Uses the default directory
            (named videos) if None provided
        :param enable_draw: whether the opencv window should be shown
            (boosts frames per second)
        :param start_frame: frame number to start the video at
        :param width: set a width for the video
        :param height: set a height for the video
        :param frame_skip: number of frames to skip every iteration
        :param loop_video: if True the stream will jump back to the beginning
            of the video, else it will end the stream
        """
        super(Video, self).__init__(width, height, video_name, enable_draw)

        self.resize_width = width
        self.resize_height = height

        video_name, capture, length_msec, num_frames, self.slider_ticks, \
            self.track_bar_name = self.load_video(video_name, directory)

        self.width, self.height, self.resize_width, self.resize_height, \
            self.resize_frame = self.init_dimensions(
                self.resize_width, self.resize_height, capture)

        # other video properties
        self.frame_skip = frame_skip
        self.loop_video = loop_video

        self.video_name = video_name

        self.capture = capture

        self.video_len = num_frames

        self.slider_has_moved = False

        if start_frame > 0:
            self.set_frame(start_frame)

    def init_dimensions(self, resize_width, resize_height, capture):
        width, height = int(capture.get(
            cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(
            cv2.CAP_PROP_FRAME_HEIGHT))

        # only resize the frame if the width and height of the video don't
        # match the given width and height
        if (resize_width is not None or resize_height is not None and
                (width, height) != (
                    resize_width, resize_height)):
            resize_frame = True
        else:
            resize_frame = False

        if resize_height is None and width is not None:
            resize_height = int(width * height / width)
        if resize_width is None and height is not None:
            resize_width = int(height * width / height)

        return width, height, resize_width, resize_height, resize_frame

    def show_frame(self, frame=None):
        """
        Display the frame in the Capture's window using cv2.imshow
        If no frame is provided, the previous frame is used.
        """
        if frame is not None:
            cv2.imshow(self.video_name, frame)
        else:
            cv2.imshow(self.video_name, self.frame)

    def load_video(self, video_name, directory):
        """Load a video file from a directory into an opencv capture object"""
        directory = os.path.abspath(directory)
#                                           ['avi', 'mov', 'mp4',
#                                            'AVI', 'MOV', 'MP4'])

        print("loading video into window named '" + str(
            video_name) + "'...")

        capture = cv2.VideoCapture(os.path.join(directory, video_name))

        cv2.namedWindow(video_name)

        # set the properties of the video
        fps = capture.get(cv2.CAP_PROP_FPS)
        num_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if num_frames <= 0:
            raise Exception("Video failed to load! "
                            "Did you misspell the video name?")

        length_sec = num_frames / fps
        length_msec = int(length_sec * 1000)

        print("\tfps:", fps)
        print("\tlength (sec):", length_sec)
        print("\tlength (frames):", num_frames)

        # initialize the track bar and the number of ticks it has
        slider_ticks = int(self.resize_width / 3)

        if slider_ticks > num_frames:
            slider_ticks = num_frames
        track_bar_name = "frame:"
        cv2.createTrackbar(track_bar_name, video_name, 0, slider_ticks,
                           self.on_slider)

        print("video loaded!")
        return video_name, capture, length_msec, num_frames, slider_ticks, track_bar_name

    def get_frame(self, advance_frame=True):
        """Get a new frame from the video stream and return it"""
        if self.frame_skip > 0:
            self.set_frame(self.current_pos() + self.frame_skip)

        success, self.frame = self.capture.read()
        if not advance_frame:
            self.set_frame(self.current_pos() - 1)

        if success is False or self.frame is None:
            if self.loop_video:
                self.set_frame(0)
                while success is False or self.frame is None:
                    success, self.frame = self.capture.read()
            else:
                self.stop()
                return None
        if self.resize_frame:
            self.frame = cv2.resize(self.frame,
                                    (self.resize_width, self.resize_height),
                                    interpolation=cv2.INTER_NEAREST)
        if self.current_pos() != self.frame_num:
            self.frame_num = self.current_pos()
            self.slider_num = int(
                self.frame_num * self.slider_ticks / self.video_len)
            cv2.setTrackbarPos(self.track_bar_name, self.video_name,
                               self.slider_num)
        return self.frame

    def current_pos(self):
        """Get the current frame number of the video"""
        return int(self.capture.get(cv2.CAP_PROP_POS_FRAMES))

    def on_slider(self, slider_index):
        """When the slider moves, change the video's position"""
        self.slider_has_moved = True
        slider_pos = int(slider_index * self.video_len / self.slider_ticks)
        if abs(slider_pos - self.current_pos()) > 1:
            self.set_frame(slider_pos)
            self.show_frame(self.get_frame())
            self.frame_num = self.current_pos()
            self.slider_num = slider_index

    def slider_moved(self):
        """For external use. Check whether the slider moved involuntarily"""
        if self.slider_has_moved:
            self.slider_has_moved = False
            return True
        else:
            return False

    def set_frame(self, position):
        """Jump the stream to a frame number"""
        if position >= self.video_len:
            position = self.video_len
        if position >= 0:
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, int(position))

    def increment_frame(self):
        """Jump the stream forward one frame"""
        self.get_frame()
        self.slider_has_moved = True

    def decrement_frame(self):
        """Jump the stream backward one frame"""

        # it doesn't listen to me if I don't subtract 3...
        self.set_frame(self.current_pos() - 3)
        self.get_frame()
        self.slider_has_moved = True

class VideoRunner:
    def __init__(self):
        self.width = 480
        self.height = 320
    
        self.capture = Video("live plotting demo.mov", "/Users/Woz4tetra/Desktop",
            width=self.width, height=self.height)
        self.time_start = time.time()
        
    def run(self):
        while True:
            if not self.capture.paused or self.capture.slider_moved():
                if self.capture.get_frame() is None:
                    break
                
                self.capture.show_frame()

            if not self.update_keys():
                break


    def update_keys(self):
        key = self.capture.key_pressed()

        if key == 'q' or key == "esc":
            print("quitting...")
            return False  # exit program
        elif key == ' ':
            if self.capture.paused:
                print("%0.4fs: ...Video unpaused" % (
                    time.time() - self.time_start))
            else:
                print("%0.4fs: Video paused..." % (
                    time.time() - self.time_start))
            self.capture.paused = not self.capture.paused
        elif key == 's':
            self.capture.save_frame()
        elif key == 'v':
            if not self.capture.is_recording:
                self.capture.start_recording()
            else:
                self.capture.stop_recording()
        elif key == 'right':
            self.capture.increment_frame()
        elif key == 'left':
            self.capture.decrement_frame()

        if not self.capture.paused:
            self.capture.show_frame()

        return True  # don't exit program

VideoRunner().run()
