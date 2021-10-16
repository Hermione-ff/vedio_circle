from app.users.model import *
from app.auth.auths import Auth,authenticate,identify
import time
import common



app = Flask(__name__)
db = MySQLDatabase("data",user='root',password='123456',host='127.0.0.1',port=3306,charset='utf8mb4')
db.connect()

@app.route("/",)
def hallo_vedio_circle():
    return 'Hello  vediocircle'

@app.route('/register', methods=['POST'])
def register():
    """
    用户注册
    用户名 username sashuishui
    密码 password 12123232
    邮箱  123456789@qq.com
    :return: json
    """
    get_data = request.get_json()
    email = get_data.get("email")
    username = get_data.get("username")
    password = get_data.get("password")
    user = Users(email=email, username=username, password=set_password(password))
    add(user)
    if user.id:
        returnUser = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'login_time': user.login_time
        }
        return jsonify(common.trueReturn(returnUser, "用户注册成功"))
    else:
        return jsonify(common.falseReturn('', '用户注册失败'))


@app.route('/login', methods=['POST'])
def login():
    """
    用户登录
    用户名 username sashuishui
    密码 password 12123232
    :return: json
    """
    get_user = request.get_json()
    username = get_user.get('username')
    password = get_user.get('password')
    if (not username or not password):
        return jsonify(common.falseReturn('', '用户名和密码不能为空'))
    else:
        return authenticate(username, password)

@app.route('/user', methods=['GET'])
def getuser():
    """
    获取用户信息
    Authorization : token
    :return: json
    """
    result = identify(request)
    if (result['status'] and result['data']):
        user = get(Users.get_or_none(Users.id==result['data']))
        returnUser = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'login_time': user.login_time
        }
        result = common.trueReturn(returnUser, "请求成功")
    return jsonify(result)



#用户发送视频,保存用户视频数据
@app.route("/user/video", methods=["POST"])
def user_data():
    """
    headers{Authorization:token}
    body{
    视频url url video.mp4
    文字    content 嘻嘻
    视频类型  type 1/2
    }
    :return: json
    """
    get_data = request.get_json()
    result = identify(request)
    if (result['status'] and result['data']):
        user = get(Users.get_or_none(Users.id == result['data']))
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 改变时间格式,不然插入数据库会报错，数据库是datetime类型
        username = user.username
        url = get_data.get("url")
        content = get_data.get("content")
        type = get_data.get("type")
        video = Videodata(date=date,username=username,url=url,content=content,type=type)
        add(video)
        if video.id:
            returnVideo = {
                'id': video.id,
                'date':video.date,
                'username': video.username,
                'url': video.url,
                'content': video.content,
                'type':video.type
            }
            return jsonify(common.trueReturn(returnVideo, "视频发表成功"))
        else:
            return jsonify(common.falseReturn('', '视频发表失败'))
    else:
        return jsonify(common.falseReturn('','用户未认证'))


#用户删除视频
@app.route("/user/deletevideo", methods=["DELETE"])
def user_deletevedio():
    """
    返回用户要删除的视频id
    id number
    :return: json
    """
    get_data = request.get_json()
    result = identify(request)
    if (result['status'] and result['data']):
        id = get_data.get("id")
        video = get(Videodata.get_or_none(Videodata.id == id))
        delete(video)
        if (Videodata.get_or_none(Videodata.id == id) == None):
            return jsonify(common.trueReturn('', "视频删除成功"))
        else:
            return jsonify(common.falseReturn('', '视频删除失败'))
    else:
        return jsonify(common.falseReturn('', '用户未认证'))



if __name__ == '__main__':
    app.run()

