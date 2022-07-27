'''
实现df和sqlite数据库间的转换,并暴露pandas的io接口,方便数据处理

Author:liu.xin
Date:2022.02.22
'''


import sqlite3
from pandas.io.api import read_sql, read_csv, read_clipboard, read_excel, read_json
from pandas.core.api import DataFrame,Series

class BaseQuery:
    '''Query基类,暂时没有实现,后期改进时可能会进行实现'''
    pass
_conn = sqlite3.connect(":memory:")  # 定义全局的内存数据库,载入时初始化,若重新载入,则会丢失数据

class Query(BaseQuery):
    def __init__(self,con):
        self.con = _conn
    
    def execute(self,sql:str):
        '''执行sql,返回游标或者记录集'''

        # 尝试执行exccutemany,若没有该方法,则按;分割,分别执行
        try:
            cursor = self.con.executemany(sql)
        except Exception:
            cursors = [self.con.execute(s) for s in sql.split(";")]
            cursor = cursors[-1]
        return cursor
    
    def sql(self,sql,chunksize=None) -> DataFrame:
        '''chunksize:指定后返回iterator'''
        df = read_sql(sql=sql,con=self.con,chunksize=chunksize)
        return df
    
    def register(self,df:DataFrame,name:str,if_exits="replace",dtype=None):
        df.to_sql(name=name,con=self.con,if_exists=if_exits,dtype=dtype)
    

class SQuery(Query):
    def __init__(self,con:sqlite3.Connection):
        super().__init__(con)
    
    def udf(self,name,fn):
        '''自定义函数'''
        self.con.create_function(name,-1,fn)
    
    def udf_agg(self,name,agg_cls):
        '''自定义聚合类

        Parameters
        ----------
        name:str
            注册的聚合函数名
        agg_class:object
            自定义的聚合类,必须实现step方法和finalize方法
        
        Examples:
        --------
        >>> class MySum:
        ...     def __init__(self):
        ...         self.total = 0
        ...
        ...     def step(self,name,score):
        ...         if name == "liuxin":
        ...             self.total += score
        ...
        ...     def finalize(self):
        ...         return self.total
        >>> udf_agg("mysum",MySum)
        '''
        self.con.create_aggregate(name,-1,agg_cls)

    def tables(self):
        '''返回数据库中的表名'''
        tables = self.con.execute(
            "select name from sqlite_master where type='table' order by name").fetchall()
        tables = [table[0] for table in tables]
        return tables

        

create_df = DataFrame
create_ts = Series

def udf(name,fn):
    _conn.create_function(name,-1,fn)

def udf_agg(name,agg_class):
    '''自定义聚合类
    
    Parameters
    ----------
    name:str
        注册的聚合函数名
    agg_class:object
        自定义的聚合类,必须实现step方法和finalize方法
    
    Examples:
    --------
    >>> class MySum:
    ...     def __init__(self):
    ...         self.total = 0
    ...
    ...     def step(self,name,score):
    ...         if name == "liuxin":
    ...             self.total += score
    ...
    ...     def finalize(self):
    ...         return self.total
    >>> udf_agg("mysum",MySum)
    '''
    _conn.create_aggregate(name,-1,agg_class)


def register(**kwargs):
    '''登记df到sqlite数据库'''
    for name, df in kwargs.items():
        df.to_sql(name, con=_conn, index=False, if_exists='replace')


def drop_tables(*names):
    '''取消登记'''
    for name in names:
        _conn.execute(f"drop table {name}")


def sql(sql):
    '''执行sql语句'''
    return _conn.execute(sql)


def df(*names, sql=None):
    '''返回df

    Parameters
    ----------
    names:List[str]
        返回数据库中为name的表
    sql:str
        通过sql语句查询数据库中数据
    sql和names仅能够使用其中一个(python没有重载,否则可以使用重载做)

    Returns
    -------
    List[DataFrame]
    DataFrame
    '''
    if len(names) > 0 and sql is not None:
        raise TypeError("names or sql only one could be used")
    if sql is None:
        dfs = [read_sql(f"select * from {name}", con=_conn) for name in names]
        if len(dfs) == 1:
            return dfs[0]
        return dfs
    return read_sql(sql, con=_conn)


def tables():
    '''返回数据库中的表名'''
    tables = _conn.execute(
        "select name from sqlite_master where type='table' order by name").fetchall()
    tables = [table[0] for table in tables]
    return tables
