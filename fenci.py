# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 09:07:19 2018

@author: hujia
"""

#!/usr/bin/python    
# -*- coding:utf-8 -*-    
  
#import sys  
#reload(sys)  
  
#sys.setdefaultencoding('utf-8')  
  
import jieba  
import jieba.analyse  
import xlwt #写入Excel表的库  
from wordcloud import WordCloud
  
if __name__=="__main__":  
  
    wbk = xlwt.Workbook(encoding = 'ascii')  
    sheet = wbk.add_sheet("wordCount")#Excel单元格名字  
    word_lst = []  
    key_list=[]  
    filepath = r'C:\Users\hujia\Documents\Tencent Files\920777584\FileRecv\1.txt'
    text = open(filepath).read()
    for line in open(filepath):#1.txt是需要分词统计的文档    
        it = line.strip('\n\r').split('\t') #制表格切分  
        #print (item)  
        tags = jieba.analyse.extract_tags(it[0]) #jieba分词  
        for t in tags:  
            word_lst.append(t)  
    #print(word_lst)
  
    word_dict= {}  
    with open("wordCount_test97.txt",'w') as wf2: #打开文件  
  
        for item in word_lst:  
            if item not in word_dict: #统计数量  
                word_dict[item] = 1  
            else:  
                word_dict[item] += 1  
  
        orderList=list(word_dict.values())  
        orderList.sort(reverse=True)  
        print (len(orderList))  
        #print(word_dict)
        word_dict_copy = word_dict.copy()
        for i in range(len(orderList)):  
            for key in word_dict:  
                if word_dict[key]==orderList[i]:  
                    wf2.write(key+' '+str(word_dict[key])+'\n') #写入txt文档  
                    key_list.append(key)  
                    word_dict[key]=0  
    #print(word_dict.values())
    print(len(key_list))
      
    for i in range(len(key_list)):  
        sheet.write(i, 1, label = orderList[i])  
        sheet.write(i, 0, label = key_list[i])  
    wbk.save('wordCount_test97.xls') #保存为 wordCount.xls文件  

    '''
    font_path = r'C:\Windows\Fonts\simkai.ttf' # 为matplotlib设置中文字体路径
    wc = WordCloud(font_path=font_path,  # 设置字体
               background_color="white",  # 背景颜色
               max_words=2000,  # 词云显示的最大词数
               #mask=back_coloring,  # 设置背景图片
               max_font_size=100,  # 字体最大值
               random_state=42,
               width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
               )
    
    frq = []
    for kv in word_dict_copy.items():
        frq.append(kv)
    #print(frq)
 
    wc.fit_words(word_dict_copy)
    wc.to_file("97.jpg")
    '''