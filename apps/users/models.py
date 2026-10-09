from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from rbac.models import BaseModel

# Create your models here.
class Depart(BaseModel):

    name = models.CharField(max_length=100,null= False,blank=True,db_comment="部门名称",verbose_name="部门名称")

    code = models.CharField(max_length=8,null= False,blank=True,db_comment="部门编号",verbose_name="部门编号")

    manager = models.CharField(max_length=20, null=True, blank=True, db_comment="部门负责人", verbose_name="部门负责人")

    phone = models.CharField(max_length=20, null=True, blank=True, db_comment="联系电话", verbose_name="联系电话")

    sort = models.IntegerField(null=False, blank=True, verbose_name="排序", db_comment="排序")

    # 定义一个关系属性、且维护 它自身、做成 树状结构
    parent_depart = models.ForeignKey(to="self", on_delete=models.DO_NOTHING, null=True, blank=True, related_name="children")

    class Meta(BaseModel.Meta):
        db_table = "tb_depart"

class Role(BaseModel):

    name = models.CharField(max_length=100, null=False, blank=True, db_comment="角色名称", verbose_name="角色名称")

    code = models.CharField(max_length=8, null=False, blank=True, db_comment="角色编号", verbose_name="角色编号")

    sort = models.IntegerField(null=False, blank=True, verbose_name="排序", db_comment="排序")
    class Meta(BaseModel.Meta):
        db_table = "tb_role"

class User(AbstractBaseUser, PermissionsMixin):
    """
    扩展 自己的 认证 User 模型
    可以 去掉 内置User 不合适的字段、添加合适的属性(字段)
    """
    username = models.CharField(max_length=150, db_comment="用户名", unique=True, blank=True)

    name = models.CharField(max_length=20, db_comment="姓名", blank=True)

    email = models.EmailField(max_length=254, db_comment="邮箱", blank=True, null=True)

    is_staff = models.BooleanField(default=False, db_comment="是否允许访问后台")

    date_joined = models.DateTimeField(auto_now_add=True, db_comment="注册时间")

    tel = models.CharField(max_length=11, blank=True, null=True, db_comment="手机号")

    state = models.BooleanField(null=True, blank=True, default=True, db_comment="状态", verbose_name="状态")

    note = models.TextField(null=True, blank=True, db_comment="备注", verbose_name="备注")

    # 关联 部门信息
    depart = models.ForeignKey(to=Depart, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="users")

    # 维护和 角色的关系
    roles = models.ManyToManyField(to=Role, blank=True,db_table = "tb_user_role", related_name="users")
    USERNAME_FIELD = 'username'  # 指定 用哪个字段 作为 用户名, 用户名必须是 唯一的
    EMAIL_FIELD = "email"        # 设置哪一个字段是邮箱
    REQUIRED_FIELDS = ["email"]  # 设置 哪一个字段是否是必传的

    # 必须配置 一个 模型管理器 
    objects = UserManager()

    class Meta:

        db_table = "auth_user" 
        # 指定 该模型类 可以被 替换
        swappable = 'AUTH_USER_MODEL'

class Captcha(models.Model):

    name = models.CharField(max_length = 36,db_comment= "验证码的键")

    value = models.CharField(max_length = 20,db_comment= "验证码的值")


    expire_time = models.DateTimeField(db_comment= "验证码的过期时间",null = True, blank = True)
    class Meta:
        db_table = "tb_captcha"