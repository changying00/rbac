import json
import base64
import uuid
from datetime import timedelta,datetime

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .captchacode import CaptchaCode
from apps.users.models import Captcha,User
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    return render(request, "index.html")


def auth_login(request):
    if request.method == "GET":
        return render(request, "login.html")
    #处理登录验证
    username = request.POST.get("username")
    password = request.POST.get("password")
    captcha = request.POST.get("captcha")
    captcha_key = request.POST.get("captchaKey")
    remember_me = request.POST.get("rememberMe")

   
    # 根据验证码的 键从 数据库 查询对应的 验证码
    queryset = Captcha.objects.filter(name=captcha_key,expire_time__gte=datetime.now())

    if not queryset.exists():
        return JsonResponse(data={"message": "验证码错误"},status=400)
    #获取 查询到 第一条记录
    if queryset.first().value.upper() != captcha.upper():
        #如果验证码不正确
        queryset.delete()  # 删除验证码，防止重复使用
        return JsonResponse(data={"message": "验证码错误"},status=400)

   
    #如果验证码正确
    queryset.delete()  # 删除验证码，防止重复使用
    # 查询当前用户是否存在
    queryset = User.objects.filter(username=username)
    if not queryset.exists():
        return JsonResponse(data={"message": "用户名或密码不正确"},status=400)

    # 获取 当前查询到的用户
    user = queryset.first()

    if not user.check_password(password):
        return JsonResponse(data={"message": "用户名或者密码不正确"},status=400)

    # 如果 密码一致、则 判断 当前是否 后台账号
    if not user.is_staff:
        return JsonResponse(data={"message": "当前账号没有后台登录权限"},status=400)

    if not user.state:
        return JsonResponse(data={"message": "当前账号已被禁用，请联系管理员"},status=400)

    # 进行登录、并将当前用户信息储存到 session 中
    login(request,user)

    if remember_me == 'off':
        #将session的过期时间设置为0(随浏览器的关闭而关闭)
        request.session.set_expiry(0)
    return JsonResponse(data={"message": "登录成功"})
def captcha_code(request):

    """
    生成验证码图片
    :param request:
    :return:
    """
    width = int(request.GET.get("width", 118))
    height = int(request.GET.get("height", 42))
    spacing = int(request.GET.get("spacing", 10))
    #删除过期的验证码
    Captcha.objects.filter(expire_time__lt=datetime.now()).delete()
    #创建一个 验证码对象
    captcha_code = CaptchaCode(width, height, spacing)

    #将图片转成base64格式的字符串
    bytesio, chars = captcha_code.get_captcha_code()
    imgurl = "data:image/png;base64," + base64.b64encode(bytesio.read()).decode("utf-8")

    # 生成一个唯一且不重复的字符串
    key = str(uuid.uuid4())

    #将key 和 chars 进行绑定、并存储到一个指定的容器中、方便登录的时候 进行验证码的校验
    #验证码默认俩小时过期
    Captcha.objects.create(name=key, value=chars, expire_time=timezone.now() + timedelta(hours=2))
    #返回一个 json 数据
    return JsonResponse({"url": imgurl, "name": key})

