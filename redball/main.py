#!/usr/bin/env python3
import dog2


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


if __name__ == "__main__":
    mydog = dog2.Dog()
    mydog.setup()
    mydog.run(act_function)
    mydog.shutdown()
