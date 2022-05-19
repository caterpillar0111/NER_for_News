from ckiptagger import data_utils
from ckiptagger import WS, POS, NER
import gdown

ws = WS("./data")
pos = POS("./data")
ner = NER("./data")

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

def test_api(text):
  return "Hello"
