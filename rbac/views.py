import json
import base64
import uuid
from datetime import timedelta,datetime

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .captchacode import CaptchaCode
from apps.users.models import Captcha


def index_page(request):
    return render(request, "index.html")


def auth_login(request):
    if request.method == "GET":
        return render(request, "login.html")

    #处理登录验证
    username = request.POST.get("username")
    password = request.POST.get("password")
    captcha = request.POST.get("captcha")
    captcha_key = request.POST.get("captchakey")
    remember_me = request.POST.get("rememberMe")

    # 根据验证码的 键从 数据库 查询对应的 验证码
    queryset = Captcha.objects.filter(name=captcha_key,expire_time__gte=datetime.now())

    if not queryset.exists():
        return JsonResponse(data={"message": "验证码错误"},status=400)
    #获取 查询到 第一条记录
    if queryset.first().value.upper() != captcha.upper():
        return JsonResponse(data={"message": "验证码错误"},status=400)

    #如果验证码正确
    queryset.delete()  # 删除验证码，防止重复使用
    #删除过期的验证码
    Captcha.objects.filter(expire_time__lt=datetime.now()).delete()
    

    
def captcha_code(request):
    """
    生成验证码图片
    :param request:
    :return:
    """
    width = int(request.GET.get("width", 118))
    height = int(request.GET.get("height", 42))
    spacing = int(request.GET.get("spacing", 10))

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

#处理登录 验证问题
def verify_login(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "请使用 POST 请求"}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"success": False, "message": "请求数据格式错误"}, status=400)

    username = str(data.get("username", "")).strip()
    password = data.get("password", "")
    captcha = str(data.get("captcha", "")).strip()
    captcha_key = str(data.get("captcha_key", "")).strip()
    if not username or not password or not captcha or not captcha_key:
        return JsonResponse({"success": False, "message": "账号、密码和验证码不能为空"}, status=400)

    captcha_obj = Captcha.objects.filter(name=captcha_key).first()
    if captcha_obj is None:
        return JsonResponse({"success": False, "message": "验证码已过期，请刷新页面"})

    captcha_value = captcha_obj.value

    is_expired = captcha_obj.expire_time is None or captcha_obj.expire_time < timezone.now()
    captcha_obj.delete()
    
    if is_expired:
        return JsonResponse({"success": False, "message": "验证码已过期，请刷新页面"})
    if captcha_value.lower() != captcha.lower():
        return JsonResponse({"success": False, "message": "验证码错误"})

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"success": False, "message": "账号或密码错误"})

    login(request, user)
    return JsonResponse({"success": True, "message": "登录成功"})

