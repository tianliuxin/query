import query

# df = query.create_df({
#     "name":['liuxin','liuxin','spark'],
#     'score':[10,20,30]
# })

f = r"C:\Users\qq162\Desktop\tmp\商机表_数据源.xlsx"
df = query.read_excel(f,dtype="str")
query.register(df=df)

query.sql("create table df_agg as select name,sum(score) as total from df group by name")

print(query.tables())

df_agg = query.df('df_agg')
print(df_agg)

import re
def rlike(s:str,pattern:str):
    return re.search(pattern,s) is not None

query.udf("rlike",rlike)

import numpy as np
import pandas as pd
dfk = pd.DataFrame({
    "a":np.random.randint(0,100,int(1e8))
})

query.register(dfk=dfk)

def double(x):
    return x*2

query.udf("double",double)