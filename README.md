# 简单疫情可视化网站

上海大学2020年暑期认识实习大作业，实现了简单的疫情可视化网站。

前端代码仓库：https://github.com/Armo00/demo3

前端：Vue 

后端：flask+mysql

## 安装及使用

后端模块：

```shell
git clone --recursive https://github.com/kyloris0660/virsualize_cov19.git
cd ./virus/
pip3 install -r requirements.txt
# 修改数据库等操作
python3 app.py
```

前端模块

```shell
cd ./virus/demo3/vue test/vue_test
npm install
npm run serve
npm run build
```

数据库文件

[virus.sql](virus.sql)

## 实现功能

* 中国2020/1/19-2020/7/11疫情数据可视化
* 传染病SEIR模型及可视化
* 疫苗和管控作用可视化（基于对模型S（易感人群）， r（接触人数）参数调整，**模型仅供参考，无现实意义**）

## 截图

![https://raw.githubusercontent.com/kyloris0660/virsualize_cov19/master/screenshots/000.png]()

![https://raw.githubusercontent.com/kyloris0660/virsualize_cov19/master/screenshots/001.png]()

![https://raw.githubusercontent.com/kyloris0660/virsualize_cov19/master/screenshots/002.png]()

![https://raw.githubusercontent.com/kyloris0660/virsualize_cov19/master/screenshots/003.png]()

