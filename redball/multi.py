from IPython.display import display, Image, Audio

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
import time
from openai import OpenAI, AsyncOpenAI
import os
import requests

client = OpenAI(api_key=os.environ.get("openaiapikey.txt"))
# Aclient = AsyncOpenAI(api_key=os.environ.get("openaiapikey.txt"))

videoList = ["data/pillow.mp4", "data/living.mp4"]
currentIndex = 0
def robotCapture():
    global currentIndex
    video = cv2.VideoCapture(videoList[currentIndex])
    base64Frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
    video.release()
    currentIndex += 1
    return base64Frames

# wait 
promptMessages = [
    {   "role": "system", 
        "content": "You are a intelligent robot dog. "
    }
]
params = {
    "model": "gpt-4-vision-preview",
    "messages": promptMessages,
    "max_tokens": 200,
}

goal = {
    "role": "user",``
    "content": ["Your mission is to find a pillow. These are frames from a video that you take with your vision camera." 
                "In which direction you decide to go first? Please just tell your decision or plan. Do not elaborate your logic.", ## micRead() + ~~~
        *map(lambda x: {"image": x, "resize": 768}, robotCapture()[0::90])
    ] 
}
promptMessages.append(goal)

for i in range(3):
    result = client.chat.completions.create(**params)
    assistant = result.choices[0].message.content ## "Go straight ahead into the room with the couch"
    print(assistant)

    promptMessages.append({"role": "assistant", "content": assistant})
    promptMessages.append({"role": "user", "content": [inputWithTimeout(5sec),
                                                       *map(lambda x: {"image": x, "resize": 768}, robotCapture()[0::50])]})
    
inputVoice()
