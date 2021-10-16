import jwt, datetime, time
from flask import jsonify,request
from app.users.model import Users,check_password,update
import common
import config

class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: datetime
        :return: string
        """
        try:
            payload = {
                'iss': 'ken',  # 签名
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=4),  # 过期时间
                'iat': datetime.datetime.utcnow(), #  开始时间
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            ) # 加密生成字符串
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, config.SECRET_KEY,algorithms='HS256') #options={'verify_exp': False} 加上后不验证token过期时间
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'


def authenticate(username, password):
    """
    用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
    :param password:
    :return: json
    """
    userInfo = Users.get_or_none(Users.username==username)
    if (userInfo is None):
        return jsonify(common.falseReturn('', '找不到用户'))
    else:
        if (check_password(userInfo.password, password)):
            login_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            userInfo.login_time = login_time
            update(userInfo)
            token = Auth.encode_auth_token(userInfo.id, login_time)
            return jsonify(common.trueReturn(token,'登录成功'))
        else:
            return jsonify(common.falseReturn('', '密码不正确'))

def identify(request):
    """
    用户鉴权
    :return: list
    """
    try:
        auth_header = request.headers.get('Authorization')
        if (auth_header):
            auth_tokenArr = auth_header.split(' ')
            if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
                result = common.falseReturn('', '请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = Auth.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = Users.get_or_none(Users.id == payload['data']['id'])
                    if (user is None):
                        result = common.falseReturn('', '找不到该用户信息')
                    else:
                        result = common.trueReturn(user.id, '请求成功')
                else:
                    result = common.falseReturn('', payload)
            return result

    except jwt.ExpiredSignatureError:
        result = common.falseReturn('', 'Token已更改，请重新登录获取')
        return result

    except jwt.InvalidTokenError:
        result = common.falseReturn('', '没有提供认证token')
        return result





