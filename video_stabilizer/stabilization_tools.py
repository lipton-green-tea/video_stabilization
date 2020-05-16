import logging
import cv2
import statistics
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

    def set_image_offsets(self):
        bfMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        for f1 in range(0, len(self.frames) - 1):
            f2 = f1 + 1
            f1_descriptors = self.frames[f1].descriptors
            f2_descriptors = self.frames[f2].descriptors
            matches = bfMatcher.match(f1, f2)
            # some kind of match filtering
            sorted_matches = sorted(matches, key=lambda x: x.distance)
            offsets = []
            for match in sorted_matches[:0.5*len(sorted_matches)]:
                kp1 = self.frames[f1].key_points[match.queryIdx]
                kp2 = self.frames[f2].key_points[match.trainIdx]
                offsets.append((kp2.pt[0] - kp1.pt[0], kp2.pt[1] - kp1.pt[1]))
            x_offsets = [x[0] for x in offsets]
            y_offsets = [x[1] for x in offsets]

            mean_x_offset = statistics.mean(x_offsets)
            mean_y_offset = statistics.mean(y_offsets)

            std_x_offset = statistics.stdev(x_offsets)
            std_y_offset = statistics.stdev(y_offsets)

            length = len(offsets)

            for index in reversed(range(0, length)):
                if x_offsets[index] > mean_x_offset + std_x_offset or x_offsets[index] < mean_x_offset - std_x_offset:
                    del x_offsets[index]
                    del y_offsets[index]
                elif y_offsets[index] > mean_y_offset + std_y_offset or y_offsets[index] < mean_y_offset - std_y_offset:
                    del x_offsets[index]
                    del y_offsets[index]

            relative_x_offset = statistics.mean(x_offsets)
            relative_y_offset = statistics.mean(y_offsets)

            overall_x_offset = self.frames[f1].global_x_offset + relative_x_offset
            overall_y_offset = self.frames[f1].global_y_offset + relative_y_offset

            self.frames[f2].relative_x_offset = relative_x_offset
            self.frames[f2].relative_y_offset = relative_y_offset
            self.frames[f2].global_x_offset = overall_x_offset
            self.frames[f2].global_y_offset = overall_y_offset
