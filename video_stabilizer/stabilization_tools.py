import logging
import cv2
from video_stabilizer.frame import Frame


class TranslationalStabilizer:
    def __init__(self, frame_list):
        self.frames = self.create_frame_objects(frame_list)

    def create_frame_objects(self, frame_images):
        """takes in a list of images which make up the frames of the original input video.
        return a list of frame objects
        """
        frame_objects = []
        for frame in frame_images:
            frame_objects.append(Frame(frame))
        return frame_objects
