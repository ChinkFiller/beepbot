import * as Tone from "tone"
import { Midi } from "@tonejs/midi"

export class MIDIPlayer {

    constructor() {
        this.midi = null
        this.synth = null
        this.part = null
        this.onPlayingList = {}
        this.duration = 0
        this.isPalying=false
    }

   async load(url) {
        // 清空旧状态
        Tone.Transport.stop()
        Tone.Transport.cancel()
        Tone.Transport.seconds = 0

        const response = await fetch(url)
        const arrayBuffer = await response.arrayBuffer()
        this.midi = new Midi(arrayBuffer)

        //this.synth = new Tone.PolySynth(Tone.Synth).toDestination()
       this.synth = new Tone.Sampler({
            urls: {
                'A0': "A0.mp3",
                'C1': "C1.mp3",
                'D#1': "Ds1.mp3",
                'F#1': "Fs1.mp3",
                'A1': "A1.mp3",
                'C2': "C2.mp3",
                'D#2': "Ds2.mp3",
                'F#2': "Fs2.mp3",
                'A2': "A2.mp3",
                'C3': "C3.mp3",
                'D#3': "Ds3.mp3",
                'F#3': "Fs3.mp3",
                'A3': "A3.mp3",
                'C4': "C4.mp3",
                'D#4': "Ds4.mp3",
                'F#4': "Fs4.mp3",
                'A4': "A4.mp3",
                'C5': "C5.mp3",
                'D#5': "Ds5.mp3",
                'F#5': "Fs5.mp3",
                'A5': "A5.mp3",
                'C6': "C6.mp3",
                'D#6': "Ds6.mp3",
                'F#6': "Fs6.mp3",
                'A6': "A6.mp3",
                'C7': "C7.mp3",
                'D#7': "Ds7.mp3",
                'F#7': "Fs7.mp3",
                'A7': "A7.mp3",
                'C8': "C8.mp3"
            },
            release: 1,
            baseUrl: "/piano/"
        }).toDestination()

        const events = []

        this.midi.tracks.forEach(track => {
            track.notes.forEach(note => {
                events.push({
                    time: note.time,
                    name: note.name,
                    duration: note.duration,
                    velocity: note.velocity
                })
            })
        })

        this.duration = this.midi.duration

        this.part = new Tone.Part((time, value) => {
            this.synth.triggerAttackRelease(
                value.name,
                value.duration,
                time,
                value.velocity
            )
        }, events)

        this.part.start(0)
    }



    async play() {
        await Tone.start()
        this.isPalying=true
        Tone.Transport.start()
        this._startTimeUpdate()
    }

    pause() {
        this.isPalying=false
        Tone.Transport.pause()
    }

    stop() {
        Tone.Transport.stop()
        Tone.Transport.seconds = 0
    }

    seek(seconds) {
        Tone.Transport.seconds = seconds
    }

    getCurrentTime() {
        return Tone.Transport.seconds
    }

    getDuration() {
        return this.duration
    }

    _startTimeUpdate() {
        if (this._timer) clearInterval(this._timer)

        this._timer = setInterval(() => {
            const currentTime = this.getCurrentTime()
            for (let id in this.onPlayingList) {
                this.onPlayingList[id](currentTime)
            }
        }, 100)
    }

    addOnPlayingEvent(id, fn) {
        this.onPlayingList[id] = fn
    }

    removeOnPlayingEvent(id) {
        delete this.onPlayingList[id]
    }
}
