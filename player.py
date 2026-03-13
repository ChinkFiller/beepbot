import time

from generator import midi_file_to_buzzer_sequence,midi_ins_to_buzzer_sequence
from driver import Drvier
from processer import MIDI_Processor



def playSong(name,ch):
    deriver=Drvier()
    processor=MIDI_Processor(name)
    deriver.ready_connect()
    print(deriver.self_check())


    ins=processor.get_all_instruments()
    print("可播放乐器：")
    for i,key in enumerate(ins):
        print(f"{i} {key}")
    c1=int(input("选择1号频道乐器序号："))
    notes1=midi_ins_to_buzzer_sequence(processor.get_one_instruments(ins[int(c1)]),processor.get_tempo())


    # 开始播放
    deriver.send_notes([notes1])


