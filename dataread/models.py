import datetime

from django.db import models
import datetime
# Create your models here.

class Competition(models.Model):
    YEAR_CHOICES = [(r,r) for r in range(1980, int(datetime.datetime.now().year)+1)]
    COMPETITION_LEVEL_CHOICES = [('国家级', '国家级'), ('省部级', '省部级'), ('校级', '校级')]
    AWARD_LEVEL_CHOICES = [('一等奖', '一等奖'), ('二等奖', '二等奖'), ('三等奖', '三等奖')]
    # 年份
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    # 竞赛名称
    name = models.CharField(max_length=200)
    # 竞赛级别
    competition_level = models.CharField(max_length=200, choices=COMPETITION_LEVEL_CHOICES)
    # 获奖级别
    award_level = models.CharField(max_length=200, choices=AWARD_LEVEL_CHOICES)
    # 负责人姓名
    leader_name = models.CharField(max_length=200)
    # 负责人学号(可选)
    leader_id = models.CharField(max_length=200, blank=True, null=True)
    # 成员
    member_name = models.CharField(max_length=200)
    # 是否为国院
    is_guoyuan = models.BooleanField(default=False)

class Users(models.Model):
    # 用户基本信息
    username = models.CharField(max_length=20,default=None,null=True)
    password = models.CharField(max_length=20,default=None,null=True)

    # 是否为管理员
    manager = models.BooleanField(default=False,blank=True,null=True)

    # 真实姓名
    real_name = models.CharField(max_length=20,default=None,null=True)


    def __str__(self):
        return self.name