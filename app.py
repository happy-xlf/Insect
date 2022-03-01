from flask import Flask, render_template, request, jsonify
from livereload import Server
from utils.mysqlhelper import MySqLHelper
from utilsYunDuan.mysqlhelper import  MySqLHelper as MySqLHelper2
import re
import json
import datetime
import os,random
from werkzeug.utils import secure_filename
app = Flask(__name__)


#文件上传存放的文件夹, 值为非绝对路径时，相对于项目根目录
IMAGE_FOLDER  = 'static/photo/'

#生成无重复随机数
gen_rnd_filename = lambda :"%s%s" %(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), str(random.randrange(1000, 10000)))
#文件名合法性验证
allowed_file = lambda filename: '.' in filename and filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg', 'gif', 'bmp','gif','jfif'])

app.config.update(
    SECRET_KEY = os.urandom(24),
    # 上传文件夹
    UPLOAD_FOLDER = os.path.join(app.root_path, IMAGE_FOLDER),

    # 最大上传大小，当前16MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
)



#face照片上传
@app.route('/facephotoupload', methods=['POST','OPTIONS'])
def facephotoupload():
    res = dict(code=-1, msg=None)
    f = request.files.get('file')
    if f and allowed_file(f.filename):
        filename = secure_filename(gen_rnd_filename() + "." + f.filename.split('.')[-1])  # 随机命名
        # 自动创建上传文件夹
        print(filename)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        # 保存图片
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imgUrl = "static/photo/"+filename
        print(imgUrl)
        res.update(code=0, data=dict(src=imgUrl))
    else:
        res.update(msg="Unsuccessfully obtained file or format is not allowed")

    return jsonify(res)


@app.route('/')
def hello_world():
    return render_template('china.html')

@app.route('/home')
def getoHome():
    return render_template('index.html')

@app.route('/show_bz')
def show_bz():
    return render_template('labelweb.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/tz_insect_predict')
def tz_insect_predict():
    return render_template('insect_predict.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/show_mu/<name>',methods=['GET','POST'])
def show_mu(name):
    ans=""
    if name=="鳞翅目":
        print(name)
    elif name=="鞘翅目":
        print(name)
    elif name=="半翅目":
        print(name)
    return render_template('show_mu.html',name=name)

@app.route('/insect_sub/<name>',methods=['GET','POST'])
def insect_sub(name):
    return render_template('insect_sub.html',name=name)

@app.route('/get_insect_byname',methods=['GET','POST'])
def get_insect_byname():
    name = request.form.get("name")
    name=name.replace('卵','')
    name=name.replace('幼虫', '')
    name=name.replace('雌成虫', '')
    name=name.replace('雄成虫', '')
    name=name.replace('成虫', '')
    print(name)
    db = MySqLHelper()
    sql = "select * from insect_sub where name = %s;"
    jsonData = []
    ret, count = db.selectall(sql=sql, param=name)
    for row in ret:
        result = {}
        result['name'] = row[0]
        result['summary']=row[1]
        result['pic'] = row[2]
        result['danger']=row[3]
        result['video']=row[4]
        jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)


@app.route('/go_waitDo')
def go_waitDo():
    return render_template('waitDo.html')

@app.route('/get_insect_Picture',methods=['GET','POST'])
def get_insect_Picture():
    print("到了这里了")
    db = MySqLHelper2()
    sql = "select * from regpicture"
    jsonData = []
    ret, count = db.selectall(sql=sql)
    for row in ret:
        result = {}
        result['id'] = row[0]
        result['name'] = row[1]
        result['number']=row[2]
        result['about'] = row[3]
        print(str(row[0]) + "  " + row[1] + "  " + row[2] + "  " + row[3])
        jsonData.append(result)

    print("获取数据成功！！！")

    return json.dumps(jsonData)

@app.route('/get_insect_bymu',methods=['GET','POST'])
def get_insect_bymu():
    mu = request.form.get("mu")
    db = MySqLHelper()
    sql = "select insect.id,insect.name,insect_sub.pic from insect join insect_sub on insect.name=insect_sub.name where insect.mu=%s"
    jsonData = []
    ret, count = db.selectall(sql=sql,param=mu)
    for row in ret:
        result = {}
        result['id'] = row[0]
        result['name'] = row[1]
        result['pic']=row[2]
        jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)



@app.route('/show_insect',methods=['GET','POST'])
def show_insect():
    db = MySqLHelper()
    sql = "SELECT insect.name,area,pic from insect join insect_sub on insect.name=insect_sub.name"
    jsonData = []
    ret, count = db.selectall(sql=sql)
    if count != 0:
        for row in ret:
            result = {}
            result['name'] = row[0]
            ans=row[1]
            result['area'] = ans.split('；')[0]
            result['pic']=row[2]
            jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)


@app.route('/kind_insect',methods=['GET','POST'])
def sum_insect():
    db = MySqLHelper()

    sql = "select mu,COUNT(*) from insect GROUP BY mu"
    jsonData = []
    ret, count = db.selectall(sql=sql)
    if count != 0:
        for row in ret:
            result = {}
            result['mu'] = row[0]
            result['num'] = row[1]
            jsonData.append(result)

    sql2="SELECT MAX(id) from insect"
    ret2,count2=db.selectall(sql=sql2)
    for it in ret2:
        result={}
        result['mu']="总数"
        result['num']=it[0]
        jsonData.append(result)
    print(json.dumps(jsonData))
    return json.dumps(jsonData)

import paddlex

#动物识别
@app.route('/animal',methods=['GET','POST'])
def animal():
    img_dir=request.form.get("imgurl")
    model_dir = 'static/inference_model'
    model = paddlex.deploy.Predictor(model_dir, use_gpu=True)
    result = model.predict(img_dir)
    print(result)
    dict={
        "1.1":"草履蚧卵",
        "1.2":"草履蚧幼虫",
        "1.3":"草履蚧雌成虫",
        "1.4":"草履蚧雄成虫",
        "2.1":"麻皮蝽卵",
        "2.2":"麻皮蝽幼虫",
        "2.3":"麻皮蝽成虫",
        "3.1":"日本脊吉丁卵",
        "3.2":"日本脊吉丁幼虫",
        "3.3":"日本脊吉丁成虫",
        "4.1":"星天牛卵",
        "4.2":"星天牛幼虫",
        "4.3":"星天牛成虫",
        "5.1":"桑天牛卵",
        "5.2":"桑天牛幼虫",
        "5.3":"桑天牛成虫",
        "6.1":"松墨天牛卵",
        "6.2":"松墨天牛幼虫",
        "6.3":"松墨天牛成虫",
        "7.1":"柳蓝叶甲卵",
        "7.2":"柳蓝叶甲幼虫",
        "7.3":"柳蓝叶甲成虫",
        "8.1":"黄刺蛾卵",
        "8.2":"黄刺蛾幼虫",
        "8.3":"黄刺蛾成虫",
        "9.1":"褐边绿刺蛾卵",
        "9.2":"褐边绿刺蛾幼虫",
        "9.3":"褐边绿刺蛾成虫",
        "10.1":"霜天蛾卵",
        "10.2":"霜天蛾幼虫",
        "10.3":"霜天蛾成虫",
        "11.1":"杨扇舟蛾卵",
        "11.2":"杨扇舟蛾幼虫",
        "11.3":"杨扇舟蛾成虫",
        "12.1":"杨小舟蛾卵",
        "12.2":"杨小舟蛾幼虫",
       "12.3":"杨小舟蛾成虫",
        "13.1":"美国白蛾卵",
        "13.2":"美国白蛾幼虫",
        "13.3":"美国白蛾成虫",
        "14.1":"人纹污灯蛾卵",
        "14.2":"人纹污灯蛾幼虫",
        "14.3":"人纹污灯蛾成虫",
        "15.1":"丝带凤蝶卵",
        "15.2":"丝带凤蝶幼虫",
        "15.3":"丝带凤蝶雌成虫",
        "15.4":"丝带凤蝶雄成虫",
    }

    insect = {}

    insect["name"]=dict[result[0]['category']]
    insect["similar"]=str(result[0]['score'])

    return json.dumps(insect,ensure_ascii=False)


