# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 17:37:21 2018

@author: hujia
"""

#-*- coding:utf-8 -*-

from os import path
import numpy as np
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
#import imageio
# jieba.load_userdict("txt\userdict.txt")
# 添加用户词库为主词典,原词典变为非主词典
#import jieba.analyse
import xlwt #写入Excel表的库  
from wordcloud import WordCloud, ImageColorGenerator
#import docx

#下面导入GUI程序所需库
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from tkinter import StringVar
from tkinter import filedialog
from PIL import Image,ImageTk

#GUI设计，呈现形式大致为：
'''
 —————————————————————————————————
|  ————————————————————   —————————| |
| |                    | |                                  | |
| |                    | |                                  | |
| |    文本选择与显示   | |          词频表                  | |
| |                    | |                                  | |
| |                    | |                                  | |
| |                    | |                                  | |
|  ————————————————————   —————————| |
|  ————————————————————   —————————| |
| |                    | |                                  | |
| |                    | |                                  | |
| | 背景图片选择与显示  | |           词云图                 | |
| |                    | |                                  | |
| |                    | |                                  | |
| |                    | |                                  | |
|  ————————————————————   —————————| |
 ————————————————————————————————
'''

if __name__ == '__main__':
    #d = path.dirname(__file__) 
    d = r'C:\Users\hujia\Documents'
    isCN = 1 #默认启用中文分词
    stopwords_path = r'C:\Users\hujia\Documents\stopwords1598.txt' # 停用词词表
    #text_name = r'C:\Users\hujia\Documents\yifang.txt'
    #img_name = r'C:\Users\hujia\Downloads\5.jpg'
    
    #第一步，设置主框架
    root = tk.Tk()
    root.title('ciyun制作')
    root.resizable(0,0)
   # root.geometry('1280x980')#1280x980
    
     #窗口布局
    
    frm = tk.Frame(root,relief = 'sunken')
    
    #选择分词文件以及背景图片
    def xz_text():
        global text_name
        global word_lst
        global key_list
        global orderList
        global str_word_lst
        addwords = []
        addstopwords = []
        xls_name = r'C:\Users\hujia\Documents\wordCount.xls'
        text_name = filedialog.askopenfilename()
        if text_name !='':
            var = open(text_name).read()
            lb1.config(text = '您选择的文件是：'+text_name)
            t1.insert('insert',var);
        else:
            var = StringVar('未输入文件')
            lb1.config(text = '您没有选择任何文件')
            t1.insert('insert',var);
            
        wbk = xlwt.Workbook(encoding = 'utf-8')  
        sheet = wbk.add_sheet("wordCount")#Excel单元格名字  
        word_lst = []  
        key_list=[] 
        addwords = e1.get().split()
        addstopwords = e2.get().split()
        for items in addwords:
            jieba.add_word(items)
        
        f_stop = open(stopwords_path)
        try:
            f_stop_text = f_stop.read( )
#        f_stop_text=unicode(f_stop_text,'utf-8')
        finally:
            f_stop.close( )
        f_stop_seg_list=f_stop_text.split('\n')
        f_stop_seg_list_new = f_stop_seg_list + addstopwords
        #filepath = r'C:\Users\hujia\Desktop\remen.txt'
        print(text_name)
        
        seg_list = jieba.cut(var, cut_all=False)
        liststr="/ ".join(seg_list)
        for myword in liststr.split('/'):
            if not(myword.strip() in f_stop_seg_list_new) and len(myword.strip())>1:
                word_lst.append(myword)

        #print(word_lst)
        #print(type(word_lst))
        str_word_lst = ' '.join(word_lst)
        word_dict= {}  
        with open("wordCount.txt",'w') as wf2: #打开文件  
            for item in word_lst:  
                if item not in word_dict: #统计数量  
                    word_dict[item] = 1  
                else:  
                    word_dict[item] += 1  
          
            orderList=list(word_dict.values())  
            orderList.sort(reverse=True)  
            #print(word_dict.values())
            #print (orderList)  
            #print(word_dict)
            #word_dict_1 = word_dict.copy()  #复制一个词频字典，后面生成词云时用
            #print(word_dict_1)
            for i in range(len(orderList)):  
                for key in word_dict:  
                    if word_dict[key]==orderList[i]:  
                        wf2.write(key+' '+str(word_dict[key])+'\n') #写入txt文档  
                        key_list.append(key)  
                        word_dict[key]=0              
                #print(word_dict)  
        for i in range(len(key_list)):  
            sheet.write(i, 1, label = orderList[i])  
            sheet.write(i, 0, label = key_list[i])  
            wbk.save(xls_name) #保存为 wordCount.xls文件  
        
        
     #选择词云形状图片
    def xz_img():
        global back_coloring
        global wc
        global img1
        img_name = filedialog.askopenfilename()
        print(img_name)
        if img_name !='':
            picture = Image.open(img_name)
            #picture.show()
            print(type(picture))
            lb2.config(text = '您选择的图片是：'+img_name)
            img1 = ImageTk.PhotoImage(picture)
            print(type(img1))
            t2.image_create('end', image= img1)
        else:
            t2.text_create('您没有选择任何图片')
        back_coloring = imread(img_name)#获取背景图的array数组用于词云
        plt.imshow(back_coloring)
        plt.show()
#        print(back_coloring)
        font_path = r'C:\Windows\Fonts\simkai.ttf' # 为matplotlib设置中文字体路径
        wc = WordCloud(font_path=font_path,  # 设置字体
                   background_color="white",  # 背景颜色
                   max_words=500,  # 词云显示的最大词数
                   mask=back_coloring,  # 设置背景图片
                   max_font_size=100,  # 字体最大值
                   random_state=42,
                    prefer_horizontal = 1,
                   collocations=False,
                   width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                   )
        
        
     #left
    frm_1 = tk.Frame(frm,relief = 'groove')
    frm_1_0 = tk.Frame(frm_1,relief = 'groove')
    lb1_1 = tk.Label(frm_1_0,text = '请在下框输入添加到词库中的新词').grid(column = 0,row =0,sticky = tk.NW)
    e1 = tk.Entry(frm_1_0)#输入添加到结巴词库中的新词
    e1.insert(10,'')
    e1.grid(column = 0,row =1,sticky = tk.NW)
    lb2_2 = tk.Label(frm_1_0,text = '请在下框输入添加到停用词表中的新词').grid(column = 1,row =0,sticky = tk.NW)
    e2 = tk.Entry(frm_1_0)#输入添加到停用词表里的新词
    e2.insert(10,'')
    e2.grid(column = 1,row =1,sticky = tk.NW)
    frm_1_0.grid(column = 0,row = 0,columnspan =2,sticky = tk.NW)
    
    frm_1_1 = tk.Frame(frm_1,relief = 'groove')
            
    bt1 = tk.Button(frm_1_1,text = '点击选择文件',width = 10,height = 2,bg = 'red',command = xz_text,relief='raised')
    bt1.grid(column = 0,row =0)
    lb1 = tk.Label(frm_1_1,text = '待选文件',show = None)
    lb1.grid(column = 1,row =0,sticky = tk.W)
    t1 = ScrolledText(frm_1_1,width = 55,height = 20,bg = 'gray')
    t1.grid(column = 0,row =1,columnspan=2)
    
    bt2 = tk.Button(frm_1_1,text = '点击选择图片',width = 10,height = 2,bg = 'yellow',command = xz_img,relief = 'raised')
    bt2.grid(column = 0,row =2)
    lb2 = tk.Label(frm_1_1,text = '待选图片',show = None)
    lb2.grid(column = 1,row =2,sticky = tk.W)

    t2 = tk.Text(frm_1_1,width = 55,height = 25,bg = 'pink',fg = 'black')
    sc1 = tk.Scrollbar(frm_1_1,orient = 'horizontal')
    sc1.grid(column = 0,row =4,columnspan =2,sticky =tk.E+tk.W+tk.N)
    sc2 = tk.Scrollbar(frm_1_1)
    sc2.grid(column = 1,row =3,sticky =tk.N+tk.S+tk.E)
    sc1.config(command = t2.xview)
    sc2.config(command = t2.yview)
    t2.config(xscrollcommand=sc1.set,yscrollcommand = sc2.set)
    t2.grid(column = 0,row =3,columnspan=2)
    
    frm_1_1.grid(column = 0,row =1,columnspan =2)
    
    frm_1.grid(column = 0,row =0)
    
    #right
    frm_2 = tk.Frame(frm,relief = 'groove')
    
    frm_2_1 = tk.Frame(frm_2,relief = 'groove')
    
    def change_list():
        for i in range(len(key_list)):
            wf.insert('',i,values=(i+1,key_list[i],orderList[i],orderList[i]/len(word_lst)))
    
    bt3 = tk.Button(frm_2_1,text = '点击更新列表',width = 10,height = 2,bg = 'gold',command = change_list,relief = 'raised')
    bt3.grid(column = 0,row =0)
    #绘制词频表
    wf = ttk.Treeview(frm_2_1,height = 15,show = 'headings')
    sc3 = tk.Scrollbar(frm_2_1)
    sc3.grid(column = 1,row =1,sticky =tk.N+tk.S+tk.E)
    sc3.config(command = wf.yview)
    wf['column']=['序号','词','出现次数','频率']
    #设置列宽
    wf.column('序号',width = 100)
    wf.column('词',width = 100)
    wf.column('出现次数',width = 150)
    wf.column('频率',width = 100)
    #设置标签显示名字
    wf.heading('序号',text = '序号')
    wf.heading('词',text = '词')
    wf.heading('出现次数',text = '出现次数')
    wf.heading('频率',text = '频率')
            
    wf.grid(column = 0,row =1)
    frm_2_1.grid(row =0)

    def to_file1():
        global img2
        wc.generate(str_word_lst)
       # h  = np.random.randint(120,250)
        #s = int(100.0 * 255.0 / 255.0)
        #l = int(100.0 * float(np.random.randint(60, 120)) / 255.0)
        #hsl = lambda:(h,s,l)
        #hsl = (h,s,l)
        #array_picture = wc.recolor(color_func = hsl).to_array()
        cmap=plt.get_cmap(cmpsel.get())
        wc.recolor(colormap = cmap)
        array_picture = wc.to_array()
        plt.imshow(array_picture)
        plt.show()
        pilstyle = Image.fromarray(np.uint8(array_picture))
        print(type(pilstyle))
        img2 = ImageTk.PhotoImage(pilstyle)
        t3.image_create('end',image = img2)
        wc.to_file(path.join(d, imgname1))
        
    def to_file2():
        global img3
        wc.generate(str_word_lst)
        image_colors = ImageColorGenerator(back_coloring)
        wc.recolor(color_func=image_colors)
        #print(image_colors)
        array_picture = wc.to_array()
        plt.imshow(array_picture)
        plt.show()
        pilstyle = Image.fromarray(np.uint8(array_picture))
        img3 = ImageTk.PhotoImage(pilstyle)
        t3.image_create('end',image = img3)
        wc.to_file(path.join(d, imgname2))

    def show_cmp():
        figure()
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))
        plt.imshow(gradient,aspect='auto',cmap=plt.get_cmap(cmpsel.get()))
        plt.show()
    
    imgname1 = 'DefautColors.jpg'
    imgname2 = 'ColorsByImg.jpg'
    #显示词云
    frm_2_2 = tk.Frame(frm_2,relief = 'groove')
    cmpsel = ttk.Combobox(frm_2_2)
    cmpsel['values']=('viridis','plasma','inferno','magma','Greys','Purples','Blues','Greens'
            ,'Oranges','Reds','YlOrBr','YlOrRd','OrRd','PuRd','RdPu','BuPu','GnBu'
            ,'PuBu','YlGnBu','PuBuGn','BuGn','YlGn','binary','gist_yarg','gist_gray'
            ,'gray','bone','pink','spring','summer','autumn','winter','cool','Wistia'
            ,'hot','afmhot','gist_heat','copper','PiYG','PRGn','BrBG','PuOr','RdGy'
            ,'RdBu','RdYlBu','RdYlGn','Spectral','coolwarm','bwr','seismic','Pastel1'
            ,'Pastel2','Paired','Accent','Dark2','Set1','Set2','Set3','tab10','tab20'
            ,'tab20b','tab20c','flag','prism','ocean','gist_earth','terrain'
            ,'gist_stern','gnuplot','gnuplot2','CMRmap','cubehelix','brg','hsv'
            ,'gist_rainbow','rainbow','jet','nipy_spectral','gist_ncar')
    cmpsel["state"] = "readonly"
    cmpsel.current(0)
    cmpsel.bind("<<ComboboxSelected>>", show_cmp)
    cmpsel.grid(column = 0,row =0)
    bt4 = tk.Button(frm_2_2,text = '点击生成默认颜色图片',width = 10,height = 2,bg = 'blue',command = to_file1,relief = 'raised')
    bt5 = tk.Button(frm_2_2,text = '点击生成模板图颜色图片',width = 10,height = 2,bg = 'green',command = to_file2,relief = 'raised')
    bt4.grid(column = 1,row =0)
    bt5.grid(column = 2,row =0)
    
    t3 = tk.Text(frm_2_2,width = 65,bg = 'cyan',fg = 'black')
    sc4 = tk.Scrollbar(frm_2_2,orient = 'horizontal')
    sc4.grid(column = 0,row =2,columnspan =3,sticky =tk.E+tk.W+tk.N)
    sc5 = tk.Scrollbar(frm_2_2)
    sc5.grid(column = 2,row =1,sticky =tk.N+tk.S+tk.E)
    sc4.config(command = t3.xview)
    sc5.config(command = t3.yview)
    t3.config(xscrollcommand=sc4.set,yscrollcommand = sc5.set)
    t3.grid(column = 0,row =1,columnspan =3,sticky = tk.W)
    
    frm_2_2.grid(row =1)
    frm_2.grid(column = 1,row =0)
    
    
    frm.grid()
    
    root.mainloop()
    
