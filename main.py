import time
import cv2
from detector.eye_detector import EyeDetector
from alert.alarm import Alarm
from utils.visuals import draw_status

def main():
    detector = EyeDetector()
    alarm = Alarm()
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW if hasattr(cv2, 'CAP_DSHOW') else cv2.CAP_ANY)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not capture.isOpened():
        print('Unable to access camera')
        return
    previous_time = time.time()
    while True:
        success, frame = capture.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        frame, drowsy, ear = detector.process_frame(frame)
        if drowsy:
            alarm.trigger()
            status = 'DROWSINESS DETECTED'
            alert_color = (0, 0, 255)
        else:
            status = 'ALERT'
            alert_color = (0, 255, 0)
        current_time = time.time()
        fps = 1.0 / (current_time - previous_time) if current_time > previous_time else 0.0
        previous_time = current_time
        draw_status(frame, status, ear, fps, alert_color)
        cv2.imshow('Driver Drowsiness Detection System', frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
