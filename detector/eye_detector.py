import urllib.request
from pathlib import Path

import cv2
import numpy as np

class EyeDetector:
    LEFT_EYE = [36, 37, 38, 39, 40, 41]
    RIGHT_EYE = [42, 43, 44, 45, 46, 47]

    MODEL_URL = 'https://raw.githubusercontent.com/kurnianggoro/GSOC2017/master/data/lbfmodel.yaml'

    def __init__(self, threshold=0.22, consecutive_frames=15):
        self.threshold = threshold
        self.consecutive_frames = consecutive_frames
        self.frame_counter = 0
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.facemark = self._create_facemark()

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(160, 160))
        ear = 0.0
        drowsy = False
        if len(faces) and self.facemark is not None:
            success, landmarks = self.facemark.fit(gray, faces)
            if success and landmarks:
                points = landmarks[0][0]
                left_ear = self._eye_aspect_ratio([tuple(points[i]) for i in self.LEFT_EYE])
                right_ear = self._eye_aspect_ratio([tuple(points[i]) for i in self.RIGHT_EYE])
                ear = float((left_ear + right_ear) / 2.0)
                if ear < self.threshold:
                    self.frame_counter += 1
                    if self.frame_counter >= self.consecutive_frames:
                        drowsy = True
                else:
                    self.frame_counter = 0
                self._draw_eye_landmarks(frame, points)
        else:
            if self.frame_counter:
                self.frame_counter -= 1
        return frame, drowsy, ear

    def _create_facemark(self):
        if not hasattr(cv2, 'face') or not hasattr(cv2.face, 'createFacemarkLBF'):
            return None
        model_path = self._ensure_model()
        facemark = cv2.face.createFacemarkLBF()
        facemark.loadModel(model_path)
        return facemark

    def _ensure_model(self):
        model_dir = Path(__file__).resolve().parent.parent / 'models'
        model_dir.mkdir(parents=True, exist_ok=True)
        model_path = model_dir / 'lbfmodel.yaml'
        if not model_path.exists():
            urllib.request.urlretrieve(self.MODEL_URL, str(model_path))
        return str(model_path)

    def _eye_aspect_ratio(self, points):
        p = np.array(points, dtype='float32')
        vertical_1 = np.linalg.norm(p[1] - p[5])
        vertical_2 = np.linalg.norm(p[2] - p[4])
        horizontal = np.linalg.norm(p[0] - p[3])
        return (vertical_1 + vertical_2) / (2.0 * horizontal) if horizontal else 0.0

    def _draw_eye_landmarks(self, frame, points):
        for idx in self.LEFT_EYE + self.RIGHT_EYE:
            cv2.circle(frame, tuple(int(v) for v in points[idx]), 2, (0, 255, 0), -1)
