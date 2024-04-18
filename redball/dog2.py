import base64
import os
import time
import datetime
import cv2
from openai import OpenAI

###################
# Run duration
MAX_ITER = 200
MAX_TIME = 200  # second


###################
# ACTION
STOP = 0
MOVE_FORWARD = 1
MOVE_LEFT = 2
MOVE_BACKWARD = 3
MOVE_RIGHT = 4
# LOOK_UP = 4
# LOOK_DOWN = 5
ACTION_DICT = {
    0: "Stop",
    1: "Move Forward",
    2: "Turn Left",
    3: "Move Backward",
    4: "Move Right",
}

#################################################

FORWARD_MAGN = 0.25  # 0.25 m / sec
ROTATION_MAGN = 0.1745  # 10 degree / sec
# SIDE_MAGN =     0.3
# BACKWARD_MAGN = 0.25

#################################################


class Dog:
    def __init__(self):
        self.capture: cv2.VideoCapture
        self.openai_client: OpenAI
        self.openai_prompt_messages = [
            {"role": "system", "content": "You are a intelligent robot dog. "}
        ]
        self.openai_params = {
            "model": "gpt-4-vision-preview",
            "messages": self.openai_prompt_messages,
            "max_tokens": 200,
        }
        self.openai_goal = {
            "role": "user",
            "content": [
                """If a red object is on the left side of the frame, prints '2'. 
                    If it is around the center, prints '1'. 
                    If it is on the right, prints '4'.
                    If there is no red object, say '0'.""",
                None,
            ],
        }
        self.openai_prompt_messages.append(self.openai_goal)

    def setup(self):
        self.connect_camera()
        f = open("openaiapikey.txt", "r")
        api_key = f.read()
        f.close()
        self.openai_client = OpenAI(api_key=api_key)

    def connect_camera(self):
        # Open the camera
        print("- Connect Cam")

        gstreamer_str = "udpsrc address=230.1.1.1 port=1720 multicast-iface=enx7cc2c64bce6b ! application/x-rtp, media=video, encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1"
        self.capture = cv2.VideoCapture(gstreamer_str, cv2.CAP_GSTREAMER)
        return

    def shutdown(self):
        # Close camera
        self.capture.release()
        cv2.destroyAllWindows()

    def get_image(self):
        ret, frame = self.capture.read()
        i2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame, i2
    
    def queryGPT_by_image(self, frame) -> str:
        _, buffer = cv2.imencode(".jpg", frame)
        decoded = base64.b64encode(buffer).decode("utf-8")
        self.openai_goal["content"][1] = {"image": decoded, "resize": 768}

        result = self.openai_client.chat.completions.create(**self.openai_params)
        assistant = result.choices[0].message.content
        return assistant

    def run(self, act_function=None):
        start = time.time()

        it = 0
        while True:
            it += 1
            # Read image and decide action
            frame, transformed = self.get_image()
            action = self.queryGPT_by_image(frame)
            print(action)

            img = cv2.putText(
                frame,
                action,
                (240, 40),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (0, 0, 255),  # red
                3,
                cv2.LINE_AA,
            )
            cv2.imshow("frame2", img)
            cv2.waitKey(1)
            # cv2.pollKey()

            # timeout
            if time.time() - start > constants.MAX_TIME:
                break

            if it >= constants.MAX_ITER:
                break
            # time.sleep(0.1)

        end = time.time()
        print(f"Run for {(end - start):.1f} sec, {it} iterations")
