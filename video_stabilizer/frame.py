import cv2


class Frame:
    def __init__(self, frame):
        self.frame = frame
        self.relative_x_offset = 0  # number of pixels offset from the top down, relative to the previous frame
        self.relative_y_offset = 0  # number of pixels offset from the left to the right, relative to the previous frame

        self.global_x_offset = 0  # number of pixels offset from the left to the right, relative to the first frame
        self.global_y_offset = 0  # number of pixels offset from the left to the right, relative to the first frame

        self.SIFT_filter = cv2.xfeatures2d.SIFT_create()

        self.key_points, self.descriptors = self.SIFT_filter.detectAndCompute(self.frame, None)
