from flask import Flask,request,jsonify
import base64
import re
import collections as cl
import json
import copy

#server
app = Flask(__name__)



def convert_b64_to_file(b64,outfile_path):
    """
    b64をデコードしてファイルに書き込む
    """
    s = base64.decodestring(b64)
    with open(outfile_path,"wb") as f :
        f.write(s)

def speech():


    return K1speech

#base64でエンコードされたjsonファイルをデコード
@app.route('/post_request', methods=['POST'])
def post_request():
    # Bad request
    if not request.headers['Content-Type'] == 'application/json':
        return jsonify(res='failure'), 400
    ###jsonはdict型なので即変換できないからlistに入れて処理している
    global count
    global K1speech
    global K2speech
    global K1scene
    global K2scene

    #jsonを取得
    data = request.json
    #keysを取得
    keys_array = list(data.keys()) #list()は{...}が[...]になる
    #valuesを取得
    values_array = list(data.values())
    """
    送ってくるjsonは一つ目の要素が{画像名:base64エンコード}としたもの
    """
    K1IDlist=[]
    K2IDlist=[]
    #depth用のlist
    K1depthlist=[]
    K2depthlist=[]
    K1center=[]
    K2center=[]
    K1sk={}
    K2sk={}
    pointK1,pointK2 = 0,0
    #keys_arrayにあるkeyリストをひとつひとつ見ていく
    for key_index in range(len(keys_array)):
        #key_index は　0,1,2...

        """
        ここでJSONkeyの場合分けをしている
        """

        #画像だった場合
        if re.search("K1_Objects",keys_array[key_index]):
            K1_object_list = []
            K1_confidence_list = []
            '''
            object_list[0]:ID1の物体名N-best
            object_list[1]:ID2の物体名N-best
            ...
            confidence_list[0]~も同様
            '''

            #画像の保存名
            save_name = "./K1fig/"+keys_array[key_index] + ".jpg"
            #コンバート
            convert_b64_to_file(bytes(values_array[key_index],"utf-8"),save_name)

            '''
            切り出し画像を、物体認識プログラムへ入力
            ここで物体辞書を用意?
            出力　name=[エルモ,トトロ,ねこ...]
                 confidence = [,,,...]
            '''

        elif re.search("K2_Objects",keys_array[key_index]):
            K2_object_list = []
            K2_confidence_list = []
            '''
            object_list[0]:ID1の物体名N-best
            object_list[1]:ID2の物体名N-best
            ...
            confidence_list[0]~も同様
            '''

            #画像の保存名
            save_name = "./K2fig/"+keys_array[key_index] + ".jpg"
            #コンバート
            convert_b64_to_file(bytes(values_array[key_index],"utf-8"),save_name)

            '''
            切り出し画像を、物体認識プログラムへ入力
            ここで物体辞書を用意?
            出力　name=[エルモ,トトロ,ねこ...]
                 confidence = [,,,...]
            '''

        #ID番号が入っている場合
        elif re.search("K1_ObjectID",keys_array[key_index]):
            #IDlistに追加
            K1IDlist.append(int(keys_array[key_index][0]))
            ##int(keys_array[key_index][0])はID番号が入る
            ##"1_K1_ObjectID"の最初の文字の"1"
            #ソート
            K1IDlist=sorted(K1IDlist)
        elif re.search("K2_ObjectID",keys_array[key_index]):
            #IDlistに追加
            K2IDlist.append(int(keys_array[key_index][0]))
            #ソート
            K2IDlist=sorted(K2IDlist)
        elif re.search("K1_ObjectDepth",keys_array[key_index]):
            K1depthlist.append([int(keys_array[key_index][0]),int(values_array[key_index])])
        elif re.search("K2_ObjectDepth",keys_array[key_index]):
            K2depthlist.append([int(keys_array[key_index][0]),int(values_array[key_index])])

        elif re.search("Pointing_K1",keys_array[key_index]):
            if int(values_array[key_index]) == 1:
                pointK1=int(keys_array[key_index][0])

        elif re.search("Pointing_K2",keys_array[key_index]):
            print(type(values_array[key_index]))
            if int(values_array[key_index]) == 1:
                pointK2=int(keys_array[key_index][0])

            # pointK2=int(keys_array[key_index][0])
        elif re.search("K1_Sk",keys_array[key_index]):
            #K1sk.append([str(keys_array[key_index]),float(values_array[key_index])])
            #→["K1_SkLeftHand_X","0.000000"]
            K1sk[str(keys_array[key_index])]=float(values_array[key_index])
        elif re.search("K2_Sk",keys_array[key_index]):
            #K2sk.append([str(keys_array[key_index]),float(values_array[key_index])])
            K2sk[str(keys_array[key_index])]=float(values_array[key_index])
        elif re.search("K1_Center",keys_array[key_index]):
            if keys_array[key_index][-1] == "X":
                lflag = 0
            else:
                lflag = 1
            K1center.append([lflag,int(keys_array[key_index][0]),int(values_array[key_index])])
        elif re.search("K2_Center",keys_array[key_index]):
            if keys_array[key_index][-1] == "X":
                lflag = 0
            else:
                lflag = 1
            K2center.append([lflag,int(keys_array[key_index][0]),int(values_array[key_index])])
        #それ以外の場合は空文字を表示
        else:
            print("",end="")
    K1scene = cl.OrderedDict()#順番にデータ格納するため
    K2scene = cl.OrderedDict()#順番にデータ格納するため
    K1data = cl.OrderedDict()#順番にデータ格納するため
    K2data = cl.OrderedDict()#順番にデータ格納するため
    for i in K1IDlist:
        if i == pointK1: #and flag == 0:
            K1data["motion"] = "POINTING"
            flag = 1

        elif i != pointK1:
            K1data["motion"] = ""
        center = []
        center.append([float("inf"),float("inf"),float("inf")])
        tempcount=0
        tempID = 0
        for j in K1center:
            if tempcount == 2:
                center.append([float("inf"),float("inf"),float("inf")])
                tempID+=1
            tempcount+=1
            if j[0] == 0:
                center[tempID][0]=j[2]
            else:
                center[tempID][1]=j[2]

        for dep in K1depthlist:
            if dep[0] == i:
                center[dep[0]-1][2]=dep[1]

        K1data["location"] = center[i-1]
            # if j[1] == i:
            #     if j[0] == 0:
            #         center.append(["X",j[2]])
            #     else:
            #         center.append(["Y",j[2]])

        # for j in K1depthlist:
            # if j[1] == i:
                # K1data["location"] = center.append(j[1])
                # K1data["location"] =
                #f.write(str(j[1])+"\t")
        #K1data["object"] = K1_object_list[i-1]
        #K1data["confidence"] = K1_confidence_list[i-1]
        # K1scene[str(i)] = K1data #辞書型のデータ
        """
        辞書型のDeep Copy
        """
        K1scene[str(i)] = copy.deepcopy(K1data)

    #print("pointK2",pointK2)
    for i in K2IDlist:
        if i == pointK2: #and flag == 0:
            K2data["motion"] = "POINTING"

        elif i != pointK2:
            K2data["motion"] = ""

        # for j in K2center:
        #     center = []
        #     if j[0] == i:
        #         center.append(j[1])
        # for j in K2depthlist:
        #     if j[0] == i:
        #         K2data["location"] = center.append(j[1])
        center = []
        center.append([float("inf"),float("inf"),float("inf")])
        tempcount=0
        tempID = 0
        for j in K2center:
            if tempcount == 2:
                center.append([float("inf"),float("inf"),float("inf")])
                tempID+=1
            tempcount+=1
            if j[0] == 0:
                center[tempID][0]=j[2]
            else:
                center[tempID][1]=j[2]

        for dep in K2depthlist:
            if dep[0] == i:
                center[dep[0]-1][2]=dep[1]

        K2data["location"] = center[i-1]
                #f.write(str(j[1])+"\t")
        #K2data["object"] = K2_object_list[i-1]
        #K2data["confidence"] = K2_confidence_list[i-1]
        # K2scene[str(i)] = K2data #辞書型のデータ
        K2scene[str(i)] = copy.deepcopy(K2data)

    ###
    #global scene
    K1scene.update(K1sk)
    K2scene.update(K2sk)
    print("K1speech\n",K1speech)
    if K1speech != {}:
        K1scene.update(K1speech)
        print(K1speech)
        K1speech = {}
    if K2speech != {}:
        K2scene.update(K2speech)
        print(K2speech)
        K2speech = {}


    K1_f = open('./K1multimodal/K1multimodal'+str(count)+'.json','w')
    K2_f = open('./K2multimodal/K2multimodal'+str(count)+'.json','w')
    count += 1
    #fl = open('scene_log.json', 'a+')
    json.dump(K1scene,K1_f,indent=4,ensure_ascii=False)
    json.dump(K2scene,K2_f,indent=4,ensure_ascii=False)

    return jsonify(res='success', **data)

