import base64
import os
import time
# import datetime
import cv2
from openai import OpenAI
import signal
import sys

sys.path.append('/home/seungwan/Desktop/our_go2/lib/python/x86_64/')
import robot_interface as sdk


def alarm_handler(signum, frame):
    raise TimeoutError

def timeoutInput(timeout):
    s = ""
    if timeout is not None:
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(timeout)
    try:
        while True:
            c = sys.stdin.read(1)
            s += c
            if c == '\n':
                break
    except TimeoutError as err:
        return s
    finally:
        if timeout is not None:
            signal.alarm(0)
    return s

###################
# Run duration
MAX_ITER = 50
MAX_TIME = 200  # second

###################
# Action dictionary
ACTION_DICT = {
    0: "Stop",
    1: "Move Forward",
    2: "Move Left",
    3: "Move Right",
    4: "Rotate",
}
#################################################

class Dog:
    def __init__(self):
        self.capture: cv2.VideoCapture
        self.openai_client: OpenAI
        self.openai_prompt_messages = [
            {"role": "system", "content": "You are a intelligent robot dog. "}
        ]
        self.openai_prompt_messages_for_feedback = [
            {"role": "system", "content": "You are a intelligent robot dog. "}
        ]
        self.openai_params = {
            "model": "gpt-4-vision-preview",
            "messages": self.openai_prompt_messages,
            "max_tokens": 200,
        }
        self.openai_params_for_feedback = {
            "model": "gpt-4-vision-preview",
            "messages": self.openai_prompt_messages_for_feedback,
            "max_tokens": 200,
        }
        self.openai_goal = {
            "role": "user",
            "content": [
                """If a water bottle is around the center, print '1'.  
                    If it is on the left side of the frame, print '2'.
                    If it is on the right, print '3'.
                    If it is close enough to the robot, print '0'.
                    If there is no water bottle, print '4'.""",
                None,
            ],
        }
        self.prefix_for_feedback = """Here is an action dictionary: {
            0: "Stop",
            1: "Move Forward",
            2: "Move Left",
            3: "Move Right",
            4: "Rotate right",
            5: "Rotate left"
            }
            According to the above action dictionary, you are only allowed to output the corresponding number as an answer by interpreting the command: """
        self.openai_goal_for_feedback = {
            "role": "user",
            "content": [
                "",
                # None,
            ],
        }
        self.openai_prompt_messages.append(self.openai_goal)
        self.openai_prompt_messages_for_feedback.append(self.openai_goal_for_feedback)

    def setup(self):
        self.connect_camera()
        f = open("openaiapikey.txt", "r")
        api_key = f.read()
        f.close()
        self.openai_client = OpenAI(api_key=api_key)

    def connect_camera(self):
        # Open the camera
        print("- Connect Cam")
        # By connecting to the robot
        gstreamer_str = "udpsrc address=230.1.1.1 port=1720 multicast-iface=enx7cc2c64bce6b ! application/x-rtp, media=video, encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1"

        # Without connecting to the robot
        # gstreamer_str = "udpsrc address=230.1.1.1 port=1720 ! application/x-rtp, media=video, encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1"

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
        print(assistant)
    
    def queryGPT_by_image_with_feedback(self, frame, inp) -> str:
        # _, buffer = cv2.imencode(".jpg", frame)
        # decoded = base64.b64encode(buffer).decode("utf-8")
        self.openai_goal_for_feedback["content"][0] = self.prefix_for_feedback + inp
        # self.openai_goal_for_feedback["content"][1] = {"image": decoded, "resize": 768}

        result = self.openai_client.chat.completions.create(**self.openai_params_for_feedback)
        assistant = result.choices[0].message.content
        return assistant

    def activate_sportclient(self, ans):
        # if len(sys.argv) < 2:
        #     print(f"Usage: {sys.argv[0]} networkInterface")
        #     return -1
        
        # Assuming that the ChannelFactory and Init methods are properly bound in Python
        # sdk.ChannelFactory.Instance().Init(0, sys.argv[1])
        chan = sdk.ChannelFactory.Instance()
        chan.Init(0, "enx7cc2c64bce6b")

        # Initialize the sport client, assuming the translated classes have the same functionality
        sport_client = sdk.SportClient(False)
        sport_client.SetTimeout(10.0)
        sport_client.Init()
        
        # Alpha test
        if ans == '1':
            sport_client.Move(0.8, 0, 0) # forward
        elif ans == '2':
            sport_client.Move(0, 0.8, 0) # left
        elif ans == '3':
            sport_client.Move(0, -0.8, 0) # right
        elif ans == '4':
            sport_client.Move(0, 0, -2) # rotate
        elif ans == '5':
            sport_client.Move(0, 0, 2) # rotate
        elif ans == '0':
            sport_client.StopMove()  # stop 
        # else:
        #     sport_client.StopMove()  # stop 

        return 0

    def run(self, act_function=None):
        for i in range(10):
            frame, transformed = self.get_image()
            _, buffer = cv2.imencode(".jpg", frame)
            decoded = base64.b64encode(buffer).decode("utf-8")
            self.openai_goal["content"][1] = {"image": decoded, "resize": 768}
            self.openai_prompt_messages.append(self.openai_goal)

            result = self.openai_client.chat.completions.create(**self.openai_params)
            assistant = result.choices[0].message.content
            print(assistant)
            self.activate_sportclient(assistant)

            self.openai_prompt_messages.append({"role": "assistant", "content": assistant})
            self.openai_goal = {
                "role": "user",
                "content": [self.prefix_for_feedback + input(), None,],}
