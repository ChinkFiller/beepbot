import time
from itertools import cycle
from threading import Lock
from utils import StoppableThread

import serial

import serial.tools.list_ports

class Drvier:
    # 初始化串口数据
    def __init__(self,port="COM5",rate=9600,timeout=1):
        self.lock = Lock()
        self.ser=serial.Serial()
        self.ser.port = port
        self.ser.baudrate = rate
        self.ser.timeout = timeout
        self.ser.bytesize = 8  # 设置数据位
        self.ser.stopbits = 1  # 设置停止位
        self.ser.parity = "N"  # 设置校验位
        self.channel_num=0
        self.device_id=""
        self.device_version=""
        self.state=False,
        self.t_list=[]


    def ready_connect(self):
        self.ser.open()
        time.sleep(2.5)
        if(self.ser.isOpen()):
            return True
        else:
            return False

    def check_connect(self):
        return self.ser.isOpen()

    def self_check(self):
        if self.check_connect():
            self.ser.write('sc'.encode('gbk'))
            info = self.recv_data().split()

            self.channel_num = int(info[0])
            self.device_id = info[1]
            self.device_version = info[2]
            self.state = info[3] == "OK"
            return True
        else:
            raise RuntimeError("设备已断开")

    def connect_device(self):
        try:
            self.ready_connect()
            # 发送硬件自检信息
            self.self_check()
            return True
        except:
            return False


    def play_midi_t(self,channel, step, notes,stop_event):
        for _ in range(step):
            note = next(notes)
            if stop_event.is_set():
                break
            with self.lock:
                self.send_note((channel, note[0], note[1]))

        # 线程播放完毕停止该频道
        self.end_note([channel])


    def send_note(self,note):
        '''
           发送一个音符数据给设备，需要手动调用end_note()函数来清空频率状态
           参数：note:一个包含三个元素的列表，分别是使用频道，音符频率，音符时长
        '''
        self.ser.write(f"bp{note[0]}#{note[1]}".encode('gbk'))
        time.sleep(note[2]/1000)



    def send_notes(self, data={}):
        '''
            发送一组音符数据给设备，需要手动调用end_note()函数来清空频率状态
        '''
        if not self.ser.isOpen():
            raise RuntimeError("设备已离线")

        max_len = 0
        note_c = {}
        for ch in data.keys():
            note = data[ch]
            max_len = max(max_len, len(note))
            note_c[ch]=cycle(note)

        for i in data.keys():
            t=StoppableThread(self.play_midi_t,int(i), max_len, note_c[i])
            # 开启独立的线程
            self.t_list.append(t)
            t.start()


    def stop_send_notes(self):
        """
        停止所有发送音符的线程
        """
        for t in self.t_list:  # 遍历线程列表
            t.stop()
            t.join()  # 等待线程结束


    def recv_data(self,timeout=4):
        '''
           获取串口数据
        '''
        f=time.time()+timeout
        while time.time()<f:
            status = self.ser.readline()
            if status != b'':
                return status.decode('gbk')
    def send_data(self,data):
        self.ser.write(data.encode('gbk'))


    def end_note(self,c):
        '''
        清空指定频道的的播放状态
        '''
        #发送停止信号
        for i in c:
            self.ser.write(f"bp{i}#-1".encode('gbk'))

    def close_connect(self):
        if (self.ser.isOpen()):
            self.ser.close()
            return True
        else:
            return True


def search_device():
    d_list=[]
    for i in list(serial.tools.list_ports.comports()):
        d_list.append({
            "port":i.name,
            "name":i.description
        })
    return d_list
