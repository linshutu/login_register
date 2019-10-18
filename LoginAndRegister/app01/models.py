from django.db import models
from captcha.fields import CaptchaField

# Create your models here.
class User(models.Model):
	"""
	用户表
	"""
	gender = (
		('male',"男"),
		('female',"女"),
	)
	name = models.CharField(verbose_name="姓名",max_length=128,unique=True)
	password = models.CharField(max_length=256)
	email = models.EmailField(unique=True)
	sex = models.CharField(max_length=32,choices=gender,default="男")
	c_time = models.DateTimeField(auto_now_add=True)
	has_confirmed = models.BooleanField(default=False)

	def __str__(self):
		"""
		人性化显示对象信息
		:return:
		"""
		return self.name

	class Meta:
		ordering = ['-c_time']
		verbose_name = "用户"
		verbose_name_plural = "用户"
	'''
	注意：这里的用户名指的是网络上注册的用户名，不要等同于现实中的真实姓名，所以采用了唯一机制。
	如果是现实中的人名，那是可以重复的，肯定是不能设置unique的。另外关于密码，建议至少128位长度，原因后面解释。
	'''
class Author(models.Model):
	"""
	作者表
	"""
	gender = (
		('male',"男"),
		('female',"女"),
	)
	name = models.CharField(max_length=32)
	age = models.IntegerField()
	sex = models.CharField(max_length=16,choices=gender,default="男")
	au = models.OneToOneField("AuthorDetail",on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "作者表"
		verbose_name_plural = "作者表"

class AuthorDetail(models.Model):
	"""
	作者详细信息表
	"""
	birthday = models.DateField()
	telephone = models.CharField(max_length=11)
	addr = models.CharField(max_length=64)

	def __str__(self):
		return self.telephone + self.addr

class Publish(models.Model):
	"""
	出版社表
	"""
	name=models.CharField( max_length=32)
	city=models.CharField( max_length=32)
	def __str__(self):
		return self.name

class Book(models.Model):
	"""
	书籍表
	"""
	title = models.CharField(max_length=32)
	publishDate = models.DateField()
	price = models.DecimalField(max_digits=5, decimal_places=2)
	publishs = models.ForeignKey(to="Publish",on_delete=models.CASCADE)
	authors = models.ManyToManyField("Author",)

	def __str__(self):
		return self.title

	def get_authors_name(self):
		"""
		获得每本书的所有作者
		:return:
		"""
		# authors = self.authors.all()
		# name_list = []
		# for i in authors:
		#     name_list.append(i.name)
		#
		# return ','.join(name_list)
		return ','.join([i.name for i in self.authors.all()])


