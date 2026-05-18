import cv2

def draw_status(frame, status, ear, fps, color):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], 80), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    cv2.putText(frame, status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2, cv2.LINE_AA)
    cv2.putText(frame, f'EAR: {ear:.2f}', (20, 72), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f'FPS: {fps:.1f}', (frame.shape[1] - 200, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    if status == 'DROWSINESS DETECTED':
        cv2.putText(frame, 'WAKE UP', (frame.shape[1] // 2 - 120, frame.shape[0] - 40), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
