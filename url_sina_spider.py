# -*- coding:utf-8 -*-

''' 爬取对象为sina微博名：木木萝希木 的用户，文件同级
建立img文件夹，和做对比用的old.txt，把op_str.py放入导入的文件夹里
以上'''

import re,urllib,urllib2,os
from op_str import Right

__all__=['gethtml','getimg','new_img_list',
        'cre_dir_img','get_old','compare_2',
        'get_others','open_html','urlretrieve']

def gethtml(url):
    '''此定义法方暂时作废 2015/10/08'''
    page=urllib.urlopen(url)
    html=page.read()
    return html

def getimg():
    '''曾经的骨架,2015/10/12不再使用'''
    count=open(r'c:\users\zhpeng\desktop\october_sch\img\number.txt','r+')
    x=int(count.read())
    count.close()
    count_img=0
    imglist=new_img_list()
    for imglist_1 in imglist:
        list_1=re.sub(r'/',r'http://ww4.sinaimg.cn/bmiddle/',imglist_1)
        urllib.urlretrieve(list_1,r'c:\users\zhpeng\desktop\october_sch\img\%s.jpg'%x)
        x+=1
        count_img+=1
    count=open(r'c:\users\zhpeng\desktop\october_sch\img\number.txt','w+')
    count.write(str(x))
    count.close()

    
    print "总计：%s 张"%count_img
      
def new_img_list():
    '''匹配照片末尾005开头的jpg地址，并排序'''
    html=open_html()
    reg=r'src=\\"\S+/(005\S+?\.(?:jpg|gif))\\" '
    imgre=re.compile(reg)
    imglist=re.findall(imgre,html)
    imglist.sort()

    '''
    寻找前后相同的值，并存在rem_val对象中.
    剔除原imglist表中相同部分
    '''
    rem_val=[]
    for i in range(len(imglist)-1):
        if imglist[i]==imglist[i+1]:rem_val.append(imglist[i])
    for i in range(len(rem_val)):imglist.remove(rem_val[i])

    '''对比imglist中与old有否重叠部分'''
    old_f_split=get_old()
    rem_val=[]
    for i in range(len(imglist)):
        if imglist[i] in old_f_split:rem_val.append(imglist[i])
    for i in range(len(rem_val)):imglist.remove(rem_val[i])

    '''此处判断语句，防止old文档末尾会有多个换行符，当imglist为空list，下同'''
    if imglist<>[]:
        old=open(r'old.txt','a+')
        for i in range(len(imglist)):old.write(imglist[i]+'\n')
        old.close() 
    
    return imglist

def cre_dir_img():
    '''匹配照片末尾005开头的jpg地址元组'''
    html=open_html()
    re_picture_name=r'#(\S*?)#.*?&pic_ids=(005\S*?)&'
    picture_name_comp=re.compile(re_picture_name)
    '''元组包含一个中文名称和照片纯地址'''
    picture_name=re.findall(picture_name_comp,html)
    x=0
    count_exist=0
    current_path=os.getcwd()
    for i in picture_name:
        picture_adr=i[1] 
        picture_adr_list=picture_adr.split(',')
        
        picture_adr_list_add_jpg=add_jpg(picture_adr_list)
        
        '''比较照片是否已经下载过'''
        oldlist=get_old()
        new_picture=compare_2(picture_adr_list_add_jpg,oldlist)[0]
        count_exist+=compare_2(picture_adr_list_add_jpg,oldlist)[1]
        if new_picture==[]:
            x+=1
            print '有 %d 位照片就已经存在'%x
            continue
        
        '''useful_picture_adr_list改造成能用URL'''
        useful_picture_adr_list=[]
        for count_i in range(len(new_picture)):
            useful_picture_adr_list.append(r'http://ww4.sinaimg.cn/bmiddle/'+new_picture[count_i])
            
        av_name=i[0].decode('utf-8')
        exist_dir=os.listdir(current_path+'\\img')
        
        '''创造一个用于文件夹是否存在的判断
        因为微软中文编码用的是cp936或者gbk
        所以需要转换一下'''
        av_name_en=av_name.encode('gbk')
                
        '''判断文件夹是否存在，存在不建立，不存在建立'''
        if exist_dir==[]:
            os.mkdir(current_path+'\\img\\%s'%av_name)
            x=0
            urlretrieve(x,useful_picture_adr_list,current_path,av_name)
  
        elif os.path.exists(current_path+'\\img\\%s'%av_name):
            getcount=os.listdir(current_path+'\\img\\%s'%av_name)
            x=len(getcount)
            urlretrieve(x,useful_picture_adr_list,current_path,av_name)

        else:
            os.mkdir(current_path+'\\img\\%s'%av_name)
            x=0
            urlretrieve(x,useful_picture_adr_list,current_path,av_name)

    print '有 %r 张重复'%count_exist
    get_others(current_path)
    

def get_old():
    '''打开照片地址大全'''
    old=open(r'old.txt','r+')
    old_f=old.read()
    old.close()
    old_f_split=old_f.split('\n')
    return old_f_split
    
def compare_2(list1,list2):
    '''比较两个表格中相同部分，并删除重新写入list1中
        list1是新的照片地址
        list2是old文档的list'''
    
    val_rem=[]
    count=0
    
    for i in range(len(list1)):
        if list1[i] in list2:
            val_rem.append(list1[i])
                   
    if val_rem<>[]: 
        for i in range(len(val_rem)):
            list1.remove(val_rem[i])
            count=len(val_rem)
    if list1<>[]:    
        old=open(r'old.txt','a+')
        for i in range(len(list1)):old.write(list1[i]+'\n')
        old.close()
        
    return list1,count
        
def get_others(current_path):
    imglist=new_img_list()
    others_dir=os.listdir(current_path+'\\img')
    if 'others' not in others_dir:
        os.mkdir(current_path+'\\img\\others')
    x=len(os.listdir(current_path+'\\img\\others'))
    for c_c in range(len(imglist)):
        urllib.urlretrieve(r'http://ww4.sinaimg.cn/bmiddle/'+imglist[c_c]
                           ,current_path+'\\img\\others\\%s.%s'%(x,Right(imglist[c_c],3)))
        x+=1

def open_html():
    htm=open('木木萝希木的微博_微博.htm','r')
    html=htm.read()
    htm.close()
    return html

def urlretrieve(x,useful_picture_adr_list,current_path,av_name):
    for c_c in range(len(useful_picture_adr_list)):
        urllib.urlretrieve(useful_picture_adr_list[c_c],
                           current_path+'\\img\\%s\\%s.%s'%(av_name,x,Right(useful_picture_adr_list[c_c],3)))
        x+=1

def add_jpg(picture_adr_list):
    picture_adr_list_add_jpg=[]
    for add_jpg_i in range(len(picture_adr_list)):
        picture_adr_list_add_jpg.append(picture_adr_list[add_jpg_i]+'.jpg')
    return picture_adr_list_add_jpg
#getimg()
cre_dir_img()

    