##発話の認識結果のjsonを保存する
@app.route('/K1chat', methods=['POST'])
def post_request_K1chat():
    # Bad request
    if not request.headers['Content-Type'] == 'application/json':
        return jsonify(res='failure'), 400
    ###jsonはdict型なので即変換できないからlistに入れて処理している

    #jsonを取得
    K1speech = request.json
    K1scene.update(K1speech)
    K1_f = open('./K1multimodal/K1multimodal'+str(count-1)+'.json','w')
    json.dump(K1scene,K1_f,indent=4,ensure_ascii=False)

    return jsonify(res='success', **K1speech)

@app.route('/K2chat', methods=['POST'])
def post_request_K2chat():
    # Bad request
    if not request.headers['Content-Type'] == 'application/json':
        return jsonify(res='failure'), 400
    ###jsonはdict型なので即変換できないからlistに入れて処理している

    #jsonを取得
    K2speech = request.json
    K2scene.update(K2speech)
    K2_f = open('./K2multimodal/K2multimodal'+str(count-1)+'.json','w')
    json.dump(K2scene,K2_f,indent=4,ensure_ascii=False)    

    return jsonify(res='success', **K2speech)

if __name__ == "__main__":
    count = 0
    print("初期化1")
    K1speech = {}
    print("初期化2")
    K2speech = {}
    print("初期化3")
    app.debug = True
    #app.run(host = "163.225.223.111")
    app.run(host='127.0.0.1')
    # app.run(host='10.0.2.15')
