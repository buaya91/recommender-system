# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 14:15:08 2014

@author: qingwei
"""

import websocket


if __name__ == "__main__":
    # websocket.enableTrace(True)
    name = input("Enter the name of customer\n")
    print("send name")
    ws = websocket.create_connection("ws://127.0.0.1:8888")    
    ws.send(name)
    result = ws.recv()
    print("Recommendations: {}\n".format(result))
    ws.close()