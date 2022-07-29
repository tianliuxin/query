import query

sq = query.SQuery()

f = r"C:\Users\qq162\Desktop\销售BI报表\商机表_数据源.xlsx"

df = query.read_excel(f)

sq.register("df",df)

print(sq.show_create_table("df"))
sq.sql("""
select * from df limit 10
""")

def foo(a,*args):
    args = [a,*args]
    args = [str(i) for i in args]
    return ",".join(args)

sq.udf("foo",foo)


from bisect import bisect_left,bisect_right
# 二分搜索查找区间(具体的算法实现忘了,后面可以看看)
bisect_left([0,2,4,6,8],2)
bisect_right([0,2,4,6,8],9)

def lcut():
    '''左开右闭,也可以通过维度表实现'''
    pass
