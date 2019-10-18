Django实现可重用注册登录系统

项目源码：git@github.com:linshutu/login_register.git

### 项目流程

- 搭建项目环境
- 设计数据模型
- admin后台
- url路由和视图
- 前端页面设计
- 登录视图
- Django表单(综合前面的步骤)
- 图片验证码
- session会话
- 注册视图
- 邮箱注册确认
- 重用app

<!----more---->

#### 1搭建项目环境

```
--Python3.6.6
--Django1.11.9
--Bootstrap4
--Pycharm2017
--windows10
```

用户登录与注册系统非常具有代表性，适用面广，灵活性大，绝大多数项目都需要将其作为子系统之一。

本项目目的是打造一个针对管理系统、应用程序等需求下的可重用的登录/注册app，而不是门户网站、免费博客等无需登录即可访问的网站。

##### 一、创建工程与app

创建工程

![](http://9017499461.linshutu.top/%E7%99%BB%E9%99%86%E9%A1%B9%E7%9B%AE1.png)

创建app

![](http://9017499461.linshutu.top/%E7%99%BB%E9%99%86%E9%A1%B9%E7%9B%AE2.png)

下面就是一段时间的等待，Pycharm会帮助我们自动创建虚拟环境，以及安装最新版本的Django。

创建完成之后，进入Pycharm的设置菜单，可以看到当前Django版本是最新的2.2版本。如果你要指定过去的版本，比如2.1、1.11等，那就不能这么操作了，需要在命令行下自己创建虚拟环境并安装django。或者在这里先删除Django，再安装你想要的指定版本。

![](http://9017499461.linshutu.top/%E7%99%BB%E9%99%86%E9%A1%B9%E7%9B%AE3.png)

##### 二、设置时区和语言

Django默认使用美国时间和英语，在项目的settings文件中，如下所示：

```python
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```

我们把它改为`亚洲/上海`时间和中文（别问我为什么没有北京时间，也别把语言写成`zh-CN`），注意USE_TZ 改成False了。

```python
LANGUAGE_CODE = 'zh-hans'     # 这里修改了

TIME_ZONE = 'Asia/Shanghai'    # 这里修改了

USE_I18N = True

USE_L10N = True

USE_TZ = False    # 这里修改了
```

##### 三、启动开发服务器

在Pycharm的`Run/Debug Configurations`配置界面里，将HOST设置为`127.0.0.1`，Port保持原样的`8000`，确定后，点击绿色三角，走你！

#### 2设计数据模型

使用Django开发Web应用的过程中，很多人都是急急忙忙地写视图，写前端页面，把最根本的模型设计给忽略了。模型中定义了数据如何在数据库内保存，也就是数据表的定义方式。这部分工作体现在Django的代码中，其实就是model类的设计。

##### 一、数据库模型设计

作为一个用户登录和注册项目，需要保存的都是各种用户的相关信息。很显然，我们至少需要一张用户表User，在用户表里需要保存下面的信息：

- 用户名
- 密码
- 邮箱地址
- 性别
- 创建时间

进入`app01/models.py`文件，这里将是我们整个login应用中所有模型的存放地点，代码如下：

```python
from django.db import models

# Create your models here.
class User(models.Model):
	'''
	用户信息表
	'''
	gender = (
		('male',"男"),
		('female',"女"),
	)
	name = models.CharField(max_length=128,unique = True)
	password = models.CharField(max_length = 256)
	email =models.EmailField(unique=True)
	sex = models.CharField(max_length=32,choices=gender,default ="男")
	c_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
	class Meta:
		ordering = ['-c_time']
		verbose_name = "用户"    #就是给我们的模型起一个中文的名字
		verbose_name_plural = "用户"    #表示复数形式显示，如果不指定，django就会在我们的“用户”后面加一个s
		
```

各字段含义：

- name: 必填，最长不超过128个字符，并且唯一，也就是不能有相同姓名,这个姓名就相当于昵称，所以可以唯一。
- password: 必填，最长不超过256个字符（实际可能不需要这么长）；
- email: 使用Django内置的邮箱类型，并且唯一；
- sex: 性别，使用了一个choice，只能选择男或者女，默认为男；
- 使用`__str__`方法帮助人性化显示对象信息；
- 元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；

##### 二、设置数据库后端

定义好了模型后，就必须选择我们用来保存数据的数据库系统。Django支持Mysql，SQLite，Oracle等等。

Django中对数据库的设置在settings文件中，如下部分：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
Django默认使用SQLite数据库，并内置SQLite数据库的访问API，也就是说和Python一样原生支持SQLite。本项目使用SQLite作为后端数据库，因此不需要修改settings中这部分内容。如果你想要使用别的数据库，请自行修改该部分设置。
'''
```

##### 三、注册app

每次创建了新的app后，都需要在全局settings中注册，这样Django才知道你有新的应用上线了。在settings的下面部分添加‘login’，建议在最后添加个逗号。

```python
INSTALLED_APPS = [    'django.contrib.admin',    'django.contrib.auth',    'django.contrib.contenttypes',    'django.contrib.sessions',    'django.contrib.messages',    'django.contrib.staticfiles',    'app01.apps.App01Config', #这个就是django为我们自动配置的
 #'app01'， 如果django没有为我们配置我们可以这样配置            
]
```

##### 四、创建记录和数据表

app中的models建立好了后，并不会自动地在数据库中生成相应的数据表，需要你手动创建。

进入Pycharm的terminal终端，执行下面的命令：

```
python manage.py makemigrations  #创建User模型
python manage.py migrate    #创建真实的数据表
```

#### 3admin后台

在我们开发的初期，没有真实的用户数据，也没有完整的测试环境，为了测试和开发的方便，通常我们会频繁地使用Django给我们提供的Admin后台管理界面，创建测试用例，观察模型效果等等。

##### 一、在admin中注册模型

admin后台本质上是Django给我们提供的一个app，默认情况下，它已经在settings中注册了，如下所示的第一行！同样的还有session会话框架，后面我们会使用的。

```python
INSTALLED_APPS = [
    'django.contrib.admin',     # 看这里
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',      # 看这里
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
]
```

进入app01/admin.py文件，注册模型：

```python
from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.User)  #简单的注册模型
```

##### 二、创建超级管理员

Django的admin后台拥有完整的较为安全的用户认证和授权机制，防护等级还算可以。

同样在Pycharm的终端中，执行下面的命令：

```
python manage.py createsuperuser
```

然后输入用户名、邮箱（可以不输入）、密码（密码不能太简单）

##### 三、使用Admin后台

启动项目，访问127.0.0.1:8000/admin，输入我们的账号，进入管理界面：

![](http://9017499461.linshutu.top/admin.png)

注意，图中下方的`认证和授权`是admin应用自身的账户管理，上面的LOGIN栏目才是我们创建的login应用所对应的User模型。

点击右上方的增加用户按钮，我们创建几个测试用户试试：

![](http://9017499461.linshutu.top/admin2.png)

通过输入不同的数据，我们看到Email会有地址合法性检查，性别有个选择框，非常的人性化。

这里我随便创建了三个测试账号，如下所示：

![](http://9017499461.linshutu.top/admin3.png)

admin的使用和配置博大精深，但在本实战项目里，我们暂时把它当做一个数据库管理后台使用。

#### 4url路由和视图

前面我们已经创建好数据模型了，并且在admin后台中添加了一些测试用户。下面我们就要设计好站点的url路由、对应的处理视图函数以及使用的前端模板了。

##### 一、路由设计

我们初步设想需要下面的四个URL：

| URL        | 视图                 | 模板           | 说明 |
| ---------- | -------------------- | -------------- | ---- |
| /index/    | app01.views.index    | index.html     | 主页 |
| /login/    | app01.views.login    | login.html     | 登录 |
| /register/ | app01.views.register | register.html  | 注册 |
| /logout/   | app01.views.logout   | 无需专门的页面 | 登出 |

具体访问的策略如下：

- 未登录人员，不论是访问index还是login和logout，全部跳转到login界面
- 已登录人员，访问login会自动跳转到index页面
- 已登录人员，不允许直接访问register页面，需先logout
- 登出后，自动跳转到login界面

根据上面的策略，进入url.py文件，写如下代码：

```python
from django.contrib import admin
from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^login/$",views.login,name="login"),
    url(r"^index/$",views.index,name="index"),
    url(r"^register/$",views.register,name="register"),
    url(r"^logout/$",views.logout,name="logout"),
]
```

##### 二、架构初步视图

根据写好的路由系统，进入views.py文件编写视图框架：

```python
from django.shortcuts import render
from django.shortcuts import redirect,reverse

# Create your views here.
def login(request):
	"""
	登录视图
	:param request:
	:return:
	"""
	if reverse('/login/'):
		return render(request,'app01/login.html')

def index(request):
	"""
	主页视图
	:param request:
	:return:
	"""
	if reverse('/index/'):
		return render(request,'app01/index.html')

def register(request):
	"""
	注册视图
	:param request:
	:return:
	"""
	if reverse('/register/'):
		return render(request,'app01/register.html')

def logout(request):
	"""
	登出视图
	:param request:
	:return:
	"""
	if reverse('/logout/'):
		return render(request,'app01/login.html')
```

我们先不着急完成视图内部的具体细节，而是把框架先搭建起来。

##### 三、创建HTML页面文件

在项目根路径的app01目录中创建一个templates目录，再在templates目录里创建一个app01目录。这么做有助于app复用，防止命名冲突，能更有效地组织大型工程，具体说明请参考教程前面的相关章节。

在`app01/templates/app01`目录中创建三个文件`login.html`、`index.html`、以及`register.html` ，并写入如下的代码：

`login.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>
<h1>登录页面</h1>
</body>
</html>
```

`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
<h1>这仅仅是一个主页模拟！请根据实际情况接入正确的主页！</h1>
</body>
</html>
```

`register.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>注册</title>
</head>
<body>
<h1>注册页面</h1>
</body>
</html>
```

到目前为止，我们的工程目录结构如下图所示：

![](http://9017499461.linshutu.top/%E7%99%BB%E5%BD%95%E9%A1%B9%E7%9B%AE4.JPG)

##### 四、测试路由和视图

启动服务器，在浏览器访问`http://127.0.0.1:8000/index/`等页面，如果能正常显示，说明一切OK！

现在，我们整个项目的基本框架已经搭建起来了！

#### 5前端页面设计

##### 一、使用原生的HTML页面

login.html文件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>

    <div style="margin: 15% 40%;">
        <h1>欢迎登录！</h1>
       <form action="{% url "login" %}" method="post">
            <p>
                <label for="id_username">用户名：</label>
                <input type="text" id="id_username" name="username" placeholder="用户名" autofocus required />
            </p>
            <p>
                <label for="id_password">密码：</label>
                <input type="password" id="id_password" placeholder="密码" name="password" required >
            </p>
            <input type="submit" value="确定">
        </form>
    </div>

</body>
</html>
```

简单解释一下：

- form标签主要确定目的地url和发送方法；
- p标签将各个输入框分行；
- label标签为每个输入框提供一个前导提示，还有助于触屏使用；
- placeholder属性为输入框提供占位符；
- autofocus属性为用户名输入框自动聚焦
- required表示该输入框必须填写
- passowrd类型的input标签不会显示明文密码

**特别声明：所有前端的验证和安全机制都是不可信的，恶意分子完全可以脱离浏览器伪造请求数据！**

##### 二、引入Bootstrapt

上面的页面是完全的html纯文本的页面，是非常简陋的，现在引入前端框架，我们就可以定制很多自己想要的界面样式。

我们先导入网络链接形式的：

```html
//引入CSS样式：
<link href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
//引入JS代码：
<script src="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>
```

当然，我们也可以将他们下载到本地，然后把文件放到我们的静态文件夹中，然后从文件夹中导入进来也是可以的。

**由于Bootstrap依赖JQuery，所以我们也需要使用CDN引用JQuery 3.3.1**

```html
<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
```

**注意：另外，从Bootstrap4开始，额外需要popper.js的支持，依旧使用CDN的方式引入**

```html
<script src="https://cdn.bootcss.com/popper.js/1.15.0/umd/popper.js"></script>
```

使用漂亮的Bootstrapt4的样式重写login.html文件：

```html
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- 上述meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <!-- Bootstrap CSS -->
    <link href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <title>登录</title>
  </head>
  <body>
    <div class="container">
            <div class="col">
              <form class="form-login" action="{%   url "login" %}" method="post">
                  <h3 class="text-center">欢迎登录</h3>
                  <div class="form-group">
                    <label for="id_username">用户名：</label>
                    <input type="text" name='username' class="form-control" id="id_username" placeholder="Username" autofocus required>
                  </div>
                  <div class="form-group">
                    <label for="id_password">密码：</label>
                    <input type="password" name='password' class="form-control" id="id_password" placeholder="Password" required>
                  </div>
                <div>
                  <a href="{%   url "register" %}" class="text-success "><ins>新用户注册</ins></a>
                  <button type="submit" class="btn btn-primary float-right">登录</button>
                </div>
              </form>
            </div>
    </div> <!-- /container -->

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    {#    以下三者的引用顺序是固定的#}
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.15.0/umd/popper.js"></script>
    <script src="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>

  </body>
</html>
```

尽管现在的界面已经很漂亮了，但是我们觉得还是不够满意，那么我们就可以手动进行调整，怎么做呢？下面的就是

##### 三、添加静态文件

在工程根目录下的app01目录下，新建一个static目录，再到static目录里创建一个app01目录，这种目录的创建方式和模板文件mystatic的创建方式都是一样的思维，也就是让重用app变得可能，并且不和其它的app发生文件路径和名称上的冲突。

继续在`/app01/static/app01`目录下创建一个css和一个image目录，css中添加我们为登录视图写的css文件，这里是`app01.css`，image目录中，拷贝进来你想要的背景图片，这里是`bg.jpg`。

下面我们修改一下login.html的代码，主要是引入了login.css文件，注意最开头的load static ，表示我们要加载静态文件。

```html
{% load static %}
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- 上述meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <!-- Bootstrap CSS -->
    <link href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'login/css/login.css' %}" rel="stylesheet"/>
    <title>登录</title>
  </head>
  <body>
    <div class="container">
            <div class="col">
              <form class="form-login" action="{%   url "login" %}" method="post">
                  <h3 class="text-center">欢迎登录</h3>
                  <div class="form-group">
                    <label for="id_username">用户名：</label>
                    <input type="text" name='username' class="form-control" id="id_username" placeholder="Username" autofocus required>
                  </div>
                  <div class="form-group">
                    <label for="id_password">密码：</label>
                    <input type="password" name='password' class="form-control" id="id_password" placeholder="Password" required>
                  </div>
                  <div>
                  <a href="{%   url "register" %}" class="text-success "><ins>新用户注册</ins></a>
                  <button type="submit" class="btn btn-primary float-right">登录</button>
                  </div>
              </form>
            </div>
    </div> <!-- /container -->

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    {#    以下三者的引用顺序是固定的#}
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.15.0/umd/popper.js"></script>
    <script src="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>

  </body>
</html>
```

好了，现在可以重启服务器，刷新登录页面，看看效果了：

![](http://9017499461.linshutu.top/%E7%99%BB%E5%BD%95%E9%A1%B9%E7%9B%AE5.JPG)

#### 6登录视图

数据模型和前端页面我们都已经设计好了，是时候开始完善我们的登录视图具体内容了。

##### 一、登录视图

首先，我们处理用户名和密码登录：

```python
def login(request):
	"""
	登录视图
	:param request:
	:return:
	"""
	if reverse('login'):
		if request.method == "POST":
			username = request.POST.get("username")
			password = request.POST.get("password")
			return redirect('/index/')
		return render(request,'app01/login.html')
```

启动服务器，然后在`http://127.0.0.1:8000/login/`的表单中随便填入用户名和密码，然后点击提交。然而，页面却出现了错误提示，如下图所示：

![](http://9017499461.linshutu.top/%E7%99%BB%E5%BD%95%E9%A1%B9%E7%9B%AE6.png)

错误原因是CSRF验证失败，请求被中断。CSRF（Cross-site request forgery）跨站请求伪造，是一种常见的网络攻击手段，Django自带对许多常见攻击手段的防御机制，CSRF就是其中一种，还有XSS、SQL注入等。

解决这个问题的办法其实在Django的Debug错误页面已经给出了，我们需要在前端页面的form表单内添加一个csrf_token标签：

```html
                <form class="form-login" action="/login/" method="post">
                  {% csrf_token %}
                  <h3 class="text-center">欢迎登录</h3>
                  <div class="form-group">
                    <label for="id_username">用户名：</label>
                    <input type="text" name='username' class="form-control" id="id_username" placeholder="Username" autofocus required>
                  </div>
                  <div class="form-group">
                    <label for="id_password">密码：</label>
                    <input type="password" name='password' class="form-control" id="id_password" placeholder="Password" required>
                  </div>
                  <div>
                  <a href="/register/" class="text-success " ><ins>新用户注册</ins></a>
                  <button type="submit" class="btn btn-primary float-right">登录</button>
                  </div>
                </form>
```

这个标签必须放在form表单内部，但是内部的位置可以随意。

重新刷新login页面，确保csrf的标签生效，然后再次输入内容并提交。这次就可以成功地在Pycharm开发环境中看到接收的用户名和密码，同时浏览器页面也跳转到了首页。

##### 二、数据验证

前面我们提到过，要对用户发送的数据进行验证。数据验证分前端页面验证和后台服务器验证。前端验证可以通过专门的插件或者自己写JS代码实现，也可以简单地使用HTML5的新特性。这里，我们使用的是HTML5的内置验证功能。

它帮我们实现了下面的功能：

- 用户名和密码这类必填字段不能为空
- 密码部分用圆点替代

**前端页面的验证都是用来给守法用户做提示和限制的，并不能保证绝对的安全，后端服务器依然要重新对数据进行验证。我们现在的视图函数，没有对数据进行任何的验证，如果你在用户名处输入个空格，是可以正常提交的，但这显然是不允许的。甚至，如果跳过浏览器伪造请求，那么用户名是None也可以发送过来。通常，除了数据内容本身，我们至少需要保证各项内容都提供了且不为空，对于用户名、邮箱、地址等内容往往还需要剪去前后的空白，防止用户未注意到的空格。**

现在，让我们修改一下前面的代码：

```python
def login(request):
	"""
	登录视图
	:param request:
	:return:
	"""
	if reverse('login'):
		if request.method == "POST":
			username = request.POST.get("username")
			password = request.POST.get("password")
			if username.strip() and password.strip():  # 确保用户名和密码都不为空  
                #更多的验证自行定制
				return redirect('/index/')
		return render(request,'app01/login.html')
```

##### 三、验证用户名和密码

数据形式合法性验证通过了，不代表用户就可以登录了，因为最基本的密码对比还未进行。

**通过唯一的用户名，使用Django的ORM去数据库中查询用户数据，如果有匹配项，则进行密码对比，如果没有匹配项，说明用户名不存在。如果密码对比错误，说明密码不正确。**

现在再看看我们修改的views.py文件：

```python
def login(request):
	"""
	登录视图
	:param request:
	:return:
	"""
	if reverse('login'):
		if request.method == "POST":
			username = request.POST.get("username")
			password = request.POST.get("password")
			if username.strip() and password.strip():  # 确保用户名和密码都不为空
				try:
                    #这里为什么用try，就是因为get()这个方法很特别，它取数据库的数据，只有一个符合条件的就返回QuerySet对象，其他的情况都会报错，而我们的用户名（昵称）是唯一的，这样在匹配用户名的同时也进行了验证，一箭双雕
					user = models.User.objects.get(name=username)  
				except:
					return render(request,'app01/login.html')
				if user.password == password:
					return redirect('/index/')
		return render(request,'app01/login.html')
```

- 首先要在顶部导入models模块；
- 使用try异常机制，防止数据库查询失败的异常；
- 如果未匹配到用户，则执行except中的语句；注意这里没有区分异常的类型，因为在数据库访问过程中，可能发生很多种类型的异常，我们要对用户屏蔽这些信息，不可以暴露给用户，而是统一返回一个错误提示，比如用户名不存在。这是大多数情况下的通用做法。当然，如果你非要细分，也不是不行。
- `models.User.objects.get(name=username)`是Django提供的最常用的数据查询API，具体含义和用法可以阅读前面的章节，不再赘述；
- 通过`user.password == password`进行密码比对，成功则跳转到index页面，失败则返回登录页面。

##### 四、添加提示信息

上面的代码还缺少很重要的一部分内容，也就是错误提示信息！无论是登录成功还是失败，用户都没有得到任何提示信息，这显然是不行的。

修改一下login视图：

```python
def login(request):
	"""
	登录视图
	:param request:
	:return:
	"""
	if reverse('login'):
		if request.method == "POST":
			username = request.POST.get("username")
			password = request.POST.get("password")
			message = "请检查填写的内容！"
			if username.strip() and password.strip():  # 确保用户名和密码都不为空
				try:
					user = models.User.objects.get(name=username)
				except:
					message = "用户不存在！"
					return render(request,'app01/login.html',{"message":message})
				if user.password == password:
					return redirect('/index/')
				else:
					message = "密码不正确！"
					return render(request,'app01/login.html',{"message":message})
			else:
				return render(request, "app01/login.html", {"message": message})
		return render(request,'app01/login.html')
```

为了在前端页面显示信息，还需要对`login.html`进行修改：

```html
<form class="form-login" action="/login/" method="post">
                  {% if message %}
                    <div class="alert alert-warning">{{ message }}</div>
                  {% endif %}
                  {% csrf_token %}
                  <h3 class="text-center">欢迎登录</h3>
                  <div class="form-group">
                    <label for="id_username">用户名：</label>
                    <input type="text" name='username' class="form-control" id="id_username" placeholder="Username" autofocus required>
                  </div>
                  <div class="form-group">
                    <label for="id_password">密码：</label>
                    <input type="password" name='password' class="form-control" id="id_password" placeholder="Password" required>
                  </div>
                  <div>
                  <a href="/register/" class="text-success " ><ins>新用户注册</ins></a>
                  <button type="submit" class="btn btn-primary float-right">登录</button>
                  </div>
                </form>
```

好了，重启服务器，尝试用错误的和正确的用户名及密码登录，看看页面效果吧！

#### 7Django表单

**我们前面都是手工在HTML文件中编写表单form元素，然后在views.py的视图函数中接收表单中的用户数据，再编写验证代码进行验证，最后使用ORM进行数据库的增删改查。这样费时费力，整个过程比较复杂，而且有可能写得不太恰当，数据验证也比较麻烦。设想一下，如果我们的表单拥有几十上百个数据字段，有不同的数据特点，如果也使用手工的方式，其效率和正确性都将无法得到保障。有鉴于此，Django在内部集成了一个表单功能，以面向对象的方式，直接使用Python代码生成HTML表单代码，专门帮助我们快速处理表单相关的内容。**

##### 一、创建表单模型

在项目根目录的login文件夹下，新建一个`forms.py`文件，也就是`/app01/forms.py`，又是我们熟悉的Django组织文件的套路，一个app一套班子！

在`/app01/forms.py`中写入下面的代码，是不是有一种编写数据model模型的既视感？

```python
from django import forms

class UserName(forms.Form):
	username = forms.CharField(label="用户名",max_length=128,widget=forms.TextInput)
	password = forms.CharField(label="密码",max_length=256,widget=forms.PasswordInput)
```

说明：

- 顶部要先导入forms模块
- 所有的表单类都要继承forms.Form类
- 每个表单字段都有自己的字段类型比如CharField，它们分别对应一种HTML语言中`<form>`内的一个input元素。这一点和Django模型系统的设计非常相似。
- label参数用于设置`<label>`标签
- `max_length`限制字段输入的最大长度。它同时起到两个作用，一是在浏览器页面限制用户输入不可超过字符数，二是在后端服务器验证用户输入的长度也不可超过。
- `widget=forms.PasswordInput`用于指定该字段在form表单里表现为`<input type='password' />`，也就是密码输入框。

##### 二、修改视图

使用了Django的表单后，就要在视图中进行相应的修改：

```python
from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect,reverse
from . import models
from . import forms
# Create your views here.
def login(request):
	"""
	登录视图
	:param request:
	:return:
	"""
	if reverse('login'):
		if request.method == "POST":
			login_form = forms.UserName(request.POST)
			message = "请检查填写的内容！"
			if login_form:
				username = request.POST.get("username")
				password = request.POST.get("password")
				try:
					user = models.User.objects.get(name=username)
				except:
					return render(request,'app01/login.html',locals())
				if user.password == password:
					return redirect('/index/')
				else:
					message = "用户名或密码不正确！"
					return render(request,'app01/login.html',locals())
			else:
				return render(request, "app01/login.html", locals())
        login_form = forms.UserForm()
		return render(request,'app01/login.html',locals())
```

说明：

- 在顶部要导入我们写的forms模块:`from . import forms`
- 对于非POST方法发送数据时，比如GET方法请求页面，返回空的表单，让用户可以填入数据；
- 对于POST方法，接收表单数据，并验证；
- 使用表单类自带的`is_valid()`方法一步完成数据验证工作；
- 验证成功后可以从表单对象的`cleaned_data`数据字典中获取表单的具体值；
- 如果验证不通过，则返回一个包含先前数据的表单给前端页面，方便用户修改。也就是说，它会帮你保留先前填写的数据内容，而不是返回一个空表！

另外，这里使用了一个小技巧，Python内置了一个locals()函数，它返回当前所有的本地变量字典，我们可以偷懒的将这作为render函数的数据字典参数值，就不用费劲去构造一个形如`{'message':message, 'login_form':login_form}`的字典了。这样做的好处当然是大大方便了我们，但是同时也可能往模板传入了一些多余的变量数据，造成数据冗余降低效率。

##### 三、修改login页面

Django的表单很重要的一个功能就是自动生成HTML的form表单内容。现在，我们需要修改一下原来的`login.html`文件：

```html
{% load static %}
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- 上述meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <!-- Bootstrap CSS -->
    <link href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'app01/css/app01.css' %}" rel="stylesheet"/>
    <title>登录</title>
  </head>
  <body>
    <div class="container">
            <div class="col">
              <form class="form-login" action="{%   url "login" %}" method="post">
                  {% if message %}
                        <div class="alert alert-warning">{{ message }}</div>
                  {% endif %}
                  {%  csrf_token %}
                  <h3 class="text-center">欢迎登录</h3>
                                   {{ login_form }}

                  <div>
                      <a href="{% url "register" %}" class="text-success " ><ins>新用户注册</ins></a>
                      <button type="submit" class="btn btn-primary float-right">登录</button>
                  </div>
              </form>
            </div>
    </div> <!-- /container -->

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    {#    以下三者的引用顺序是固定的#}
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.15.0/umd/popper.js"></script>
    <script src="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>

  </body>
</html>
```

说明：

- 你没有看错！一个 login_form 就直接完成了表单内容的生成工作！`login_form`这个名称来自你在视图函数中生成的form实例的变量名！
- 但是，它不会生成`<form>...</form>`标签，这个要自己写；
- 使用POST的方法时，必须添加 csrf_token %标签，用于处理csrf安全机制；
- Django自动为每个input元素设置了一个id名称，对应label的for参数
- 注册链接和登录按钮需要自己写，Django不会帮你生成！

上面的 login_form为我们生成了下面的代码：

```html
<tr><th><label for="id_username">用户名:</label></th><td><input type="text" name="username" maxlength="128" required id="id_username"></td></tr> 
<tr><th><label for="id_password">密码:</label></th><td><input type="password" name="password" maxlength="256" required id="id_password"></td></tr> 
```

这看起来好像一个`<table>`标签啊？没错，就是`<table>`标签，而且是不带`<table></table>`的，捂脸！

- ```
  实际上除了通过`{{ login_form }}`简单地将表单渲染到HTML页面中了，还有下面几种方式：
  
  - `{{ login_form.as_table }}` 将表单渲染成一个表格元素，每个输入框作为一个`<tr>`标签
  - `{{ login_form.as_p }}` 将表单的每个输入框包裹在一个`<p>`标签内
  - `{{ login_form.as_ul }}` 将表单渲染成一个列表元素，每个输入框作为一个`<li>`标签
  ```

##### 四、手动渲染表单字段

直接login_form 虽然好，啥都不用操心，但是界面真的很丑，并且我们先前使用的Bootstraps4都没了。因为这些都需要对表单内的input元素进行额外控制，那怎么办呢？手动渲染字段就可以了！

可以通过login_form.name_of_field 获取每一个字段，然后分别渲染，如下例所示：

```html
<div class="form-group">
  {{ login_form.username.label_tag }}
  {{ login_form.username}}
</div>
<div class="form-group">
  {{ login_form.password.label_tag }}
  {{ login_form.password }}
</div>
```

好像Bootstrap4没有生效呀！仔细查看最终生成的页面源码，你会发现，input元素里少了`form-control`的class，以及placeholder和autofocus，这可咋办？

在form类里添加attr属性即可，如下所示修改`login/forms.py`

```python
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))
```

再次刷新页面，我们熟悉的Bootstrap4框架UI又回来了！

![](http://9017499461.linshutu.top/%E7%99%BB%E5%BD%95%E9%A1%B9%E7%9B%AE5.JPG)

**注意：表单系统其实很简单，为我们省下了不少的功夫，但是也有很多的不足，我推荐大家基于中小型的系统大家还是自己来设计表单的内容，安全控制的都自己加上去**

#### 8图片验证码

验证码（CAPTCHA）是“Completely Automated Public Turing test to tell Computers and Humans Apart”（全自动区分计算机和人类的图灵测试）的缩写，是一种区分用户是计算机还是人的公共全自动程序。可以防止恶意破解密码、刷票、论坛灌水，有效防止某个黑客对某一个特定注册用户用特定程序暴力破解方式进行不断的登陆尝试。

图形验证码的历史比较悠久，到现在已经有点英雄末路的味道了。因为机器学习、图像识别的存在，机器人已经可以比较正确的识别图像内的字符了。但不管怎么说，作为一种防御手段，至少还是可以抵挡一些低级入门的攻击手段，抬高了攻击者的门槛。

在Django中实现图片验证码功能非常简单，有现成的第三方库可以使用，我们不必自己开发（也要能开发得出来，囧）。这个库叫做`django-simple-captcha`。

##### 一、安装captcha

```
执行命令：pip install django-simple-captcha
```

pip自动帮我们安装了相关的依赖库`six`、`olefile`和`Pillow`，其中的Pillow是大名鼎鼎的绘图模块。

##### 二、注册captcha

在settings中，将‘captcha’注册到app列表里：

```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'captcha',
]
```

captcha需要在数据库中建立自己的数据表，所以需要执行migrate命令生成数据表：

```
makemigrations
migrate
```

##### 三、添加url路由

在根目录下的urls.py文件中增加captcha对应的url：

```python
from django.contrib import admin
from django.conf.urls import url,include
from app01 import views

urlpatterns = [
    url(f"^captcha/",include('captcha.urls')), # 增加这一行
]
```

##### 四、修改forms.py

如果上面都OK了，就可以直接在我们的forms.py文件中添加CaptchaField了。

```python
from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control',  'placeholder': "Password"}))
    captcha = CaptchaField(label='验证码')
```

##### 五、修改login.html

由于我们前面是手动生成的form表单，所以还要修改一下，添加captcha的相关内容，如下所示：

```html
{% load static %}
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- 上述meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <!-- Bootstrap CSS -->
    <link href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'app01/css/app01.css' %}" rel="stylesheet"/>
    <title>登录</title>
  </head>
  <body>
    <div class="container">
            <div class="col">
              <form class="form-login" action="{%   url "login" %}" method="post">
                  {% if login_form.captcha.errors %}
                    <div class="alert alert-warning">{{ login_form.captcha.errors }}</div>
                  {% elif message %}
                    <div class="alert alert-warning">{{ message }}</div>
                  {% endif %}

                  {%  csrf_token %}

                  <h3 class="text-center">欢迎登录</h3>

                  <div class="form-group">
                    {{ login_form.username.label_tag }}
                    {{ login_form.username}}
                  </div>

                  <div class="form-group">
                    {{ login_form.password.label_tag }}
                    {{ login_form.password }}
                  </div>

                  <div class="form-group">
                    {{ login_form.captcha.label_tag }}
                    {{ login_form.captcha }}
                  </div>

                  <div>
                      <a href="{% url "register" %}" class="text-success " ><ins>新用户注册</ins></a>
                      <button type="submit" class="btn btn-primary float-right">登录</button>
                  </div>
              </form>
            </div>
    </div> <!-- /container -->

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    {#    以下三者的引用顺序是固定的#}
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.15.0/umd/popper.js"></script>
    <script src="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>

  </body>
</html>
```

```
这里在顶部的消息处，在`{% if %}`模板代码中，额外增加了一条`{{ login_form.captcha.errors }}`的判断，用于明确指示用户的验证码不正确。
```

##### 六、查看效果

重启服务器，进入登录页面，尝试用用户名错误、密码不对、验证码不对、全对的不同情况，看看我们新增的四位验证码的效果如何。

![](http://9017499461.linshutu.top/%E7%99%BB%E5%BD%95%E9%A1%B9%E7%9B%AE7.JPG)

其中验证图形码是否正确的工作都是在后台自动完成的，只需要使用`is_valid()`这个forms内置的验证方法就一起进行了，完全不需要在视图函数中添加任何的验证代码，非常方便快捷！

关于captcha的功能，当然绝不仅限于此，你可以设置六位、八位验证码，可以对图形噪点的生成模式进行定制，这些就留待你自己学习和研究了。

#### 9session会话

因为因特网HTTP协议的特性，每一次来自于用户浏览器的请求（request）都是无状态的、独立的。通俗地说，就是无法保存用户状态，后台服务器根本就不知道当前请求和以前及以后请求是否来自同一用户。对于静态网站，这可能不是个问题，而对于动态网站，尤其是京东、天猫、银行等购物或金融网站，无法识别用户并保持用户状态是致命的，根本就无法提供服务。你可以尝试将浏览器的cookie功能关闭，你会发现将无法在京东登录和购物。

为了实现连接状态的保持功能，网站会通过用户的浏览器在用户机器内被限定的硬盘位置中写入一些数据，也就是所谓的Cookie。通过Cookie可以保存一些诸如用户名、浏览记录、表单记录、登录和注销等各种数据。但是这种方式非常不安全，因为Cookie保存在用户的机器上，如果Cookie被伪造、篡改或删除，就会造成极大的安全威胁，因此，**现代网站设计通常将Cookie用来保存一些不重要的内容，实际的用户数据和状态还是以Session会话的方式保存在服务器端。**

但是，必须清楚的是**Session依赖Cookie**！不同的地方在于Session将所有的数据都放在服务器端，用户浏览器的Cookie中只会保存一个非明文的识别信息，比如哈希值。

Django提供了一个通用的Session框架，并且可以使用多种session数据的保存方式：

- 保存在数据库内
- 保存到缓存
- 保存到文件内
- 保存到cookie内

通常情况，没有特别需求的话，请使用保存在数据库内的方式，尽量不要保存到Cookie内。

Django的session框架默认启用。

##### 一、使用session

首先，修改`app01/views.py`中的login()视图函数：

```python
def login(request):
	"""
	登录视图
	:param request:
	:return:
	"""
	if request.session.get('is_login',None):  #不允许重复登录
		return redirect('/index/')
	if reverse('login'):
		if request.method == "POST":
			login_form = forms.UserForm(request.POST)
			message = "请检查填写的内容！"
			if login_form:
				username = request.POST.get("username")
				password = request.POST.get("password")
				try:
					user = models.User.objects.get(name=username)
				except:
					return render(request,'app01/login.html',locals())
				if user.password == password:
					request.session['is_login'] = True
					request.session['user_id'] = user.id
					request.POST.session['user_name'] = user.name
					return redirect('/index/')
				else:
					message = "用户名或密码不正确！"
					return render(request,'app01/login.html',locals())
			else:
				return render(request, "app01/login.html", locals())
		login_form = forms.UserForm()
		return render(request,'app01/login.html',locals())
```

说明：

通过下面的if语句，我们不允许重复登录：

```python
if request.session.get('is_login',None):
    return redirect("/index/")
```

通过下面的语句，我们往session字典内写入用户状态和数据：

```python
request.session['is_login'] = True
request.session['user_id'] = user.id
request.session['user_name'] = user.name
```

你完全可以往里面写任何数据，不仅仅限于用户相关！

既然有了session记录用户登录状态，那么就可以完善我们的登出视图函数了：

```python
def logout(request):
	"""
	登出视图
	:param request:
	:return:
	"""
	if reverse('logout'):
		if not request.session.get("is_login",None):   #get没有值返回None
			return redirect('/login/')
		#这个方法就是当我们登出的时候，清除我们在后台保留的session值，这样下次我们再登录的时候就是新的状态，同时再次设置新的session值
		request.session.flush()
		#当然，我们也可以使用下面的方式
		# del request.session['is_login']
		# del request.session['user_id']
		# del request.session['user_name']
		return redirect("/login/")
```

flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。但也有不好的地方，那就是如果你在session中夹带了一点‘私货’，会被一并删除，这一点一定要注意。

##### 二、在index页面中验证登录

有了用户状态，就可以根据用户登录与否，展示不同的页面，比如在index页面中显示当前用户的名称：

修改index.html的代码：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
<h1>{{ request.session.user_name }}!  欢迎回来！</h1>
<p>
    <a href="{% url "login" %}">登出</a>
</p>
</body>
</html>
```

```
**注意其中的模板语言，`{{ request }}`这个变量会被默认传入模板中，可以通过圆点的调用方式，获取它内部的`{{ request.session }}`，再进一步的获取session中的内容。其实`{{ request }}`中的数据远不止此，例如`{{ request.path }}`就可以获取先前的url地址。**

```

修改index视图函数，添加相关限制：

```python
def logout(request):
	"""
	登出视图
	:param request:
	:return:
	"""
	if reverse('logout'):
		if not request.session.get("is_login",None):   #get没有值返回None
			return redirect('/login/')
		#这个方法就是当我们登出的时候，清除我们在后台保留的session值，这样下次我们再登录的时候就是新的状态，同时再次设置新的session值
		request.session.flush()
		#当然，我们也可以使用下面的方式
		# del request.session['is_login']
		# del request.session['user_id']
		# del request.session['user_name']
		return redirect("/login/")

```

#### 10注册视图

前面我们已经完成了项目大部分内容，现在还剩下重要的注册功能没有实现。

##### 一、创建forms

显而易见，我们的注册页面也需要一个form表单。同样地，在`/app01/forms.py`中添加一个新的表单类：

```python
class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')
```

说明：

- gender字典和User模型中的一样，其实可以拉出来作为常量共用，为了直观，特意重写一遍；
- password1和password2，用于输入两遍密码，并进行比较，防止误输密码；
- email是一个邮箱输入框；
- sex是一个select下拉框；
- 没有添加更多的input属性

##### 二、完善register.html

同样地，类似login.html文件，我们手工在register.html中编写forms相关条目：

```html
{% load static %}
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- 上述meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <!-- Bootstrap CSS -->
    <link href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <link href="{% static 'app01/css/register.css' %}" rel="stylesheet"/>
    <title>注册</title>
  </head>
  <body>
    <div class="container">
            <div class="col">
                <form class="form-register" action="{% url 'register' %}" method="post">

                    {% if register_form.captcha.errors %}
                        <div class="alert alert-warning">{{ register_form.captcha.errors }}</div>
                    {% elif message %}
                        <div class="alert alert-warning">{{ message }}</div>
                    {% endif %}

                  {% csrf_token %}
                  <h3 class="text-center">欢迎注册</h3>

                  <div class="form-group">
                      {{ register_form.username.label_tag }}
                      {{ register_form.username}}
                  </div>
                  <div class="form-group">
                      {{ register_form.password1.label_tag }}
                      {{ register_form.password1 }}
                  </div>
                  <div class="form-group">
                      {{ register_form.password2.label_tag }}
                      {{ register_form.password2 }}
                  </div>
                  <div class="form-group">
                      {{ register_form.email.label_tag }}
                      {{ register_form.email }}
                  </div>
                  <div class="form-group">
                      {{ register_form.sex.label_tag }}
                      {{ register_form.sex }}
                  </div>
                  <div class="form-group">
                      {{ register_form.captcha.label_tag }}
                      {{ register_form.captcha }}
                  </div>

                  <div>
                      <a href="{% url "login" %}"  ><ins>直接登录</ins></a>
                      <button type="submit" class="btn btn-primary float-right">注册</button>
                  </div>
                </form>
            </div>
    </div> <!-- /container -->

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    {#    以下三者的引用顺序是固定的#}
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
    <script src="https://cdn.bootcss.com/popper.js/1.15.0/umd/popper.js"></script>
    <script src="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>

  </body>
</html>

```

需要注意的是：

- 编写了一个register.css样式文件
- form标签的action地址为`/register/`，class为`form-register`
- from中传递过来的表单变量名字为`register_form`
- 最下面的链接修改为直接登录的链接

register.css样式文件的代码很简单，如下所示：

```css
body {
  height: 100%;
  background-image: url('../image/bg.jpg');
}
.form-register {
  width: 100%;
  max-width: 400px;
  padding: 15px;
  margin: 0 auto;
}
.form-group {
  margin-bottom: 5px;
}
form a{
  display: inline-block;
  margin-top:25px;
  line-height: 10px;
}

```

##### 三、实现注册视图

进入`/app01/views.py`文件，现在来完善我们的`register()`视图：

```python
def register(request):
	"""
	注册视图
	:param request:
	:return:
	"""
	if reverse('register'):
		if request.session.get("is_login",None):
			return redirect('/index/')
		if request.method == "POST":
			register_form = forms.RegisterForm(request.POST)
			message = "请检查填写的内容！"
			if register_form.is_valid():    #判断表单的数据是否合法，返回一个布尔值
				username = register_form.cleaned_data.get('username')
				password1 = register_form.cleaned_data.get('password1')
				password2 = register_form.cleaned_data.get('password2')
				email = register_form.cleaned_data.get('email')
				sex = register_form.cleaned_data.get('sex')

				if password1 != password2:
					message = '两次输入的密码不同！'
					return render(request, 'app01/register.html', locals())
				else:
					same_name_user = models.User.objects.filter(name=username)
					if same_name_user:
						message = '用户名已经存在'
						return render(request, 'app01/register.html', locals())
					same_email_user = models.User.objects.filter(email=email)
					if same_email_user:
						message = '该邮箱已经被注册了！'
						return render(request, 'app01/register.html', locals())
					new_user = models.User()
					new_user.name = username
					new_password = password1
					new_email = email
					new_sex = sex
					new_user.save()

					return redirect('/login/')
			else:
				return render(request, 'app01/register.html', locals())
		register_form = forms.RegisterForm()
		return render(request,'app01/register.html',locals())

```

从大体逻辑上，也是先实例化一个RegisterForm的对象，然后使用`is_valide()`验证数据，再从`cleaned_data`中获取数据。

让我们看一下注册的页面：

![](http://9017499461.linshutu.top/%E7%99%BB%E5%BD%95%E9%A1%B9%E7%9B%AE8.JPG)

##### 四、密码加密

等等！我们好像忘了什么！我们到现在都还一直在用明文的密码！

对于如何加密密码，有很多不同的途径，其安全程度也高低不等。这里我们使用Python内置的hashlib库，使用哈希值的方式加密密码，可能安全等级不够高，但足够简单，方便使用，不是么？

首先在`login/views.py`中编写一个hash函数：

```python
import hashlib

def hash_code(s, salt='LogAndReg'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

```

然后，我们还要对login()和register()视图进行一下修改：

```python
from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect,reverse
import hashlib
from . import models
from . import forms
# Create your views here.
def hash_code(s, salt='mysite'):
	h = hashlib.sha256()
	s += salt
	h.update(s.encode())
	return h.hexdigest()

def login(request):
	"""
	登录视图
	:param request:
	:return:
	"""
	if request.session.get('is_login',None):  #不允许重复登录
		return redirect('/index/')
	if reverse('login'):
		if request.method == "POST":
			login_form = forms.UserForm(request.POST)
			message = "请检查填写的内容！"
			if login_form.is_valid():
				username = login_form.cleaned_data.get("username")
				password = login_form.cleaned_data.get("password")
				try:
					user = models.User.objects.get(name=username)
				except:
					return render(request,'app01/login.html',locals())
				if user.password == hash_code(password):
					request.session['is_login'] = True
					request.session['user_id'] = user.id
					request.session['user_name'] = user.name
					return redirect('/index/')
				else:
					message = "用户名或密码不正确！"
					return render(request,'app01/login.html',locals())
			else:
				return render(request, "app01/login.html", locals())
		login_form = forms.UserForm()
		return render(request,'app01/login.html',locals())

def index(request):
	"""
	主页视图
	:param request:
	:return:
	"""
	if reverse('index'):
		if not request.session.get("is_login",None):
			return redirect("/login/")
		return render(request,'app01/index.html')

def register(request):
	"""
	注册视图
	:param request:
	:return:
	"""
	if reverse('register'):
		if request.session.get("is_login",None):
			return redirect('/index/')
		if request.method == "POST":
			register_form = forms.RegisterForm(request.POST)
			message = "请检查填写的内容！"
			if register_form.is_valid():    #判断表单的数据是否合法，返回一个布尔值
				username = register_form.cleaned_data.get('username')
				password1 = register_form.cleaned_data.get('password1')
				password2 = register_form.cleaned_data.get('password2')
				email = register_form.cleaned_data.get('email')
				sex = register_form.cleaned_data.get('sex')

				if password1 != password2:
					message = '两次输入的密码不同！'
					return render(request, 'app01/register.html', locals())
				else:
					same_name_user = models.User.objects.filter(name=username)
					if same_name_user:
						message = '用户名已经存在'
						return render(request, 'app01/register.html', locals())
					same_email_user = models.User.objects.filter(email=email)
					if same_email_user:
						message = '该邮箱已经被注册了！'
						return render(request, 'app01/register.html', locals())
					new_user = models.User()
					new_user.name = username
					new_password = hash_code(password1)
					new_email = email
					new_sex = sex
					new_user.save()

					return redirect('/login/')
			else:
				return render(request, 'app01/register.html', locals())
		register_form = forms.RegisterForm()
		return render(request,'app01/register.html',locals())

def logout(request):
	"""
	登出视图
	:param request:
	:return:
	"""
	if reverse('logout'):
		if not request.session.get("is_login",None):   #get没有值返回None
			return redirect('/login/')
		#这个方法就是当我们登出的时候，清除我们在后台保留的session值，这样下次我们再登录的时候就是新的状态，同时再次设置新的session值
		request.session.flush()
		#当然，我们也可以使用下面的方式
		# del request.session['is_login']
		# del request.session['user_id']
		# del request.session['user_name']
		return redirect("/login/")
```

好了，我们可以来验证一下了!但是，**请先在admin后台里，把我们前面创建的测试用户全部删除！**因为它们的密码没有使用哈希算法加密，已经无效了。

**可以看到密码长度根据你哈希算法的不同，已经变得很长了，所以前面model中设置password字段时，不要想当然的将`max_length`设置为16这么小的数字。**

#### 11Django发送邮件

通常而言，我们在用户注册成功，实际登陆之前，会发送一封电子邮件到对方的注册邮箱中，表示欢迎。进一步的还可能要求用户点击邮件中的链接，进行注册确认。

下面就让我们先看看如何在Django中发送邮件吧。

##### 一、在Django中发送邮件

其实在Python中已经内置了一个smtp邮件发送模块，Django在此基础上进行了简单地封装。

首先，我们需要在项目的settings文件中配置邮件发送参数，分别如下

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xxx@sina.com'  #自己的邮箱账号
EMAIL_HOST_PASSWORD = 'xxxxxxxxxxx'  #开启stmp之后人家给你的密码

```

- 第一行指定发送邮件的后端模块，大多数情况下照抄！
- 第二行，不用说，发送方的smtp服务器地址，建议使用新浪家的；
- 第三行，smtp服务端口，默认为25；
- 第四行，你在发送服务器的用户名；
- 第五行，对应用户的密码。

##### 二、创建模型

既然要区分通过和未通过邮件确认的用户，那么必须给用户添加一个是否进行过邮件确认的属性。

另外，我们要创建一张新表，用于保存用户的确认码以及注册提交的时间。

全新、完整的`/app01/models.py`文件如下：

```python
from django.db import models

# Create your models here.
class User(models.Model):
	'''
	用户信息表
	'''
	gender = (
		('male',"男"),
		('female',"女"),
	)
	name = models.CharField(max_length=128,unique = True)
	password = models.CharField(max_length = 256)
	email =models.EmailField(unique=True)
	sex = models.CharField(max_length=32,choices=gender,default ="男")
	c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

	def __str__(self):
		return self.name
	class Meta:
		ordering = ['-c_time']
		verbose_name = "用户"    #就是给我们的模型起一个中文的名字
		verbose_name_plural = "用户"    #表示复数形式显示，如果不指定，django就会在我们的“用户”后面加一个s

class ConfirmString(models.Model):
	code = models.CharField(max_length=256)
	user = models.OneToOneField('User', on_delete=models.CASCADE)
	c_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.name + ":   " + self.code

	class Meta:
		ordering = ["-c_time"]
		verbose_name = "确认码"
		verbose_name_plural = "确认码"
```

- User模型新增了`has_confirmed`字段，这是个布尔值，默认为False，也就是未进行邮件注册；
- ConfirmString模型保存了用户和注册码之间的关系，一对一的形式；
- code字段是哈希后的注册码；
- user是关联的一对一用户；
- `c_time`是注册的提交时间。

这里有个问题可以讨论一下：是否需要创建ConfirmString新表？可否都放在User表里？我认为如果全都放在User中，不利于管理，查询速度慢，创建新表有利于区分已确认和未确认的用户。最终的选择可以根据你的实际情况具体分析。

模型修改和创建完毕，需要执行migrate命令，一定不要忘了。

顺便修改一下admin.py文件，方便我们在后台修改和观察数据

```python
from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.User)
admin.site.register(models.ConfirmString)

```

##### 三、修改视图

首先，要修改我们的`register()`视图的逻辑：

```python
#在new_user.save()后面添加
	code = make_confirm_string(new_user)
	send_email(email, code)

	message = '请前往邮箱进行确认！'
	return render(request, 'login/confirm.html', locals())

```

`make_confirm_string()`是创建确认码对象的方法，代码如下：

```python
import datatime

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code

```

`make_confirm_string()`方法接收一个用户对象作为参数。首先利用datetime模块生成一个当前时间的字符串now，再调用我们前面编写的`hash_code()`方法以用户名为基础，now为‘盐’，生成一个独一无二的哈希值，再调用ConfirmString模型的create()方法，生成并保存一个确认码对象。最后返回这个哈希值。

`send_email(email, code)`方法接收两个参数，分别是注册的邮箱和前面生成的哈希值，代码如下：

```python
from django.conf import settings

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.liujiangblog.com的注册确认邮件'

    text_content = '''感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

```

邮件内容中的所有字符串都可以根据你的实际情况进行修改。其中关键在于`<a href=''>`中链接地址的格式，我这里使用了硬编码的'127.0.0.1:8000'，请酌情修改，url里的参数名为`code`，它保存了关键的注册确认码，最后的有效期天数为设置在settings中的`CONFIRM_DAYS`。所有的这些都是可以定制的！

下面是邮件相关的settings配置：

```python
# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xxx@sina.com'
EMAIL_HOST_PASSWORD = 'xxxxxx'

# 注册有效期天数
CONFIRM_DAYS = 7

```

##### 四、处理确认邮件

首先，在根目录的`urls.py`中添加一条url：

```python
path('confirm/', views.user_confirm),

```

其次，在`login/views.py`中添加一个`user_confirm`视图。

```python
def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals()

```

说明：

- 通过`request.GET.get('code', None)`从请求的url地址中获取确认码;
- 先去数据库内查询是否有对应的确认码;
- 如果没有，返回`confirm.html`页面，并提示;
- 如果有，获取注册的时间`c_time`，加上设置的过期天数，这里是7天，然后与现在时间点进行对比；
- 如果时间已经超期，删除注册的用户，同时注册码也会一并删除，然后返回`confirm.html`页面，并提示;
- 如果未超期，修改用户的`has_confirmed`字段为True，并保存，表示通过确认了。然后删除注册码，但不删除用户本身。最后返回`confirm.html`页面，并提示。

这里需要一个`confirm.html`页面，我们将它创建在`/app01/templates/app01/`下面：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>注册确认</title>
</head>
<body>
    <h1 style="margin-left: 100px;">{{ message }}</h1>

    <script>
        window.setTimeout("window.location='/login/'",2000);
    </script>

</body>
</html>

```

页面中通过JS代码，设置2秒后自动跳转到登录页面。

confirm.html页面仅仅是个示意的提示页面，你可以根据自己的需要去除或者美化。

##### 五、修改登录规则

既然未进行邮件确认的用户不能登录，那么我们就必须修改登录规则，如下所示：

```python
#在except下面添加：
if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login/login.html', locals())

```

关于邮件注册，还有很多内容可以探讨，比如定时删除未在有效期内进行邮件确认的用户，这个可以用Django的celery实现，或者使用Linux的cronb功能。

关于邮件注册的工作逻辑，项目里只是抛砖引玉，做个展示，并不够严谨，也需要你自己根据实际环境去设计。

最后，其实Django生态圈有一个现成的邮件注册模块django-registration，但是这个模块灵活度不高，并且绑定了Auth框架，有兴趣的可以去看看其英文文档，中文资料较少。

至此！一切完成！

#### 12Githun管理项目

项目介绍到这里，基本就结束了，可对于真正的业务开发，还只是刚开始。

不管是对于教程代码免费分享的需要，还是项目开发过程中的版本管理，Github都是我们首选的开源代码仓库，如果你没有私有仓库，并且不用保护代码，那么将项目上传到Github上是最佳的选择。

##### 一、创建requirements.txt文件

`requirements.txt`文件是一个项目的依赖文件，可以通过下面的方式自动生成：

进入虚拟环境，切换到项目根目录下，使用pip工具的freeze参数。

```py
(venv) D:\work\2019\for_test\mysite>pip freeze > ./requirements.t

```

他人如果拷贝了我们的代码，要安装第三方库依赖的话，只需要：

```
pip install -r requirements.txt
```

就可以一次性安装好所有的库了。

##### 二、创建.gitignore文件

在项目代码中，有一些文件是不能上传的，比如密码文件、数据库文件、核心配置文件等等，还有一些是不用上传的，比如临时文件。为了让git自动忽略这些文件，我们需要创建一个忽略名单。

在项目根目录下新建一个`.gitignore`文件，这里可能需要你在Pycharm下安装ignore插件，如下图所示：

![](http://9017499461.linshutu.top/%E7%99%BB%E9%99%86%E9%A1%B9%E7%9B%AE9.png)

我这里是已经安装好了，新安装的话，要在搜索栏里搜索到插件后再安装。

在`.gitignore`文件里写入下面的内容：

```
.gitignore
venv
.idea
settings.py
db.sqlite3
mysite/__pycache__/

```

这些文件将不会上传到Github中，也不会进行版本管理。

##### 三、特殊文件处理

对于settings.py文件有个问题，如果没有这个文件是无法运行Django项目的，但是settings中又可能包含很多关键的不可泄露的部分，比如SECRET_KEY：

```
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b(&6i_$g2%8vh)ruu$)a9pkw+s-e&qj_e_#=@gnbo^48#gp_8a'

```

还有数据库的IP/Port、用户名和密码，邮件发送端的用户名和密码，这些都是绝对不能泄露的。

那怎么办呢？简单！复制settings文件，并重命名为settings.example.py文件，放在同一目录里，把敏感信息、密码等修改或删除。使用者看到这个文件名，自然会明白它的作用。

##### 四、添加说明文件和许可文件

通常我们要给Github的仓库添加说明文件和许可文件。

在项目根目录下创建一个`README.md`文件，这是markdown格式的。在文件里写入项目说明，使用方法，注意事项等等所有你认为需要说明的东西。

```python
## 这是一个用户登录和注册教学项目
## 这是一个可重用的登录和注册APP
## 该项目教程发布在www.liujiangblog.com

## 简单的使用方法：


创建虚拟环境
使用pip安装第三方依赖
修改settings.example.py文件为settings.py
运行migrate命令，创建数据库和数据表
运行python manage.py runserver启动服务器


路由设置：


from django.contrib import admin
from django.urls import path, include
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('confirm/', views.user_confirm),
    path('captcha/', include('captcha.urls'))   # 增加这一行
]
```

对于许可文件`LICENSE`，如果你暂时不想公开授权，或者不知道用哪种授权，可以暂时不提供。

下面是一个APACHE2.0授权的范例：

```
   mysite - User login and register system

   Copyright 2019- www.liujiangblog.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```

##### 五、上传代码

这里我们将项目上传到github中，并取名为login-register。

在上传过程中，确认文件列表的时候，一定要注意查看没有保密文件被上传。

具体流程：https://blog.csdn.net/Jasonmes/article/details/80798227

### 重用app

http://www.liujiangblog.com/course/django/277



