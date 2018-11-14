from django.db import models
from core.xmlrpc import XmlRpc

# Create your models here.


class Node(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="节点名")
    description = models.TextField(null=True, blank=True, verbose_name='描述')
    host = models.CharField(max_length=128, verbose_name="IP或域名")
    port = models.IntegerField(verbose_name="端口")
    username = models.CharField(max_length=128, null=True, verbose_name="用户名")
    password = models.CharField(max_length=128, null=True, verbose_name="密码")

    c_time = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    def __str__(self):
        return '%s(%s)' % (self.name, self.host)

    def generate_connection(self):

        return XmlRpc.connection(
            self.host, self.port, self.username, self.password
        )

    class Meta:
        verbose_name = '节点'
        verbose_name_plural = "节点"
        ordering = ['-c_time']
        unique_together = (('host', 'port'),)