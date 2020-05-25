#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# In[2]:


samsung = pd.read_csv("./samsung_2.csv")


# ## MACD
# 
# - MACD는 장단기 이동평균선의 차이를 이용하여 매매신호를 포착하려는 기법
# - 원리는 장기 이동평균선과 단기평균선이 서로 멀어지게 되면 언젠가는 다시 가까워져 어느 시점에서 서로 교차한다는 성질을 이용하여 두 개의 이동평균선이 멀어지게 되는 가장 큰 시점을 찾고자 하는 것이다.

# ### 기본 공식
# - MACD : 12일 지수이동평균 - 26일 지수이동평균
# - 시그널 : MACD의 9일 지수이동평균
# - 오실레이터 : MACD값 - 시그널 값

# In[11]:


def get_macd(df, short=12, long=26, t=9):
    ma_12 = df.st_close.ewm(span=12).mean()
    ma_26 = df.st_close.ewm(span=26).mean()
    macd = ma_12 - ma_26
    macds = macd.ewm(span=9).mean()
    macdo = macd - macds
    df = df.assign(macd = macd, macds=macds, macdo = macdo).dropna()
    return df


# In[12]:


samsung_macd = get_macd(samsung)


# In[13]:


samsung_macd.head(3)


# In[14]:


samsung_macd['neg_pos'] = (samsung_macd.macdo > 0).map({True : 'b', False : 'r'})


# In[16]:


plt.figure(figsize=(150,8))
plt.plot(samsung_macd.st_day, samsung_macd.macd, label='MACD', color = '#002AFF')
plt.plot(samsung_macd.st_day, samsung_macd.macds, label='Signal Line', color = '#00FFA9')
plt.bar(samsung_macd.st_day, samsung_macd.macdo, label='Histogram', color = samsung_macd.neg_pos, width=0.6, align='center')
plt.legend(loc='upper left')
plt.xticks(rotation=60)
plt.show()


# ## RSI
# 
# - RSI는 주식, 선물, 옵션 등의 기술적 분석에 사용되는 보조지표이다. RSI는 가격의 상승압력과 하강압력 간의 상대적인 강도를 나타낸다.
# 
# - 주어진 기간의 모든 날의 주가에 대하여,
# 
#     -- 가격이 전일 가격보다 상승한 날의 상승분은 U 값이라 하고,
#     
#     -- 가격이 전일 가격보다 하강한 날의 하락분은 D 값이라 한다.
#     
#     -- U값과 D값의 평균값을 구하여 각각 AU와 AD라 한다.
#     
#     -- AU를 AD 값으로 나눈 값을 RS라 하며, RS가 크다는 건 일정 기간 하락한 폭보다 상승한 폭이 크다는 의미이다.

# ## RSI 계산 공식
# 
# - RSI = RS / (1 + RS)
# 
# - RSI = AU / (AU + AD)
# 
# - 백분율로 나타냄
# 
# - RSI-signal : RSI 이동 평균선

# In[17]:


def func_RSI(df, rsi_date, rsi_signal):
    U = df.where(df.diff(1) > 0, 0)
    D = df.where(df.diff(1) < 0, 0)
    
    AU = pd.DataFrame(U).rolling(rsi_date).mean()
    AD = pd.DataFrame(D).rolling(rsi_date).mean()
    
    RSI = AU.div(AD+AU) * 100
    
    RSI_Signal = RSI.rolling(rsi_signal).mean()
    return RSI, RSI_Signal


# In[18]:


rsi, rsi_sig = func_RSI(samsung.st_close, 10, 7)


# In[19]:


samsung = samsung.assign(rsi = rsi, rsi_sig = rsi_sig)


# In[20]:


samsung.dropna().head()


# In[21]:


plt.figure(figsize=(150,8))
plt.plot(samsung.st_day, samsung.rsi, label = "RSI", color = '#000000')
plt.plot(samsung.st_day, samsung.rsi_sig, label = "RSI signal", color = '#E5A4CB')
plt.legend(loc='upper left')
plt.xticks(rotation=60)
plt.show()


# In[ ]:




