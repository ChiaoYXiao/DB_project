def group_sql(iid):
    sql =f"""
        with
        minmax_date(iid,sid, sdate, edate) AS
        (select ig.iid, sg.sid, min(st.date), max(st.date)
        from invest_group ig, stock_group sg, stock_trans st
        where ig.iid = sg.iid
        and sg.sid = st.sid
        and sg.sid = st.sid
        and st.date between ig.sdate and ig.edate
        group by ig.iid, st.sid)
  
        select sg.sid, s.name, sg.weight, round(((st2.close - st1.close) / st1.close)*100,2)  as profit
        from invest_group ig, stock_group sg, minmax_date mm, stock_trans st1, stock_trans st2, stock s
        where sg.sid = s.sid 
        and ig.iid = mm.iid
        and ig.iid = sg.iid
        and sg.sid = mm.sid
        and mm.sdate = st1.date
        and mm.sid = st1.sid
        and mm.edate = st2.date
        and mm.sid = st2.sid
        and ig.iid = '{iid}'
        order by ig.iid, mm.sid;
        """
    return sql
 
def invest_sql(pid):
    sql = f"""
        with
        minmax_date(iid,sid, sdate, edate) AS
        (select ig.iid, sg.sid, min(st.date), max(st.date)
        from invest_group ig, stock_group sg, stock_trans st
        where ig.iid = sg.iid
        and sg.sid = st.sid
        and sg.sid = st.sid
        and st.date between ig.sdate and ig.edate
        group by ig.iid, st.sid)

        select ig.*,round(sum(((st2.close - st1.close) / st1.close)*sg.weight),2) as profit
        from invest_group ig 
        left join stock_group sg on ig.iid = sg.iid
        left join stock s on sg.sid = s.sid
        left join minmax_date mm on ig.iid = mm.iid and sg.sid = mm.sid
        left join stock_trans st1 on mm.sdate = st1.date and mm.sid = st1.sid
        left join stock_trans st2 on mm.edate = st2.date and mm.sid = st2.sid
        where ig.pid = '{pid}'
        group by ig.iid
        order by ig.iid;
    """
    return sql

def stock_sql(iid,sid):
    sql = f"""
        select s.name,t.* from stock_trans t,stock_group g,stock s,invest_group i
        where t.sid = s.sid
        and t.date <= i.edate 
        and t.date >= i.sdate
        and i.iid = g.iid
        and g.sid = t.sid          
        and i.iid = {iid} 
        and s.sid = '{sid}'
    """ 
    return sql