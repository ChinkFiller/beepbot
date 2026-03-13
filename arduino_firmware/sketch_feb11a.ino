#define VERSION "V1.2"
#define CHANNELNUM 1

#include "avr/boot.h"
#include <ArduinoUniqueID.h>

static char buf1[50];
static char buf2[30];

int pins[1]={5};

// 发生频率的数组指令，
char* channelData[2];



void print(String msg){
  Serial.println(msg);
}

// 获取可用字符串
String getInputString(){
  if (Serial.available()) {
    String inputString = "";
    while (Serial.available()) {
      char c = Serial.read();
      inputString += c;
      delay(1);
    }
    return inputString;
  }
  return "";
}

String getArduinoUniqueId(){
  /*获得arduino板子硬件唯一ID*/  
  String uniqid = "";
  for (size_t i = 0; i < UniqueIDsize; i++)
  {
    if( i > 0 and i < UniqueIDsize){
      uniqid = uniqid+"-";
    }
    if (UniqueID[i] < 0x10){
      uniqid = uniqid + "0";
    }
    uniqid = uniqid + String(UniqueID[i], HEX);
  }
  return uniqid;
}

void parseCode(char* codeData[],String data,const char* key, char* buffer, int bufSize){
    data.toCharArray(buffer, bufSize);
    int i = 0;
    char *token = strtok(buffer, key);
    while (token != NULL) {
      codeData[i++] = token;
      token = strtok(NULL, key);
    }
}

void beep(int channel,int f,int d){
  tone(pins[channel], f);
  delay(d);
  noTone(pins[channel]);
}

void startAsyncBeep(int channel,int f){
  tone(pins[channel], f);
}

void stopAsyncBeep(int channel){
  noTone(pins[channel]);
}

// 初始化状态
void setup(){

  // 初始化所有频道
  for (int i=0; i<CHANNELNUM; i++) {
    pinMode(pins[i],OUTPUT);
  }
  
  Serial.begin(9600);
}

// 主循环
void loop(){
  String stringData = getInputString();
  // 设置播放指令集bp表示指令
  // 以#进行分割不同频道，以,分割频率和持续时间
  if (stringData.startsWith("bp")){
    // 去除前置指令后的传数据指令
    stringData=stringData.substring(2);
    
    // 分割数据
    parseCode(channelData,stringData,"#",buf1, 50);

    if (atoi(channelData[1])==-1){
      // 执行关闭频率指令
      stopAsyncBeep(atoi(channelData[0]));
    }else{
      // 执行发出指令
      startAsyncBeep(atoi(channelData[0]),atoi(channelData[1]));
    }
  }

  // 自检指令
  if (stringData.startsWith("sc")){
    //  对每个音轨进行试音
    for(int i=0;i<CHANNELNUM;i++){
      beep(i, 262, 250);
      beep(i, 330, 250);
      beep(i, 523, 250);

      delay(200);
    }

    // 生成自检信息
    String msg = String(CHANNELNUM)+" "+getArduinoUniqueId()+" "+VERSION+" "+"OK";

    // 返回自检信息
    print(msg);
  }

  if (stringData.startsWith("bi")){
    // 返回自检信息
    print(String(CHANNELNUM)+" "+getArduinoUniqueId()+" "+VERSION);
  }
}
