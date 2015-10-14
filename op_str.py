# -*- coding:utf-8 -*-
import re
__all__=['Right']
'''类似EXCEL中left，middle，right函数'''

def Right(string,length):
    right=''
    r1=r'.'
    r1_com=re.compile(r1)
    str_list=re.findall(r1_com,string)
    i=len(string)
    if 0<length<=i:
        for j in range(i-length,i):
            right+=str_list[j]
    return right
