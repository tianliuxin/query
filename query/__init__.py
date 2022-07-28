import sqlite3

from .io import (
    create_df,create_ts,read_sql,read_csv,read_excel,read_clipboard,read_json
)

from .core import (
    Query,SQuery
)

# 初始化sqlite内存数据库
sq = SQuery(con=sqlite3.connect(":memory:"))
