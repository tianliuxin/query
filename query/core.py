
import sqlite3
from .io import read_sql,DataFrame
from .udf import init_udfs


class BaseQuery:
    '''Query基类,暂时没有实现,后期改进时可能会进行实现'''
    pass

class Query(BaseQuery):
    '''更通用的Query对象'''

    def __init__(self,con):
        '''
        Parameters
        ----------
        con:
            常见数据库的connect对象,由于使用了pandas的read_sql,
            因此最好是使用sqlite或者sqlalchemy的engine
        '''
        self.con = con
    
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
    
    def register(self,name:str,df:DataFrame,if_exits="replace",dtype=None):
        df.to_sql(name=name,con=self.con,if_exists=if_exits,dtype=dtype,index=False)
    

class SQuery(Query):
    '''sqlite作为数据库的Query对象,支持udf等'''

    def __init__(self,con=None,is_initial_udfs=True):
        '''
        Parameters
        ----------
        con:
            sqlite的Connection对象,或者None对象,当为None,则返回构建sqlite内存数据库
        is_initial_udfs:
            是否初始化自定义的常用udf,默认是True
        '''
        if con is None:
            con = sqlite3.connect(":memory:")
        super().__init__(con)

        self.udfs = {} # 记录注册的udf函数
        if is_initial_udfs:
            init_udfs(self)
    
    def udf(self,name,fn):
        '''注册自定义函数'''
        self.udfs[name] = fn
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

        TODO:
        --------
        能否改成函数实现
        '''
        self.con.create_aggregate(name,-1,agg_cls)

    def tables(self):
        '''返回数据库中的表名'''
        tables = self.con.execute(
            "select name from sqlite_master where type='table' order by name").fetchall()
        tables = [table[0] for table in tables]
        return tables
    
    def show_create_table(self,name):
        '''显示建表语句'''
        cursor = self.con.execute("select `sql` from sqlite_master where type='table' and tbl_name='{}'".format(name))
        stmt = cursor.fetchone()[0]
        return stmt
    
    def close(self):
        self.con.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self,exc_type,exc_value,exc_tb):
        self.close()

        

