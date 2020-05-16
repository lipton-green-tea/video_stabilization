import os
import cv2
import numpy as np


def create_padded_frames(frames):
    frame_width = frames[0].frame.shape[1]  # native pixel width of the images
    frame_height = frames[0].frame.shape[0]  # native pixel height of the images

    max_x_offset = max([frame.global_x_offset for frame in frames])
    min_x_offset = min([frame.global_x_offset for frame in frames])
    total_padding_width = round(max_x_offset) - round(min_x_offset)
    default_left_padding = round(min_x_offset) * -1
    default_right_padding = round(max_x_offset)
    total_padding_width = default_left_padding + default_right_padding
    padded_frame_width = frame_width + total_padding_width

    max_y_offset = max([frame.global_y_offset for frame in frames])
    min_y_offset = min([frame.global_y_offset for frame in frames])
    default_top_padding = round(min_y_offset) * -1
    default_bottom_padding = round(max_y_offset)
    total_padding_height = default_top_padding + default_bottom_padding
    padded_frame_height = frame_height + total_padding_height

    padded_frames = []

    for frame in frames:
        left_padding = default_left_padding + round(frame.global_x_offset)
        right_padding = total_padding_width - left_padding

        top_padding = default_top_padding + round(frame.global_y_offset)
        bottom_padding = total_padding_height - top_padding

        padded_frame = cv2.copyMakeBorder(frame.frame,
                                          top_padding,
                                          bottom_padding,
                                          left_padding,
                                          right_padding,
                                          cv2.BORDER_CONSTANT,
                                          np.array([255, 255, 255]))

        padded_frames.append(padded_frame)

    return padded_frames


def output_video_from_frames(frames, path, video_name):
    path_out = os.path.join(path, video_name + '.' + '.mp4')
    default_fps = 24
    size = (frames[0].shape[1], frames[0].shape[0])

    out = cv2.VideoWriter(path_out, cv2.VideoWriter_fourcc(*'MP4V'), default_fps, size)

    for frame in frames:
        out.write(frame)
    out.release()
