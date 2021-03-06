# -*- coding: utf-8 -*-
# @Time    : 18-2-25 下午5:00
# @Author  : Storm
# @File    : my_getdata_process.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
import datetime

data_train_getdata = pd.read_csv('resultAend/getdata_train.csv')
data_testA_getdata = pd.read_csv('resultAend/getdata_testA.csv')
data_testB_getdata = pd.read_csv('resultAend/getdata_testB.csv')

data_train = pd.DataFrame()
data_train['r_date'] = data_train_getdata['r_date']
data_train['date'] = data_train_getdata['date']
data_train['brand'] = data_train_getdata['brand']
data_train['cnt'] = data_train_getdata['cnt']
data_train['day_of_week'] = data_train_getdata['day_of_week']

# 统计每天的总数
df_allcnt = data_train.groupby(by=['r_date', 'date', 'day_of_week'])['cnt'].sum()
df_allcnt = df_allcnt.to_frame()

df_allcnt_tA = data_testA_getdata.dropna(axis=0)
df_allcnt_tB = data_testB_getdata.dropna(axis=0)

df_allcnt.to_csv('resultAend/getdata_train_cnt.csv')
df_allcnt_tA.to_csv('resultAend/getdata_testA_cnt.csv', index=None)
df_allcnt_tB.to_csv('resultAend/getdata_testB_cnt.csv', index=None)

# =========================================================================

df_train = pd.read_csv('resultAend/getdata_train_cnt.csv')
df_testA = pd.read_csv('resultAend/getdata_testA_cnt.csv')
df_testB = pd.read_csv('resultAend/getdata_testB_cnt.csv')
as_testA = pd.read_table("data/answer_A_20180225.txt", header=0, encoding='gb2312', delim_whitespace=True)

df_train['r_date'] = pd.to_datetime(df_train['r_date'])
df_testA['r_date'] = pd.to_datetime(df_testA['r_date'])
df_testB['r_date'] = pd.to_datetime(df_testB['r_date'])

# 年月日
df_train['month'] = df_train['r_date'].apply(lambda x: x.month)
df_train['year'] = df_train['r_date'].apply(lambda x: x.year)
df_train['day'] = df_train['r_date'].apply(lambda x: x.day)

df_testA['month'] = df_testA['r_date'].apply(lambda x: x.month)
df_testA['year'] = df_testA['r_date'].apply(lambda x: x.year)
df_testA['day'] = df_testA['r_date'].apply(lambda x: x.day)
df_testA['cnt'] = as_testA['cnt']

df_testB['month'] = df_testB['r_date'].apply(lambda x: x.month)
df_testB['year'] = df_testB['r_date'].apply(lambda x: x.year)
df_testB['day'] = df_testB['r_date'].apply(lambda x: x.day)

# 合并testA的答案
df_train_resultA = pd.merge(df_train, df_testA, how='outer')

df_train.to_csv('resultAend/getdata_train_ok.csv', index=None)
df_testA.to_csv('resultAend/getdata_testA_ok.csv', index=None)
df_testB.to_csv('resultAend/getdata_testB_ok.csv', index=None)
df_train_resultA.to_csv('resultAend/getdata_train_resultA.csv', index=None)

# 删除真实日期
df_train = df_train.drop(['r_date'], axis=1)
df_testA = df_testA.drop(['r_date'], axis=1)
df_testA = df_testA.drop(['cnt'], axis=1)
df_testB = df_testB.drop(['r_date'], axis=1)


# print(df_train.head())
# print(df_testA.head())
# print(df_testB.head())


# =========================================================================================
# PolynomialFeatures
def polyX(df_train_X, df_testA, df_testB):
    poly = PolynomialFeatures(2, interaction_only=False)  # 默认的阶数是２，同时设置交互关系为true
    X = pd.concat([df_train_X, df_testA, df_testB])
    polyX = poly.fit_transform(X)
    return polyX


def polyX_go():
    predictors = [f for f in df_testB.columns if f not in ['cnt']]
    df_train_X = df_train[predictors]
    my_polyX = polyX(df_train_X, df_testA, df_testB)
    pd.DataFrame(my_polyX).to_csv('resultAend/getdata_polyX.csv', index=None)

    # 读取my_polyX
    my_polyX = pd.read_csv('resultAend/getdata_polyX.csv')
    polyX_train = my_polyX[:len(df_train_X)]
    polyX_testA = my_polyX[len(df_train_X):(len(df_train_X) + len(df_testA))]
    polyX_testB = my_polyX[len(df_train_X) + len(df_testA):]

    df_test_polyA = polyX_testA
    df_test_polyA['date'] = pd.Series(df_testA['date'].values, index=df_test_polyA.index)
    df_test_polyA['day_of_week'] = pd.Series(df_testA['day_of_week'].values, index=df_test_polyA.index)
    df_test_polyA['cnt'] = pd.Series(as_testA['cnt'].values, index=df_test_polyA.index)

    df_test_polyB = polyX_testB
    df_test_polyB['date'] = pd.Series(df_testB['date'].values, index=df_test_polyB.index)
    df_test_polyB['day_of_week'] = pd.Series(df_testB['day_of_week'].values, index=df_test_polyB.index)

    df_train_poly = polyX_train
    df_train_poly['cnt'] = df_train['cnt']
    df_train_poly['date'] = df_train['date']
    df_train_poly['day_of_week'] = df_train['day_of_week']

    df_train_poly.to_csv('resultAend/getdata_train_poly.csv', index=None)
    df_test_polyA.to_csv('resultAend/getdata_testA_poly.csv', index=None)
    df_test_polyB.to_csv('resultAend/getdata_testB_poly.csv', index=None)

    df_train_resultA_poly = pd.merge(df_train_poly, df_test_polyA, how='outer')
    df_train_resultA_poly.to_csv('resultAend/getdata_train_resultA_poly.csv', index=None)


polyX_go()
