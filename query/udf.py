
import re

def rlike(s,pattern):
    return re.search(pattern,s) is not None

def split(s,sep,idx):
    return s.split(sep=sep)[idx]

def if_(exp,vt,vf):
    # 注意,这里if对空值会返回false,不一定满足要求
    if exp:
        return vt
    else:
        return vf

# udf容器,管理常用的udf
udfs = [
    ("rlike",rlike),
    ("split",split),
    ("if",if_)
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
    

    

