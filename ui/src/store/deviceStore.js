// stores/deviceStore.js
import { defineStore } from 'pinia'

export const useDeviceStore = defineStore('device', {
  state: () => ({
    id:"", // 设备ID
    hardVersion:"", // 硬件版本
    isConnected: false, // 是否已连接
    isPassCheck:false,
    channelNum:1,
    channels: [
      { id: 0, enabled: true, time: 0, instrument: '', progress: 0, src:'' }
    ],
    currentMidi: {
      name: "Null",
      id: "",
      duration: 0,
      progress:0,
      instruments: []
    },
    deviceList:[]
  }),
  actions: {
    // 可以在这里添加切换设备或更新通道的方法
    setSelectedMidi(song) {
      this.currentMidi.id=song.id;
      this.currentMidi.name=song.name;
      this.currentMidi.duration=song.duration;
      this.currentMidi.instruments=song.instruments;
    },
    resetChannels() {
      this.channels=[]
      for (let i = 0; i < this.channelNum; i++) {
        this.channels.push({ id: i, enabled: true, time: 0, instrument: '', progress: 0, src:'' })
      }
    },
    setDeviceInfo(info){
      this.id=info.deviceID
      this.channelNum=info.channelNum
      this.hardVersion=info.hardVersion
      this.isConnected=true
      this.isPassCheck=info.checkState
      this.resetChannels()
    },
    setDeviceDisconnect(){
      this.isConnected=false
      this.channelNum=1
      this.hardVersion=''
      this.isPassCheck=false
      this.resetChannels()
    }
  }
})