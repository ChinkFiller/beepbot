<template>
  <div class="audio-controller">
    <aside class="sidebar">
      <div class="search-box">
        <el-input v-model="searchQuery" placeholder="搜索设备..." :prefix-icon="Search" />
      </div>

      <div class="list-header">
        <el-icon @click="refreshDevices" class="refresh-btn"><Refresh /></el-icon>
      </div>

      <div class="device-list">
        <div
          v-for="item in deviceStore.deviceList"
          v-if="deviceStore.deviceList.length!==0"
          :class="['device-item', { active: item.active }]"
          @click="connectDevice(item)"
        >
          {{ item.name }} - {{item.port}}
        </div>
        <div v-else>
          <el-empty description="暂无可用设备" />
        </div>
      </div>
    </aside>

    <main class="console">
      <header class="console-header">
        <div class="status">
          <span class="dot" :class="{ connected: deviceStore.isConnected }"></span>
          {{ deviceStore.isConnected ? '已连接' : '未连接' }}
        </div>
        <el-icon class="settings-icon"><Tools /></el-icon>
      </header>

      <div class="channel-container">
        <div
          v-for="ch in deviceStore.channels"
          :key="ch.id"
          class="channel-row"
          :class="{ disabled: !ch.enabled }"
        >
          <el-checkbox v-model="ch.enabled" :label="'音轨' + ch.id" size="large" />

          <div class="channel-card" v-if="ch.enabled">
            <audio controls :src="ch.src" style="flex: 1"/>
            <div class="instrument-select">
              <span class="label">当前乐器:</span>
              <el-select v-model="ch.instrument" size="small" style="width: 100px" @change="switchInstrument(ch)">
                <el-option v-for="ins in deviceStore.currentMidi.instruments"
                           :label="'乐器'+ins.num+' '+ins.key" :value="ins.num" />
              </el-select>
            </div>
          </div>
          <div class="channel-card empty" v-else></div>
        </div>
      </div>

      <footer class="console-footer">
        <div class="midi-info">
          <p>
            当前选择MIDI文件:<span class="filename">{{ deviceStore.currentMidi.name }}</span>
            <el-link type="primary" @click="$router.push('/search')">重新选择</el-link>
          </p>
          <p>使用乐器数量:{{ deviceStore.currentMidi.instruments.length }}</p>
          <hr />
          <p v-if="deviceStore.isConnected">设备可输出频道:{{deviceStore.channelNum}}</p>
          <p v-if="deviceStore.isConnected">设备ID:{{deviceStore.id}}</p>
          <p v-if="deviceStore.isConnected">固件版本:{{deviceStore.hardVersion}}</p>
          <p v-if="deviceStore.isConnected">自检状态：<span class="pass" :style="{color:deviceStore.isPassCheck?'#67c23a':'#f56c6c'}">{{ deviceStore.isPassCheck?"已通过":"未通过" }}</span></p>
        </div>

        <div class="action-bar">
          <div class="self-check" v-if="deviceStore.isConnected">

          </div>
          <el-button v-if="deviceStore.isConnected && !isStream" type="primary" class="start-btn" size="large" @click="self_check()">设备自检</el-button>
          <el-button type="primary" class="start-btn" size="large" @click="startStream()" v-if="!isStream">开始串流</el-button>
          <el-button type="primary" class="start-btn" style="background: #f56c6c;border-color:#f56c6c" size="large" @click="stopStream()" v-else>停止串流</el-button>
        </div>
      </footer>
    </main>
  </div>
</template>

<script>
import {Search, Refresh, Setting, VideoPlay, RefreshRight, Tools,CaretRight} from '@element-plus/icons-vue'
import { useDeviceStore } from '@/store/deviceStore'
import { mapStores } from 'pinia'
import {callApi} from "@/utils/apiCaller.js";
import {base64toBlob, nsyncWaiting, showErrorDilog, showSuccessMessage} from "@/utils/commonUtils.js";

