from ckiptagger import WS, POS, NER
import requests
import json

ws = WS("./data")
pos = POS("./data")
ner = NER("./data")
city_dict={'基隆','嘉義','臺北','新北','臺南','桃園'	,'高雄','新竹','屏東','臺東','苗栗','花蓮','臺中',
           '宜蘭','彰化','澎湖','南投','金門','雲林','連江','台南','台北','台東','台中'}

def get_ner_result(text,ws,pos,ner):
  ws_results = ws([text])
  pos_results = pos(ws_results)
  ner_results = ner(ws_results, pos_results)

  return ws_results,pos_results,ner_results

def get_ner_tag(text,tag):
  tag_list=[]
  ws_results,pos_results,ner_results=get_ner_result(text,ws,pos,ner)
  for tuple_result in list(ner_results[0]):
    if tuple_result[2]==tag:
      tag_list.append(tuple_result[-1])
  return tag_list

def get_pos(text,pos_tag):
  adj_list=[]
  ws_results,pos_results,ner_results=get_ner_result(text,ws,pos,ner)
  for i in range(len(ws_results[0])):
    if pos_results[0][i]==pos_tag:
      adj_list.append(ws_results[0][i])
  return adj_list

def get_location_city_by_geocode_api(place,api_key,city_dict):
  #function功能，input一個地點與帶入google map api key，回傳縣市資訊
  #申請google API key : https://developers.google.com/maps/documentation/geocoding/get-api-key
  url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+place+'&language=zh-TW'+'&key='+api_key
  reponse=requests.post(url)
  data=reponse.json()
  #data會是一個json格式，可以參考下面這篇查看格式
  #https://icelandcheng.medium.com/%E4%BD%BF%E7%94%A8google-map-api-geocoding-api-%E5%BE%97%E5%88%B0%E9%BB%9E%E4%BD%8D%E7%B8%A3%E5%B8%82%E9%84%89%E9%8E%AE%E8%B3%87%E6%96%99-25bf5f0e4a21
  if len(data['results'])==0: return "Not Found BY API"
  location_information=data['results'][0]['formatted_address']
  #只需要部分地址相關資料，此處的location_information會是正式的地址格式
  for location in city_dict:
    if location in location_information:
      #如果發現地址裡有縣市資訊
      return location
    else:
      return "Not Found BY API"

def get_city_in_news(news,city_dict):
  #function功能，input一個新聞文本，找尋文本中出現的縣市資訊，如果同一個縣市出現超過三次，就回傳，否則回傳出現最多次的
  
  city_dict_tmp=dict(zip(city_dict,[0 for i in range(len(city_dict))]))
  for city in city_dict_tmp:
    if city in news:
      city_dict_tmp[city]+=1
      if city_dict_tmp[city]>=3:
        return city

  if all(value==0 for value in city_dict_tmp.values()):
    return None
  else:
    return max(city_dict_tmp, key=city_dict_tmp.get)

def get_major_city_for_news(text,city_dict,api_key):
  if get_city_in_news(text,city_dict)!=None:
    #找到縣市
    return get_city_in_news(text,city_dict)
  else:
    #NER
    location_list=get_ner_tag(text,'LOC')
    if len(location_list)!=0 and location_list!=None:
      location_list.sort(key=lambda s:len(s),reverse=True)
        #打API get_location_city_by_geocode_api(location,api_key)
        #sort從最長的開始打
      for place in location_list:
        place_result=get_location_city_by_geocode_api(place,api_key,city_dict)
        if  place_result!='Not Found BY API':
          return  place_result
    else:
      return "Not Found Location Information"
      #另外可以存一份表把打過的存起來