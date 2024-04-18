#!/usr/bin/env python3
import dog2

import sys
import time
import math
import asyncio
import threading

sys.path.append('/home/yeonsoo/Desktop/our_go2/lib/python/x86_64/')
import robot_interface as sdk



def act_function(p1, p2, p3):
    if p1 > p2 and p2 >= p3:
        action = dog2.TURN_LEFT
    elif p1 > p2 and p2 < p3 and p3 < p1:
        action = dog2.TURN_LEFT
    elif p1 == p2 and p2 > p3:
        action = dog2.TURN_LEFT
    elif p1 > p2 and p2 < p3 and p3 == p1:
        action = dog2.STOP
    elif p1 == p2 and p2 == p3:
        action = dog2.STOP
    elif p1 < p2 and p2 > p3:
        action = dog2.MOVE_FORWARD
    else:
        action = dog2.TURN_RIGHT
    return action

def activate_sportclient(ans):
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
    
    if ans == 1:
        sport_client.Move(0.8, 0, 0) # forward
    elif ans == 2:
        sport_client.Move(0, 0.8, 0) # left
    elif ans == 3:
        sport_client.Move(-0.8, 0, 0) # backward
    elif ans == 4:
        sport_client.Move(0, -0.8, 0) # right
    else:
        print("Statment Error has been occurred.")

    sport_client.StopMove()  # Stop moving

    return 0


if __name__ == "__main__":
    mydog = dog2.Dog()
    mydog.setup()
    mydog.run(act_function)
    ans = mydog.queryGPT_by_image()
    activate_sportclient(ans)
    mydog.shutdown()

