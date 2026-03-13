<template>
    <router-view class="main-view"/>
</template>
<script>
  import {MIDIPlayer} from "@/utils/midiPlayer.js";

  export default {
    data () {
      return {
      }
    },
    created() {
      // 全局挂载MIDIPlayer
      window.midiPlayer=new MIDIPlayer()
    },

    methods:{

    }
  }
</script>
<style scoped lang="scss">

.main-view{
  height: calc(100vh - var(--Tab-Bar-Height));
  transition: all 0.3s;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
