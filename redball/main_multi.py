#!/usr/bin/env python3
import dog2_multi

# import sys
# import time
# import math
# import asyncio
# import threading

if __name__ == "__main__":
    mydog = dog2_multi.Dog()
    mydog.setup()
    mydog.run()
    # ans = mydog.queryGPT_by_image()
    # activate_sportclient(ans)
    mydog.shutdown()


# Without GPT
"""def act_function2(p1, p2, p3):
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
"""