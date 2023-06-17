from flask import Flask, render_template, request, jsonify
import db
import qry 
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from mysql.connector.errors import Error
    
app = Flask(__name__)

#預設網頁
@app.route("/")
def login():
    return render_template("login.html")

### 註冊 ###
#註冊按鍵導入peoplec.html
@app.route("/register", methods=["POST","GET"])
def register():
    return render_template("peoplec.html") 

#新增帳號:成功則導入peoples.html
@app.route("/people_insert", methods=["POST","GET"])
def people_insert():
    pid = request.form.get("id")
    pwd = request.form.get("pwd")
    name = request.form.get("name")
    sql = f"""insert people (pid, pwd, name) values ('{pid}','{pwd}','{name}')"""
    rtn=db.process_data(sql)
    if rtn==0:
        return render_template("peoples.html") 
    else:
        print('insert error:',rtn.errno,rtn)
        error_message = "inser error. ", str(rtn)
        response = jsonify({'error': error_message})
        response.status_code = 400  
        return response

#設定帳號
@app.route("/people_setup", methods=["POST","GET"])
def people_setup():
    pid = request.form.get("pid")
    name = request.form.get("name")    
    return render_template("peopleu.html",pid=pid,name=name) 

#修改帳號
@app.route("/people_update", methods=["POST","GET"])
def people_update():
    pid = request.form.get("pid")
    pwd = request.form.get("pwd")
    name = request.form.get("name")
    sql = f"""update people set pwd='{pwd}',name='{name}' where pid = '{pid}'"""
    db.process_data(sql)
    sql = f"""select pid,name from people where pid='{pid}'"""
    records=db.query_data(sql)
    sql = qry.invest_sql(pid)
    invest=db.query_data(sql)    
    return render_template("invest.html", data=records, invest=invest)

### 登入 ###
#檢查login帳密,正確則記錄登入歷程,並導入invest.html
@app.route("/login_check", methods=["POST","GET"])
def login_check():
    pid = request.form.get("id")
    pwd = request.form.get("pwd")
    sql = "select pid,name from people where pid='"+pid+"' and pwd='"+pwd+"'"
    records = db.query_data(sql)
    if len(records)== 0 :
        return "login error."
    else:
        #記錄登入歷程
        sql = f"""insert login_his (pid,time) values ('{pid}',NOW())"""
        db.process_data(sql)
        '''
        #導入invest.html
        sql = qry.invest_sql(pid)
        invest=db.query_data(sql)    
        return render_template("invest.html", data=records,invest=invest) 
        '''
        return invest_query(pid)

### 投資組合 ###
@app.route("/invest_query/<pid>", methods=["POST","GET"])
def invest_query(pid):
        print(pid)
        sql = "select pid,name from people where pid='"+pid+"'"
        records = db.query_data(sql)

        #導入invest.html
        sql = qry.invest_sql(pid)
        invest=db.query_data(sql)    
        return render_template("invest.html", data=records,invest=invest) 
    

#投資組合清單處理
@app.route("/invest_proc", methods=["POST","GET"])
def invest_proc():
    iid = request.form.get("iid")
    name = request.form.get("name")
    sdate = request.form.get("sdate")
    edate = request.form.get("edate")
    pid = request.form.get("pid")
    pname = request.form.get("pname")
    insert = request.form.get("insert")
    update = request.form.get("update")
    delete = request.form.get("delete")
    
    #新增
    if insert is not None:
        sql = f"""insert invest_group (name, sdate, edate, pid) 
              values ('{name}','{sdate}','{edate}','{pid}')"""
        db.process_data(sql)
    
    #修改
    elif update is not None:
        sql = f"""update invest_group set iid='{iid}',name='{name}',sdate='{sdate}',edate='{edate}' 
              where iid ='{iid}' and pid = '{pid}'"""
        db.process_data(sql)
    
    #刪除
    elif delete is not None:
        sql =f"""delete from invest_group where iid='{iid}' and pid='{pid}'"""
        db.process_data(sql)

    #查詢
    records=[[pid,pname]]
    sql = qry.invest_sql(pid)
    invest=db.query_data(sql)    
    return render_template("invest.html", data=records, invest=invest) 

