%pip install yfinance
import yfinance as yf
from tqdm import tqdm
from datetime import datetime
import time
import pandas as pd
import os



cols = ['sid','Date','Volume','Open','High','Low','Close','Change']

stock_list=['1101','1102','1216','1301','1303','1326','1402','1590','2002','2207','2603','2609','2615','2801',
           '2880','2881','2882','2884','2885','2886','2887','2891','2892','5876','5880','2912','5871',
            '9910','6505','2303','2330','2379','2408','2454','3034','3711','6415','2357','2382','2395','4938',
             '2409','3008','2412','3045','4904','2308','2327','8046','2317']


lost_ls = []
stock_ls = []
df = pd.DataFrame()
for stc in tqdm(stock_list):
  try :
    dff = yf.download(f'{stc}.TW',start = '2018-01-01',end = '2023-06-12',progress=False)
  except:
    lost_ls.append(stc)
    continue
  if len(dff) != 0:
    stock_ls.append(stc)
    change = []
    for i in range(0,len(dff)):
      change.append(dff.iloc[i]['High']-dff.iloc[i]['Low'])
    dff['Change'] = change 
    dff['sid'] = stc
    dff = dff.reset_index()
    dff = dff[cols]
    df = pd.concat([df,dff])
    # print('done')
df.to_csv(f'/content/stock_data.csv', index=False)