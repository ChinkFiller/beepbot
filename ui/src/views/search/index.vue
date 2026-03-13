<template>
  <div class="search-page">
    <header class="search-header">
      <el-icon class="back-icon" @click="handleBack()"><ArrowLeft /></el-icon>
      <div class="search-input-wrapper">
        <el-input
          v-model="searchText"
          placeholder="请输入搜索内容"
          :prefix-icon="Search"
          clearable
          @keyup.enter.native="handleSearch"
        />
        <el-button type="primary" class="search-btn" @click="handleSearch">搜索</el-button>
      </div>
    </header>

    <div class="result-container">
      <el-scrollbar>
        <div class="song-list" v-if="searchList.length!==0">
          <div v-for="song in searchList" :key="song.id" class="song-item" :style="{background: `linear-gradient(to right, #00ff8f ${song.now}%, rgba(0,0,0,0) ${song.now}%)`}">
            <div class="left-info">
              <el-icon class="play-icon">
                <i v-if="!song.isPlaying" class="iconfont icon-bofangqi-bofang" style="font-size: 24px" @click="handlePlayMidi(song)"></i>
                <i v-else="song.isPlaying" class="iconfont icon-bofangqi-zanting" style="font-size: 24px" @click="handlePauseMidi(song)"></i>
              </el-icon>
              <div style="width: 45px;height: 45px">
                <el-image :src="song.image" class="cover" fit="cover" />
              </div>
              <div class="meta">
                <div class="title">{{ song.name }}</div>
                <div class="artist">{{ song.author }}</div>
              </div>
            </div>

            <div class="middle-info">
              <span class="desc">{{ song.desc }}</span>
            </div>

            <div class="right-action">
              <el-button type="primary" size="small" @click="handleSelect(song)">
                选择
              </el-button>
            </div>
          </div>
        </div>
        <div v-else>
          <el-empty description="暂无结果" />
        </div>
      </el-scrollbar>
    </div>
  </div>
</template>

<script>
import { Search, ArrowLeft, VideoPlay } from '@element-plus/icons-vue'
import { useDeviceStore } from '@/store/deviceStore'
import { mapStores } from 'pinia'
import {callApi} from "@/utils/apiCaller.js";

export default {
  name: 'SearchView',
  data() {
    return {
      searchText: '',
      searchList: [],
      nowPlayingSong:{},
      Search, ArrowLeft, VideoPlay
    }
  },
  computed: {
    ...mapStores(useDeviceStore)
  },
  created() {
    window.midiPlayer.stop()
    window.midiPlayer.addOnPlayingEvent("seacher",(e)=>{
      this.nowPlayingSong.now=((parseInt(e)/window.midiPlayer.getDuration())*100).toFixed(2)
    })
  },
  unmounted() {
    window.midiPlayer.stop()
    window.midiPlayer.removeOnPlayingEvent("seacher")
  },
  methods: {
    handleBack(){
      this.$router.back()
    },
    handleSelect(song) {
      useDeviceStore().resetChannels()
      callApi('process_song',song).then(res=>{
        useDeviceStore().setSelectedMidi(res)
        // 2. 跳转回主页
        this.$router.push('/');
      })

    },
    handleSearch() {
      window.midiPlayer.stop()
      callApi("get_midi_search_data",this.searchText).then(res=>{
        this.searchList=res
        this.searchList.forEach(item=>{
          item.isPlaying=false
          item.now
        })
      })
    },
    handlePlayMidi(song){
      const player=window.midiPlayer
      if (song.id!==this.nowPlayingSong.id){
        player.stop()
        player.load(song.midiUrl)
        player.play()
        this.nowPlayingSong=song
        this.searchList.forEach(item=>{
            item.isPlaying = item.id === song.id;
            item.now=0
        })
      }else{
        player.play()
        this.nowPlayingSong.isPlaying=true
      }
    },
    handlePauseMidi(song){
      const player=window.midiPlayer
      player.pause()
      this.nowPlayingSong.isPlaying=false
    }

  }
}
</script>

<style lang="scss" scoped>
.search-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 20px;
  box-sizing: border-box;

  .search-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;

    .back-icon {
      font-size: 24px;
      cursor: pointer;
      font-weight: bold;
    }

    .search-input-wrapper {
      flex: 1;
      display: flex;
      gap: 10px;

      :deep(.el-input__wrapper) {
        border-radius: 4px;
      }

      .search-btn {
        background-color: #1a9edc;
        border-color: #1a9edc;
        padding: 0 30px;
      }
    }
  }

  .result-container {
    flex: 1;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    overflow: hidden;

    .song-list {
      padding: 10px;

      .song-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 15px;
        border: 1px solid #ebeef5;
        border-radius: 8px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
        height: 50px;

        &:hover {
          background-color: #f5f7fa;
        }

        .left-info {
          display: flex;
          align-items: center;
          gap: 12px;
          flex: 2;

          .play-icon { font-size: 24px; cursor: pointer;width: 10px }
          .cover { width: 45px; height: 45px; border-radius: 4px; }
          .meta {
            .title { font-size: 14px;
              color: #303133;
              display: -webkit-box;
              -webkit-box-orient: vertical;
              -webkit-line-clamp: 2; // 这里数字是几，就显示几行
              overflow: hidden;
              text-overflow: ellipsis; }
            .artist { font-size: 12px; color: #909399; margin-top: 4px; }
          }
        }

        .middle-info {
          flex: 3;
          display: flex;
          justify-content: space-around;
          align-items: center;
          font-size: 13px;
          color: #909399;
          min-width: 0; // ⚡关键：允许 flex 容器缩小，不被内容撑开

          .desc {
            color: #b1b3b8;
            // --- 核心省略样式 ---
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 3; // 这里数字是几，就显示几行
            overflow: hidden;
            text-overflow: ellipsis;
            // --------------------
            flex: 1;                  // 让描述部分占据中间的剩余空间
            margin: 0 15px;           // 给左右留点间距，防止挤在一起
            min-width: 0;             // ⚡关键：防止文字撑开 flex 子项
          }

          .plays {
            flex-shrink: 0;           // 保证播放量文字不被挤压
          }
        }

        .right-action {
          flex: 1;
          display: flex;
          justify-content: flex-end;

          .el-button--primary {
            background-color: #1a9edc;
            border-color: #1a9edc;
          }
        }
      }
    }
  }
}
</style>