@app.route('/getkindsum',methods=['GET','POST'])
def getkindsum():
    db = MySqLHelper()

    sql = "select COUNT(*) as count from insect where mu='半翅目'"
    result={}
    ret, count = db.selectall(sql=sql)
    if count != 0:
        for row in ret:
            result['bcm'] = row[0]

    sql2 = "select COUNT(*) as count from insect where mu='鳞翅目'"
    ret2, count2 = db.selectall(sql=sql2)
    if count2 != 0:
        for row in ret2:
            result['lcm'] = row[0]

    sql3 = "select COUNT(*) as count from insect where mu='鞘翅目'"
    ret3, count3 = db.selectall(sql=sql3)
    if count3 != 0:
        for row in ret3:
            result['qcm'] = row[0]

    sql4="select COUNT(*) as count from insect";
    ret4, count4 = db.selectall(sql=sql4)
    if count4 != 0:
        for row in ret4:
            result['sum'] = row[0]

    time=datetime.datetime.now().strftime('%Y-%m')
    sql5 = "select * from insect where time like '" + time + "%'";
    ret5, count5 = db.selectall(sql=sql5)
    result['month_num'] = count5
    print(result['month_num'])

    return json.dumps(result)

import requests
def geocode(address):
    parameters = {'address': address, 'key': '3409090984aea93d6ee622ffa4097165'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    print(answer)
    #print(address + "的经纬度：", answer['geocodes'][0]['location'])
    if answer['geocodes']==[]:
        return "null"
    str = answer['geocodes'][0]['location']
    list = str.split(',')
    newlist = []
    for it in list:
        newlist.append(float(it))
    return newlist

#获取14中昆虫的分布信息场所的迁移图
@app.route('/getinsectlocation',methods=['GET','POST'])
def getinsectlocation():
    db = MySqLHelper()
    insects=['草履蚧','麻皮蝽','扁刺蛾','人纹污灯蛾','霜天蛾','杨扇舟蛾']
    names=['one','two','three','four','five','six']
    result={}
    ans={}
    data=[]
    i=0
    for it in insects:
        l=[]
        start=""
        f=0
        sql="select * from insect where name='"+it+"'"
        ret, count = db.selectall(sql=sql)
        area=""
        if count != 0:
            for row in ret:
                area = row[6]
        list=area.split('、')
        for tt in list:
            if tt!="":
                if f == 0:
                    f = 1
                    start = tt
                l2=[]
                vas={"name":start}
                if start==tt:
                    vas2={"name":tt,"value":200}
                else:
                    vas2={"name":tt,"value":55}
                l2.append(vas)
                l2.append(vas2)
                l.append(l2)
        ans[names[i]]=l
        i=i+1
    ans["name"]=insects
    print(ans)
    return jsonify(ans)

#获取14中昆虫的分布信息场所的迁移图
@app.route('/getlist',methods=['GET','POST'])
def getlistn():
    db = MySqLHelper()
    #'草履蚧', '麻皮蝽', '扁刺蛾', '人纹污灯蛾', '霜天蛾', '杨扇舟蛾'
    insects = ['杨扇舟蛾']
    # names = ['one', 'two', 'three', 'four', 'five', 'six']
    result={}
    ans={}
    data=[]
    i=0
    for it in insects:
        l=[]
        start=""
        f=0
        sql="select * from insect where name='"+it+"'"
        ret, count = db.selectall(sql=sql)
        area=""
        if count != 0:
            for row in ret:
                area = row[6]
        list=area.split('、')
        for tt in list:
            if tt!="":
                jwd=geocode(tt)
                if jwd!="null":
                    result[tt]=jwd
                else:
                    print(tt)
    return jsonify(result)

import pymysql
#获取昆虫分布省份的总和信息
@app.route('/getsumprovince',methods=['GET','POST'])
def getsumprovince():
    db = pymysql.connect(host="localhost", user="root", password="root", database="insect_database", charset='utf8')
    cursor = db.cursor()
    insect_name = []
    insect_city = []
    insect_province = []
    sql_insect = "select * from insect"
    cursor.execute(sql_insect)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        name=row[4]
        pro=row[7]
        insect_name.append(name)
        insect_province.append(pro)

    anspro=[]
    anssum=[]
    for i in range(len(insect_name)):
        list=insect_province[i].split('、')
        for item in list:
            if item not in anspro:
                anspro.append(item)
                anssum.append(1)
            else:
                idx=anspro.index(item)
                anssum[idx]=anssum[idx]+1

    ans={}
    ans["province"]=anspro
    ans["sum"]=anssum
    return jsonify(ans)




if __name__ == '__main__':

    app.run(debug=True)
