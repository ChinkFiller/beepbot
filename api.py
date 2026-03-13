import base64

from midiseacher import get_search_list
from driver import search_device
from utils import download_file_to_local
from processer import MIDI_Processor
from driver import Drvier
from generator import midi_ins_to_buzzer_sequence


class WebApi:
    nowDevice=None

    def get_midi_search_data(self,keyword):
        return get_search_list(keyword)

    def get_device_list(self):
        return search_device()

    def process_song(self,song):
        path=download_file_to_local(song['midiUrl'],str(song['id'])+'.mid')
        p=MIDI_Processor(path)
        return {
            "id":song['id'],
            "name":song['name'],
            "instruments":[{"num":i,"key":key} for i,key in enumerate(p.get_all_instruments()) ],
            "duration":p.get_duration(),
        }

    def get_midi_instrument_file(self,song_id,instrument_num):
        p=MIDI_Processor(f"./midi/{song_id}.mid")
        data=p.get_one_instruments_wav_file(p.get_all_instruments()[instrument_num])

        midi_bytes = data.read()

        # 转 base64
        return "data:audio/wav;base64,"+base64.b64encode(midi_bytes).decode('utf-8')


    def connect_device(self,device):
        d=Drvier(device['port'],9600,1)
        # 链接设备
        if d.connect_device():
            self.nowDevice=d
            return {
                "deviceID":d.device_id,
                "channelNum":d.channel_num,
                "hardVersion":d.device_version,
                "checkState":d.state
            }
        else:
            raise RuntimeError("无法连接该设备")

    def self_check(self):
        if self.nowDevice.self_check():
            return {
                "deviceID": self.nowDevice.device_id,
                "channelNum": self.nowDevice.channel_num,
                "hardVersion": self.nowDevice.device_version,
                "checkState":self.nowDevice.state
            }

    def start_stream(self,id,ins_num,channel):
        processor = MIDI_Processor('./midi/'+str(id)+'.mid')
        notes = midi_ins_to_buzzer_sequence(processor.get_one_instruments(processor.get_all_instruments()[int(ins_num)]), processor.get_tempo())
        self.nowDevice.send_notes({
            channel:notes
        })
        return True

    def stop_stream(self):
        self.nowDevice.stop_send_notes()
