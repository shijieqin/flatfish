# -*- coding: utf-8 -*-

from django.db import models
from supervisor.models import Node
from django.contrib.auth.models import Group

# Create your models here.


class Policy(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Police名字")

    nodes = models.ManyToManyField(Node)
    groups = models.ManyToManyField(Group)

    environment = models.TextField(verbose_name="环境(以;分割)", null=True, blank=True)
    type = models.TextField(verbose_name="功能(以;分割)", null=True, blank=True)

    c_time = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = "权限"
        ordering = ['-c_time']
