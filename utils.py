from pathlib import Path
import requests
import uuid
from constants import *
import threading
import time


class StoppableThread(threading.Thread):
    def __init__(self, target, *args, **kwargs):
        super().__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.stop_event = threading.Event()

    def run(self):
        self.target(*self.args, stop_event=self.stop_event)

    def stop(self):
        self.stop_event.set()


def write_data_to_local(data, path, cover=True):
    file_path = Path(path)

    file_path.parent.mkdir(parents=True, exist_ok=True)

    # 3. 写入文件
    mode = 'wb' if cover else 'ab'
    with open(file_path, mode) as f:
        f.write(data)
def download_file_to_local(url,name=str(uuid.uuid4()).replace('-','')):
    res=requests.get(url,headers=web_headers)
    path=f"./midi/{name}"
    write_data_to_local(res.content,path)
    return path


