import {ElLoading, ElMessage, ElMessageBox} from "element-plus";

export function base64toBlob(base64, contentType) {
  return fetch(base64)
    .then(response => response.blob())
}


export function nsyncWaiting(content){
  return ElLoading.service({
        lock: true,
        text: content,
        background: 'rgba(0, 0, 0, 0.7)',
      })
}

export function showErrorDilog(content){
    ElMessageBox({
          title: '错误',
          message: content,
          type:"error",
          closeOnClickModal:false
    })
}

export function showSuccessMessage(content){
    ElMessage({
      message:content,
      type: 'success'
    })
}