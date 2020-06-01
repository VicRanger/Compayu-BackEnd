# Compayu-BackEnd

直真我来了！！！
飞哥我来了！！！

### 数据库定义指南
#### 指定Router
在`backsite/backsite/settings.py`中找到`DATABASE_APPS_MAPPING`，如果你的`app`定义的`config`中的`name`为`xxx`，加入一条`'xxx':'db_compayu'`。
#### 迁移命令
`$app_name`为迁移的`APPConfig`中的`name`，`$db_name`为`$app_name`对应的数据库名。
```
shell> python manage.py makemigrations $app_name
shell> python manage.py migrate $app_name --database=$db_name
```
执行完上述两条即可完成数据库建立。

hints：makemigrations命令对所有模型都会作用，只会生成迁移规则，不会真的应用，migrate是真的建立数据表，但是会按照一定规则过滤，不满足当前数据库条件的数据表不会建立。
#### 查错指北
 - 检查Mysql的用户名密码、端口号是否指定正确（位于`backsite\backsite\settings.py`中的`DATABASES`）
 - 检查Mysql中是否已经建立相应名字的`database`，对应的定义位于`backsite\backsite\settings.py`中的`DATABASES.xxx.NAME`。

#### 启动项目，贴在这
 python manage.py runserver_plus --cert server.crt 127.0.0.1:8000