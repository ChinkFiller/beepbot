import pretty_midi
import math
from collections import defaultdict


def midi_to_freq(note):
    return int(round(440 * (2 ** ((note - 69) / 12))))


def midi_file_to_buzzer_sequence(filename, subdivision=16):
    pm = pretty_midi.PrettyMIDI(filename)

    tempo_times, tempi = pm.get_tempo_changes()

    events = defaultdict(list)

    for instrument in pm.instruments:
        if instrument.is_drum:
            continue
        for note in instrument.notes:
            events[note.start].append(("on", note.pitch))
            events[note.end].append(("off", note.pitch))

    timeline = sorted(events.keys())

    active_notes = set()
    result = []

    last_time = 0.0
    last_freq = 0

    tempo_index = 0
    current_tempo = tempi[0]

    for time in timeline:

        # 检查是否进入新的 tempo 区间
        while (tempo_index + 1 < len(tempo_times) and
               time >= tempo_times[tempo_index + 1]):
            tempo_index += 1
            current_tempo = tempi[tempo_index]

        duration = time - last_time

        if duration > 0:
            quarter_duration = 60.0 / current_tempo
            unit_duration = quarter_duration / (subdivision / 4)

            units = round(duration / unit_duration)
            duration_ms = int(units * unit_duration * 1000)

            if duration_ms > 0:
                result.append((last_freq, duration_ms))

        # 更新音符状态
        for event_type, pitch in events[time]:
            if event_type == "on":
                active_notes.add(pitch)
            else:
                active_notes.discard(pitch)

        if active_notes:
            highest = max(active_notes)
            current_freq = midi_to_freq(highest)
        else:
            current_freq = 0

        last_freq = current_freq
        last_time = time

    # 合并连续相同频率
    merged = []
    for freq, dur in result:
        if dur <= 0:
            continue
        if merged and merged[-1][0] == freq:
            merged[-1] = (freq, merged[-1][1] + dur)
        else:
            merged.append((freq, dur))

    return merged

def midi_ins_to_buzzer_sequence(ins, tem,subdivision=16):
    tempo_times=tem[0]
    tempi=tem[1]

    events = defaultdict(list)

    if not ins.is_drum:
        for note in ins.notes:
            events[note.start].append(("on", note.pitch))
            events[note.end].append(("off", note.pitch))


    timeline = sorted(events.keys())

    active_notes = set()
    result = []

    last_time = 0.0
    last_freq = 0

    tempo_index = 0
    current_tempo = tempi[0]

    for time in timeline:

        # 检查是否进入新的 tempo 区间
        while (tempo_index + 1 < len(tempo_times) and
               time >= tempo_times[tempo_index + 1]):
            tempo_index += 1
            current_tempo = tempi[tempo_index]

        duration = time - last_time

        if duration > 0:
            quarter_duration = 60.0 / current_tempo
            unit_duration = quarter_duration / (subdivision / 4)

            units = round(duration / unit_duration)
            duration_ms = int(units * unit_duration * 1000)

            if duration_ms > 0:
                result.append((last_freq, duration_ms))

        # 更新音符状态
        for event_type, pitch in events[time]:
            if event_type == "on":
                active_notes.add(pitch)
            else:
                active_notes.discard(pitch)

        if active_notes:
            highest = max(active_notes)
            current_freq = midi_to_freq(highest)
        else:
            current_freq = 0

        last_freq = current_freq
        last_time = time

    # 合并连续相同频率
    merged = []
    for freq, dur in result:
        if dur <= 0:
            continue
        if merged and merged[-1][0] == freq:
            merged[-1] = (freq, merged[-1][1] + dur)
        else:
            merged.append((freq, dur))

    return merged