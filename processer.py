import io
import pretty_midi
import numpy as np
from scipy.io import wavfile

class MIDI_Processor:
    def __init__(self, midi_file):
        self.midi_data = pretty_midi.PrettyMIDI(midi_file)

    def get_tempo(self):
        return self.midi_data.get_tempo_changes()

    def get_duration(self):
        return self.midi_data.get_end_time()


    '''
    返回所有使用的乐器文字数组
    '''
    def get_all_instruments(self):
        return [ins.name for ins in self.midi_data.instruments]

    '''
    返回这个乐器的所有数据
    '''
    def get_one_instruments(self, instrument_name):
        for instrument in self.midi_data.instruments:
            if instrument.name == instrument_name:
                return instrument
        return None

    '''
    返回内存mid文件对象
    '''
    def get_one_instruments_mid_file(self,instrument_name):
        new_midi = pretty_midi.PrettyMIDI()
        for instrument in self.midi_data.instruments:
            if instrument.name == instrument_name:
                new_midi.instruments = [instrument]
                byte_data=io.BytesIO()
                new_midi.write(byte_data)
                byte_data.seek(0)
                return byte_data


    '''
        返回内存wav文件对象
    '''
    def get_one_instruments_wav_file(self, instrument_name):
        new_midi = pretty_midi.PrettyMIDI()
        for instrument in self.midi_data.instruments:
            if instrument.name == instrument_name:
                new_midi.instruments = [instrument]
                # 渲染音频 (默认44100采样率)
                audio = new_midi.synthesize()

                wav_buffer = io.BytesIO()
                wavfile.write(wav_buffer, 44100, (audio * 32767).astype(np.int16))
                wav_buffer.seek(0)

                return wav_buffer