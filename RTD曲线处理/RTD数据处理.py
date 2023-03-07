import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import *

root = tk.Tk()
root.title('平均停留时间处理系统V1.0')
label=Label(root,fg="blue",bg="white",font="Time 15 bold")
root.geometry('600x200+450+200')
root.withdraw

def openpath():  ###打开文件函数
    global col_concat_df
    global twu_array
    global cwu_array
    file_openpath = filedialog.askopenfilename(title='选择文件')# 获取文件路径
    df = pd.read_csv(file_openpath)  # 读取文件,读取csv文件
    t_df = df['t']  # 将时间赋值给变量t_df
    c_df = df['c(t)']  # 将浓度赋值给变量c_df,数据类型仍为dataframe
    twu_df = t_df / 6.18  ####################获取无量纲时间，无量纲时间数据类型为datafr，分母为理论停留时间。
    twu_array = np.array(twu_df)  # 将无量纲时间的格式由datafram转化为数组
    c_array = np.array(c_df)
    q = np.trapz(c_array, twu_array)  ##q为经过改点处示踪剂的总量
    cwu_df = c_df / q  # 得到datafram格式无量纲浓度
    cwu_array = np.array(cwu_df)  # 无量纲浓度由datafram格式转化为array格式
    e = np.trapz(cwu_array, twu_array)
    f = twu_array * cwu_array
    g = np.trapz(f, twu_array)
    h = g / e  ######h就是平均停留时间因子
    i = ((twu_array - h) ** 2) * cwu_array
    j = np.trapz(i, twu_array)
    k = j / (h) ** 2
    #报存平均停留时间及方差
    h_series = pd.Series([h])
    k_series = pd.Series([k])  # 将数值e,k转化为Series类型
    # 将两个series进行拼接成一个表
    df_hk = pd.DataFrame({'tm': h_series, 'ver': k_series})
    # 将无量纲浓度和无量纲时间拼接到一个表
    col_concat_df = pd.concat([twu_df, cwu_df, df_hk], axis=1)
    label["text"] = "数据已处理完成，请保存为.csv格式"
    print('数据已处理完毕，请保存')
def savepath():  ###保存文件函数
    global col_concat_df
    file_savepath = filedialog.asksaveasfilename(title='保存文件')
    col_concat_df.to_csv(file_savepath)  # 读入路径是正斜杠，输出路径为反斜杠；
    label["text"] = "数据已保存，再次使用请点击（打开文件）按钮"
    print('数据已经保存')
def plot_curve():##绘制RTD曲线
    global twu_array
    global cwu_array
    plt.plot(twu_array, cwu_array, color='b', marker='o', linestyle='-', linewidth=0.5)
    plt.title('RTD', fontsize=15, color='black')
    plt.xlabel('t', fontsize=15, color='black')
    plt.ylabel('c', fontsize=15, color='black', rotation=360)
    plt.xlim((0, 4))
    plt.show()

bt1 = tk.Button(root, text='打开文件', bg='blue', font=('Arial 12 bold'), width=15, height=2, command=openpath)
label.pack(side=LEFT,fill=Y)
bt1.pack()
bt2 = tk.Button(root, text='保存文件', bg='red', font=('Arial 12 bold'), width=15, height=2, command=savepath)
bt2.pack(pady=10)
bt3=tk.Button(root, text='绘制RTD', bg='orange', font=('Arial 12 bold'), width=15, height=2, command=plot_curve)
bt3.pack()
root.mainloop()