<<　股票投資組合分析系統 >>

本專題將資料庫架設在個人電腦上並將其作為伺服器，
再提供前端頁面讓使用者進行操作。

以下提供如何使用此處提供的程式碼以使用本專題的服務：

== 第一步 ==

先下載 Github 上的 Source_Codes 資料夾，
內含啟動這項專題功能的檔案，有以下八項：

1. 四項程式檔案
－－－－－－－－－－－－－－－－－
"app.py"  	  ---> 主程式
"db.py"   	  ---> 連接資料庫
"qry.py"　	  ---> Query 函式
"create_data.sql" ---> 建立資料庫
－－－－－－－－－－－－－－－－－

2. 四個資料夾
－－－－－－－－－－－－－－－－－
".ipynb_checkpoints"
"__pycache__"
"static"     	  ---> CSS  前端
"templates"  	  ---> HTML 頁面
－－－－－－－－－－－－－－－－－


== 第二步 ==

開啟 MySQL，並在 localhost 中執行 create_data.sql。


== 第三步 ==

Python 需安裝 flask 及 MySQL 相關套件：

pip install flask
pip install mysql-connector-python

（依照個人環境不同而將使用不同指令安裝這兩個套件
　此處以 pip install 安裝）

flask 是我們使用的框架；mysql-connector-python 用於連接資料庫


== 第四步 ==

開啟 db.py，檢視自己的 MySQL 修改對應的參數

 conn = mysql.connector.connect(host='localhost', \
 port='3306', \
 database='invest', \ 
 user='root', \
 password='', \    ---> 這邊要輸入自己 localhost 的密碼
 charset='utf8')

本專題使用預設設定，上面的參數可以透過
查看自己 local instance 的屬性查詢得知。

若沒有設定好，會導致沒有辦法連線資料庫。


== 第五步 ==

上述設定完成後，執行 app.py 檔案，
執行後應該會出現以下訊息：

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 940-345-379

看到以上訊息，代表啟動成功。

這時候請在瀏覽器中輸入　http://127.0.0.1:5000
就可以開始在網頁中使用我們的專題功能。
