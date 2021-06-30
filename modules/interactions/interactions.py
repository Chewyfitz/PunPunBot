import asyncio
import json
from ..varStore import Store
import websocket
import threading
import time
import random
from queue import Queue

vs = Store()

send_queue = Queue(maxsize=1)
recv_queue = Queue()

hbi = 1
seq = 0

async def start_heartbeat_thread():
    print("Starting heartbeat")
    time.sleep(0)
    print("Heartbeat wait complete")
    while True:
        heartbeat = json.dumps(
        {
            "op": 1,
            "d": seq
        })
        send_queue.put(heartbeat)
        print(f"Sent heartbeat #{seq}")
        time.sleep(hbi)


def on_message(ws, message):
    msg = json.loads(message)
    seq = msg["s"]

    print(msg)

    def _0(ws, msg):
        # Dispatch
        pass
    def _1(ws, msg):
        # Heartbeat
        pass
    def _2(ws, msg):
        # Identify
        pass
    def _3(ws, msg):
        # Presence update
        pass
    def _4(ws, msg):
        # Voice state update
        pass

    def _6(ws, msg):
        # Resume
        pass
    def _7(ws, msg):
        # Reconnect
        pass
    def _8(ws, msg):
        # Request Guild Members
        pass
    def _9(ws, msg):
        # Invalid Session
        pass
    def _10(ws, msg):
        # Setup Heartbeat
        if "d" in msg:
            if "heartbeat_interval" in msg['d']:
                hbi = msg["d"]["heartbeat_interval"]
                print(f"Set heartbeat_interval to {hbi}")

                hbt = threading.Thread(target=start_heartbeat_thread, args=(ws))
                hbt.start()
                # asyncio.ensure_future(start_heartbeat_thread(ws))

        print("Authorising...")
        # Authorise
        auth = json.dumps({
            "op": 2,
            "d": {
                "token": vs["botkey"],
                "properties": {
                    "$os": "linux",
                    "$browser": "disco",
                    "$device": "disco"
                },
                "intents": 513
            }
            })
        ws.send(auth)

    def _11(ws, msg):
        # Heartbeat Ack
        seq = msg["d"]
        print(f"seq: {seq}")
        seq += 1

    switch = {
          0:  _0
        , 1:  _1
        , 2:  _2
        , 3:  _3
        , 4:  _4
        , 6:  _6
        , 7:  _7
        , 8:  _8
        , 9:  _9
        , 10: _10
        , 11: _11
    }

    switch[msg["op"]](ws, msg)


def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    pass
    # def run(*args):
    #     for i in range(3):
    #         time.sleep(1)
    #         ws.send(json.dumps({
    #             "op": 1
    #             }))
    #     time.sleep(1)
    #     ws.close()
    #     print("thread terminating...")
    # thread.start_new_thread(run, ())

async def run_websocket():
    # websocket.enableTrace(True)
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=9&encoding=json"
        , on_open=on_open
        , on_message=on_message
        , on_error=on_error
        , on_close=on_close
        )

    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    # try:
    #     ws.run_forever()
    # except KeyboardInterrupt:
    #     pass

asyncio.ensure_future(run_websocket()) 
