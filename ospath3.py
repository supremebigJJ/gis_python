# -*- coding: utf-8 -*-
# 生成文件夹中所有子目录的路径到txt
import os
from pathlib import Path

def listdir(basepath, file_path, file_name):
    for entry in basepath.iterdir():
        if entry.is_dir():
            print(entry.name)
            name = entry.name
            file_name.append(name)
            fpath = os.path.join(basepath, name)
            file_path.append(fpath)

file_name=[]
file_path=[]
basepath = Path('D:\py')
listdir(basepath, file_path, file_name)

with open('D:/py/list.txt','w') as f:     #要存入的txt
    write=''
    for i,h in zip(file_path,file_name):
         write=write+str(h)+'='+str(i)+'\n'
    f.write(write)        