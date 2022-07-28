# test file

import query

df = query.create_df({
    "name":['a','b','c'],
    "score":[10,20,30]
})
sq = query.SQuery()
sq.register("df",df)

df_agg = sq.sql("select sum(score) from df")

print(df_agg)
