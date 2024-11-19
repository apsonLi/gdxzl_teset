
from flask import Flask, request ,render_template,Blueprint
import  os
import socket
import base64
import json

import time
#md5
import hashlib

from  gdxzl_config import battlewaymap,stuff,hero_level_up,nucleus,nucleus_test

app = Flask(__name__)


from flask import Response

def convert_to_string(data):
    if isinstance(data, dict):
        return {str(k): convert_to_string(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_string(v) for v in data]
    else:
        return str(data)




@app.route('/gdxzl/data_get', methods=['POST'])
def gdxzldata_get():
    params = request.get_data()
    result = params.decode('utf-8')
    resultdic = convert_to_dict(result)
    data = resultdic['DataSec']
    errorresult = {"Time": str(int(time.time()) * 1000)}
    error_str = 'abc' + json.dumps(errorresult)
    error_bytees = error_str.encode('utf-8')
    if resultdic['DataName'] == 'EnterConfig':
        nucleus_deal = {}
        for k,v in nucleus.items():
            # print(k)
            nucleus_deal[k] = json.dumps(v)
        hero_level_up_deal = {}
        for k, v in hero_level_up.items():
            hero_level_up_deal[k] = json.dumps(v)
        resultclient = {
            "Data_CNucleus":json.dumps(nucleus_deal),
                        "Data_CHeroLevelUp":json.dumps(hero_level_up_deal ),
            "Time":str(int(time.time())*1000)
        }
        data_str = 'abc' + json.dumps(resultclient)
        data_bytes = data_str.encode('utf-8')
        #log_action(data + " success return! ")
        return Response(data_bytes, mimetype='application/octet-stream')
    if resultdic['DataName'] == 'BattleWayMap':
        #返回字节流
        idxobj = battlewaymap[str(resultdic['DataIdx'] )]
        if 'ExtraRewardString' not in idxobj:
            idxobj['ExtraRewardString'] = ""
        #判断 GroundPrefab 字段是否是字符串
        if 'GroundPrefab'in idxobj and idxobj['GroundPrefab'] != None and type(idxobj['GroundPrefab']) == str:
            idxobj['GroundPrefab'] = [idxobj['GroundPrefab']]
        # if idxobj['MonsterLevel'] > 261:
        #     idxobj['MonsterLevel'] = 261

        resultclient = {"DataString":json.dumps(idxobj),"DataIdx":str(resultdic['DataIdx']),"Time":str(int(time.time())*1000)}
        # data_str = json.dumps(resultclient)
        # if sqliteutil.get_game_platform(sqlconnfig['db_file'],sqlconnfig['table_name'],data) == "1":#如果是android
        data_str = 'abc'+json.dumps(resultclient)
        data_bytes = data_str.encode('utf-8')
        return Response(data_bytes, mimetype='application/octet-stream')
    #log_action(data + resultdic['DataName'] +" dataname legal! ")
    return Response(error_bytees, mimetype='application/octet-stream')



if __name__ == "__main__":
    # nucleus_deal = {}
    # for k, v in nucleus.items():
    #     print(k)
    #     nucleus_deal[k] = json.dumps(v)
    # hero_level_up_deal = {}
    # for k, v in hero_level_up.items():
    #     hero_level_up_deal[k] = json.dumps(v)
    # resultclient = {
    #     "Data_CNucleus": json.dumps(nucleus_deal),
    #     "Data_CHeroLevelUp": json.dumps(hero_level_up_deal),
    #     "Time": str(int(time.time()) * 1000)
    # }
    # data_str = 'abc' + json.dumps(resultclient)
    # print('android data_get')
    # print(resultclient)

    # sqliteutil.initdb(sqlconnfig['db_file'],sqlconnfig['table_name'])

    app.run(host='0.0.0.0', port=8080,debug=True)
