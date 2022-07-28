# query用途
query通过将DataFrame存储至sqlite内存数据库,使用户可以使用sql来操作数据

# 使用方式
```python
import query

sq = query.SQuery()
# 创建DataFrame,Series
# 方式一:create_df,create_ts直接创建
# 方式二:read_excel,read_sql,read_csv,read_json,read_clipboard通过IO创建
df = query.create_df({
    "name":['liuxin','liuxin','spark'],
    'score':[10,20,30]
})

f = ''
df_excel = query.read_excel(f,dtype=str) # 推荐使用字符串方式读,一方面是sqlite弱类型,处理起来比较方便,另一方面是类型处理比较繁琐

# 将df存储至sqlite
sq.register("df",df)

# 使用sql语句,返回的是cursor
sq.sql("create table df_agg as select name,sum(score) as total from df group by name")

# 查看数据库表
print(sq.tables())

# 查看表结构
print(sq.show_create_table("df"))
```

# TODO
- [ ] udf_agg必须跟原定义的一样,需要传递类(定义了step和finalize方法),能否将这个构造为函数,合并到udf里
- [ ] duckdb替代sqlite,优化计算速度(暂时不行,duckdb存在太多bug,结果不准确!!!若存在其他更好的计算引擎也可以尝试)
