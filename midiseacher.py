import requests
import json
from constants import web_headers


def get_search_list(keyword):
    res=requests.post("http://pz.perfectpiano.cn/search_works_v1",
        headers=web_headers,
        data={
            "p_number":1,
            "s_word":keyword,
            "type":"midiAndXml",
            "p_size":20,
        }
    )
    if res.status_code==200:
        d_list=[]
        for info in res.json()['data']:
            d_list.append({
                "image":json.loads(info['image_json']) if len(json.loads(info['image_json']))!=0 else info['image'],
                "desc":info['w_desc'],
                "author":info['name'],
                "name":info['title'],
                "midiUrl":info['audio_url'],
                "playCount":info['play_count'],
                "id":info['w_id']
            })
        return d_list
    else:
        return []
