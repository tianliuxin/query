# query用途
query通过将DataFrame存储至sqlite内存数据库,使用户可以使用sql来操作数据

# How To Use
```python
import query
# 创建DataFrame,Series
# 方式一:create_df,create_ts直接创建
# 方式二:read_excel,read_sql,read_csv,read_json,read_clipboard通过IO创建
df = query.create_df({
    "name":['liuxin','liuxin','spark'],
    'score':[10,20,30]
})

f = ''
df_excel = query.read_excel(f)

# 将df存储至sqlite
query.register(df=df)

# 使用sql语句,返回的是cursor
query.sql("create table df_agg as select name,sum(score) as total from df group by name")

# 查看数据库表
print(query.tables())

# 使用query.df获取数据库中数据,返回DataFrame
# 方式一:通过表名来获取数据
# 方式二:通过sql来获取数据
# 注:这两种方式仅支持一种,不能同时使用
df_agg = query.df('df_agg')
print(df_agg)
df_agg_2 = query.df(sql="select name,sum(score) as total from df group by name")

# 删除数据库中表格
query.drop_tables('df_agg')
```

# TODO
- [ ] 对conn对象进行close
- [ ] udf定义为装饰器
- [ ] udf_agg必须跟原定义的一样,需要传递类(定义了step和finalize方法),能否将这个构造为函数,合并到udf里
- [ ] 学习pytest,编写测试用例
- [ ] duckdb替代sqlite,优化计算速度(暂时不行,duckdb存在太多bug,结果不准确!!!)

# Problems
1. 对于存在缺失值的,pandas可能采用object来存储,此时写入sqlite可能会当文本处理,原本的数值可能被当二进制存储