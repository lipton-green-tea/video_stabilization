import cv2


def create_frames(image_path):
    cap = cv2.VideoCapture(image_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is False:
            break
        frames.append(frame)

    cap.release()
    cv2.destroyAllWindows()
    return frames
