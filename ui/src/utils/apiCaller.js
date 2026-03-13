import {ElMessage} from "element-plus";

export function callApi(method, ...params) {
  return new Promise((resolve, reject) => {
    try {
      return window.pywebview.api[method](...params).then((res) => {
        resolve(res)
      }).catch(e=>{
        ElMessage(
          { message: e.message, type: 'error' }
        )
        reject(e)
      })
    }catch (e){
      ElMessage(
        { message: e.message, type: 'error' }
      )
    }
  })

}