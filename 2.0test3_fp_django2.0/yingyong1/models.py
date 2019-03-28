from django.db import models

# Create your models here.


# 600000 浦发银行  日期	    开盘	    最高	    最低	    收盘	    成交量	    成交额

class Gupiao(models.Model):

	id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=6)
	name = models.CharField(max_length=10)
	date = models.CharField(max_length=10)
	kp = models.DecimalField(max_digits=7, decimal_places=2, null=True)
	zg = models.DecimalField(max_digits=7, decimal_places=2, null=True)
	zd = models.DecimalField(max_digits=7, decimal_places=2, null=True)
	sp = models.DecimalField(max_digits=7, decimal_places=2, null=True)
	cjl = models.DecimalField(max_digits=13, decimal_places=2, null=True)
	cje = models.DecimalField(max_digits=13, decimal_places=2, null=True)
	today_ma20 = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	today_md = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	bls = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	blz = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	blx = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	today_ma20_1_1 = models.DecimalField(max_digits=10,decimal_places=5, null=True)
	today_md_1_1 = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	bls_1_1 = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	blz_1_1 = models.DecimalField(max_digits=10, decimal_places=5, null=True)
	blx_1_1 = models.DecimalField(max_digits=10, decimal_places=5, null=True)


	class Meta:
		unique_together=("code", "name", "date",)