export default {
  name: 'HomeView',
  data() {
    return {
      searchQuery: '',
      isStream:false,
      // 将图标通过 data 返回，以便在 template 中使用
      Search, Refresh, Setting, VideoPlay, RefreshRight,CaretRight
    }
  },
  computed: {
    ...mapStores(useDeviceStore)
  },
  methods: {
    self_check(){
      const loading = nsyncWaiting("设备自检中...")
      callApi("self_check").then(res=>{
        useDeviceStore().setDeviceInfo(res)
      }).catch(e=>{
        useDeviceStore().setDeviceDisconnect()
        this.refreshDevices()
      }).finally(()=>{
        loading.close()
      })
    },
    switchInstrument(ch){
      const loading = nsyncWaiting("渲染MIDI中...")
      callApi("get_midi_instrument_file",useDeviceStore().currentMidi.id,ch.instrument).then(res=>{
        base64toBlob(res,"audio/wav").then(blob=>{
          ch.src=URL.createObjectURL(blob)
        })
      }).finally(()=>{
        loading.close()
      })
    },
    connectDevice(info){
      // 对已连接的设备不进行再次连接
      if (info.active){return}
      const loading = nsyncWaiting("设备连接中...")
      callApi("connect_device",{
        port:info.port
      }).then(res=>{
        useDeviceStore().setDeviceInfo(res)
        showSuccessMessage("设备连接成功")
        info.active=true
      }).finally(()=>{
        loading.close()
      })
    },
    refreshDevices() {
      callApi("get_device_list").then(res => {
        useDeviceStore().deviceList=res.map((item)=>{
            const a=useDeviceStore().deviceList.find(t=>t.name===item.name && t.port===item.port)
            if (a){
              return a
            }else {
              return {
                name: item.name,
                port: item.port,
                active: false
              }
            }
        })
        showSuccessMessage('设备列表刷新成功')
      })
    },
    startStream(){
      if (!useDeviceStore().isConnected){
        showErrorDilog('当前无可用设备,请链接设备后重试')
        return
      }

      if (useDeviceStore().currentMidi.id==='' || useDeviceStore().channels[0].instrument===''){
        showErrorDilog("至少需要一个音轨有数据")
        return;
      }
      useDeviceStore().channels.forEach(item=>{
        callApi('start_stream',useDeviceStore().currentMidi.id,item.instrument,item.id).then(res=>{
          showSuccessMessage(`频道${item.id}开始串流`)
          this.isStream=true
        })
      })
    },
    stopStream(){
      callApi("stop_stream").then(res=>{
        showSuccessMessage('停止串流成功')
        this.isStream=false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.audio-controller {
  display: flex;
  height: 100vh;
  background-color: #fff;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;

  // 侧边栏样式
  .sidebar {
    width: 200px;
    border-right: 1px solid #dcdfe6;
    padding: 15px;
    display: flex;
    flex-direction: column;

    .list-header {
      display: flex;
      justify-content: flex-end;
      margin: 10px 0;
      .refresh-btn { cursor: pointer; font-size: 18px; }
    }

    .device-list {
      .device-item {
        background-color: #e4e7ed;
        padding: 10px;
        margin-bottom: 8px;
        border-radius: 8px;
        font-size: 14px;
        color: #606266;
        text-align: center;
        cursor: pointer;

        &.active {
          background-color: #b1b3b8;
          color: #303133;
        }
      }
    }
  }

  // 右侧控制台样式
  .console {
    flex: 1;
    padding: 20px;
    display: flex;
    flex-direction: column;

    .console-header {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 15px;
      margin-bottom: 20px;

      .status {
        display: flex;
        align-items: center;
        font-size: 14px;
        .dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #f56c6c;
          margin-right: 5px;
          &.connected { background: #67c23a; }
        }
      }
      .settings-icon { font-size: 20px; cursor: pointer; }
    }

    .channel-container {
      flex: 1;
      .channel-row {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 15px;

        .channel-card {
          flex: 1;
          border: 1px solid #dcdfe6;
          padding: 10px 15px;
          display: flex;
          align-items: center;
          gap: 15px;
          min-height: 50px;

          &.empty {
            background-color: #c0c4cc;
            border: none;
          }

          .progress-bar { flex: 1; }
          .time-display { font-size: 13px; min-width: 40px; }

          .instrument-select {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 13px;
            .sync-icon { color: #409eff; cursor: pointer; }
          }
        }
      }
    }

    .console-footer {
      border-top: 1px solid #ebeef5;
      padding-top: 20px;

      .midi-info {
        font-size: 14px;
        line-height: 1.8;
        .filename { font-weight: bold; margin-right: 10px; }
        hr { border: none; border-top: 1px solid #ebeef5; margin: 10px 0; }
      }

      .action-bar {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 20px;
        margin-top: 10px;

        .self-check {
          font-size: 14px;
          .pass { font-weight: bold; }
        }

        .start-btn {
          background-color: #1a9edc;
          border-color: #1a9edc;
          padding-left: 40px;
          padding-right: 40px;
        }
      }
    }
  }
}
</style>