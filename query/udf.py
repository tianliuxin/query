
import re

def rlike(s,pattern):
    return re.search(pattern,s) is not None

def split(s,sep,idx):
    return s.split(sep=sep)[idx]

# udf容器,管理常用的udf
udfs = [
    ("rlike",rlike),
    ("split",split)
]

def init_udfs(query):
    '''注册常用的udf函数
    
    Paramaters
    ----------
    query:
        query实例,需要支持udf,当前是SQuery实例
    '''
    for name,fn in udfs:
        query.udf(name,fn)
    

    

