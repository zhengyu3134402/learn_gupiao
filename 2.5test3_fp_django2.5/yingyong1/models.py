from django.db import models

# Create your models here.


# 600000 浦发银行  日期	    开盘	    最高	    最低	    收盘	    成交量	    成交额

class Gupiao(models.Model):

	id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=6)
	name = models.CharField(max_length=10)
	date = models.CharField(max_length=10)
	kp = models.DecimalField(max_digits=7,decimal_places=2)
	zg = models.DecimalField(max_digits=7,decimal_places=2)
	zd = models.DecimalField(max_digits=7,decimal_places=2)
	sp = models.DecimalField(max_digits=7,decimal_places=2)
	cjl = models.DecimalField(max_digits=13,decimal_places=2)
	cje = models.DecimalField(max_digits=13,decimal_places=2)

	class Meta:
		unique_together=("code", "name", "date",)