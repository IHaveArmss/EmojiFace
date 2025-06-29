import cv2
import mediapipe as mp
import tkinter as tk
from threading import Thread
from queue import Queue, Empty
import time
import simpleaudio as sa
from pydub import AudioSegment

bleehAudio = AudioSegment.from_file("blehh.wav")
huhhhAudio = AudioSegment.from_file("huhhh.wav")

mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)

UPPER_LIP_IDX = 13
LOWER_LIP_IDX = 14
LEFT_EYEBROW_IDX = 65
LEFT_EYE_TOP_IDX = 159

lastBleehPlayTime = 0
lastHuhPlayTime = 0
cooldownSeconds = 1.0

def getMouthOpenDistance(landmarks, imageHeight):
    topLip = landmarks[UPPER_LIP_IDX]
    bottomLip = landmarks[LOWER_LIP_IDX]
    return abs(bottomLip.y - topLip.y) * imageHeight

def getEyebrowRaiseDistance(landmarks, imageHeight):
    eyebrow = landmarks[LEFT_EYEBROW_IDX]
    eyeTop = landmarks[LEFT_EYE_TOP_IDX]
    return abs(eyeTop.y - eyebrow.y) * imageHeight

class EmojiWindow:
    def __init__(self, emojiQueue):
        self.root = tk.Tk()
        self.root.title("Emoji Display")
        self.root.attributes('-topmost', True)
        self.label = tk.Label(self.root, text="😐", font=("Arial", 150))
        self.label.pack(padx=20, pady=20)
        self.emojiQueue = emojiQueue
        self.running = True
        self.updateLabel()

    def updateLabel(self):
        try:
            while True:
                emoji = self.emojiQueue.get_nowait()
                self.label.config(text=emoji)
        except Empty:
            pass
        if self.running:
            self.root.after(100, self.updateLabel)

    def run(self):
        self.root.mainloop()

    def close(self):
        self.running = False
        self.root.quit()

def runOpenCV(emojiQueue):
    global lastBleehPlayTime, lastHuhPlayTime
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceMesh.process(rgbFrame)

        emoji = "😐"
        currentTime = time.time()

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            h, _, _ = frame.shape

            mouthOpenDist = getMouthOpenDistance(landmarks, h)
            eyebrowRaiseDist = getEyebrowRaiseDistance(landmarks, h)

            if mouthOpenDist > 20:
                emoji = "😛"
                if currentTime - lastBleehPlayTime >= cooldownSeconds:
                    lastBleehPlayTime = currentTime
                    Thread(target=playBleehSound, daemon=True).start()

            elif eyebrowRaiseDist > 20:  # you can tweak this value
                emoji = "😲"
                if currentTime - lastHuhPlayTime >= cooldownSeconds:
                    lastHuhPlayTime = currentTime
                    Thread(target=playHuhhhSound, daemon=True).start()

            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.multi_face_landmarks[0], mpFaceMesh.FACEMESH_TESSELATION,
                mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1),
                mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)
            )

        emojiQueue.put(emoji)
        cv2.imshow("Webcam Feed", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def playBleehSound():
    playObj = sa.play_buffer(bleehAudio.raw_data,
                             num_channels=bleehAudio.channels,
                             bytes_per_sample=bleehAudio.sample_width,
                             sample_rate=bleehAudio.frame_rate)
    playObj.wait_done()

def playHuhhhSound():
    playObj = sa.play_buffer(huhhhAudio.raw_data,
                             num_channels=huhhhAudio.channels,
                             bytes_per_sample=huhhhAudio.sample_width,
                             sample_rate=huhhhAudio.frame_rate)
    playObj.wait_done()

if __name__ == "__main__":
    emojiQueue = Queue()
    emojiWin = EmojiWindow(emojiQueue)
    t = Thread(target=runOpenCV, args=(emojiQueue,), daemon=True)
    t.start()
    try:
        emojiWin.run()
    finally:
        emojiWin.close()