### 圖形顯示 ###
#將圖片放到前端用
def return_img_stream(img_local_path):
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream

#產生圖檔
def gen_img(iid):
        # 從資料庫中取得股價資料
    sql =f"""
         select i.sdate, i.edate, g.iid, g.sid, g.weight from stock_group g, invest_group i 
         where g.iid = i.iid and g.iid = {iid}"""
    stock_list = db.query_data(sql)
        
    # 處理查詢結果
    for row in stock_list:
            # 每行資料都是一個元組，可以透過索引值來訪問每個欄位的值
            sdate = row[0]  # 第1個欄位的值
            edate = row[1]  # 第2個欄位的值
            iid = row[2]  # 第3個欄位的值
            sid = row[3]  # 第4個欄位的值
            weight = row[4]  # 第5個欄位的值
        
        # 將資料轉換成DataFrame
    columns_name = ['sdate', 'edate', 'iid', 'sid', 'weight']  # 取得欄位名稱
    stock_df = pd.DataFrame(stock_list, columns=columns_name)
       
        # 取得指定股票代號的資料
    image_paths = []
    profit_list = []
        
    plt.clf()
    plt.figure(figsize=(10, 6))

    for df_sid in stock_df['sid']:
            yf_data = yf.download(f"{df_sid}.TW", start=stock_df['sdate'][0], end=stock_df['edate'][0])
    
            # 計算獲利
            this_profit = round((yf_data["Close"][-1] - yf_data["Close"][0]) / yf_data["Close"][0], 4) * 100
            profit_list.append(this_profit)
    
            # 繪製股價績效圖
            plt.plot(yf_data.index, yf_data["Close"], label=f"Stock {df_sid}")

    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title("Stock Performance")
    plt.legend()
    plt.grid(True)
    plt.savefig("templates/combined_price_plot.png")  # 儲存圖片
    plt.close()

    profit = 0.0
        
    for i in range(len(stock_df['weight'])):
            profit += stock_df['weight'][i] * profit_list[i]
    
    return profit

### 股票清單　###
#股票清單資訊
@app.route("/group_query/<iid>,<iname>,<pid>,<pname>", methods=["POST","GET"])
def group_query(iid,iname,pid,pname):
    data=[iid,iname,pid,pname]
    sql = qry.group_sql(iid)
    records=db.query_data(sql)
    print(iid)
    print(sql)
    gen_img(iid)
    img_stream = return_img_stream("templates/combined_price_plot.png")
    return render_template("group.html", group=records, data=data, img_stream=img_stream) 


#股票清單處理
@app.route("/group_proc", methods=["POST","GET"])
def group_proc():
    iid = request.form.get("iid")
    iname= request.form.get("iname")
    pid = request.form.get("pid")
    pname = request.form.get("pname")
    data=[iid,iname,pid,pname]
    sid = request.form.get("sid")
    weight = request.form.get("weight")
    insert = request.form.get("insert")
    update = request.form.get("update")
    delete = request.form.get("delete")
    analyze = request.form.get("analyze")

    #新增
    if insert is not None:
        sql = f"""insert stock_group (iid, sid, weight) values ({iid},'{sid}',{weight})"""
        db.process_data(sql)

    #修改
    elif update is not None:
        sql = f"""update stock_group set iid={iid},sid='{sid}',weight={weight} where iid ={iid} and sid = '{sid}'"""
        db.process_data(sql)
    
    #刪除
    elif delete is not None:
        sql =f"""delete from stock_group where iid={iid} and sid='{sid}'"""
        db.process_data(sql)

    #查詢
    sql = qry.group_sql(iid)
    records=db.query_data(sql)   
    print(iid)
    gen_img(iid)
    img_stream = return_img_stream("templates/combined_price_plot.png")
    return render_template("group.html", group=records, data=data,img_stream=img_stream) 



#股票詳細資訊
@app.route("/stock_query/<iid>,<sid>", methods=["POST","GET"])
def stock_query(iid,sid):
    sql = qry.stock_sql(iid,sid)
    records=db.query_data(sql)
    return render_template("stock.html", stock=records, data=[iid,sid]) 
    
if __name__ == "__main__":
    app.run(debug=True)
    