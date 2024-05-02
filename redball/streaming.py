import cv2
gstreamer_str = "udpsrc address=230.1.1.1 port=1720 multicast-iface=enx7cc2c64bce6b ! application/x-rtp, media=video, encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1"
capture = cv2.VideoCapture(gstreamer_str, cv2.CAP_GSTREAMER)

# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
while (capture.isOpened()):
    ret, frame = capture.read()
    i2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    cv2.imshow("frame2", frame)
    cv2.waitKey(1)


'''
while(cap.isOpened()):
    ret, frame = capture.read()
    if ret:
        #print("Frame read successfully.")
        cv2.imshow("Input via Gstreamer", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        #print("Failed to read frame.")
        break
capture.release()
cv2.destroyAllWindows()'''


#if not cap.isOpened():
#    print("Failed to open video capture.")
#else:
#    print("Video capture opened successfully.")


# capture = cv2.VideoCapture(gstreamer_str, cv2.CAP_GSTREAMER)
# self.capture = cv2.VideoCapture(0)







# def try_all_port():
#     for port in range(100,65000):
#         connection_str = f"udpsrc address=192.168.123.161 port={port} multicast-iface=enx7cc2c64bce6b ! application/x-rtp, media=video, encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1"
#         cap = cv2.VideoCapture(connection_str, cv2.CAP_GSTREAMER)
#         if cap.isOpend():
#             print(port + " is opend")
#             break