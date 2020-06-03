import paddlehub as hub
import numpy as np
import logging
import time
import time
import threading
import requests
import json
from backsite.settings import PREDICTION_CHECK_TIME,PREDICTION_CLOSE_TIME
from datetime import datetime
moods = {0: '喜悦', 1: '愤怒', 2: '厌恶', 3: '低落'}

def getTimeStr():
    return str(datetime.fromtimestamp(time.time()))
class Module:
    def __init__(self, name, port):
        self.name = name
        self.active = False
        self.port = port
        self.env_name = "webserver"
        self.last_predict_time = time.time()
        self.proc = None

    def activate(self):
        if self.active == True:
            return
        print("[{}] Module<{}>: 正在开启...".format(getTimeStr(),
                    self.name))
        self.proc = Popen("hub serving start -m {} -p {}".format(self.name,
                                                                 self.port), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.active = True
        print("[{}] Module<{}>: 开启成功".format(getTimeStr(),
                    self.name))

    def deactivate(self):
        if self.active == False:
            print("[{}] Module<{}>: 已关闭".format(getTimeStr(),
                    self.name))
            return
        print("[{}] Module<{}>: 正在关闭...".format(getTimeStr(),
                    self.name))
        # proc = Popen("hub serving stop -p {}".format(self.port),shell=True,stdin=PIPE, stdout=PIPE, stderr=PIPE)
        if self.proc != None:
            self.proc.kill()
            self.proc = None
        self.active = False
        print("[{}] Module<{}>: 关闭成功".format(getTimeStr(),
                    self.name))

    def predict(self, datas):
        self.last_predict_time = time.time()
        if not(self.active):
            self.activate()
        url = "http://127.0.0.1:{}/predict/{}".format(self.port, self.name)
        inputs = [[data] for data in datas]

        def req(inputs):
            headers = {"Content-Type": "application/json"}
            try:
                res = requests.post(url=url, headers=headers,
                                    data=json.dumps({'data': inputs}))
            except requests.exceptions.ConnectionError:
                print("[{}] Module<{}>: Error<{}>".format(getTimeStr(),
                    self.name, "ConnectionError"))
                return False
            return res.json()
        res = req(inputs)
        if res == False:
            return False,None
        predictions = res['results']
        for index, text in enumerate(inputs):
            print("%s\tpredict=%s" % (inputs[index], predictions[index]))
        return True,predictions[0]


class check_active_worker(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q

    def run(self):
        close_time = PREDICTION_CLOSE_TIME
        check_time = PREDICTION_CHECK_TIME
        while True:
            time.sleep(check_time)
            module = self.q.get(block=True)
            if module.active == True:
                if time.time() - module.last_predict_time > close_time:
                    print("[{}] Thread<check_active_worker>: 检查到PREDICTION服务可以关闭".format(getTimeStr()))
                    module.deactivate()
                else:
                    print("[{}] Thread<check_active_worker>: PREDICTION服务将在{:.2f}秒后关闭".format(getTimeStr(),
                        module.last_predict_time+close_time-time.time()))
            self.q.put(module, block=True)
