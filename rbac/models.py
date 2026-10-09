from django.db import models 

class BaseModel(models.Model):
    state = models.BooleanField(null=True, blank=True, default=True, db_comment="状态", verbose_name="状态")

    create_time = models.DateTimeField(auto_now_add=True, db_comment="录入时间")

    update_time = models.DateTimeField(null=True, blank=True, db_comment="最后一次更新时间")

    is_delete = models.BooleanField(blank=True, default=False, db_comment="是否被删除")

    delete_time = models.DateTimeField(null=True,blank = True,db_comment = "删除时间")

    note = models.TextField(null=True, blank=True, db_comment="备注", verbose_name="备注")
    class Meta:
        abstract = True