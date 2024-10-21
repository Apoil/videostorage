import sqlite3
#2、数据库文件
db_file = 'db.sqlite3'
#3、获取与数据库的连接
conn = sqlite3.connect(db_file)
#4、编写sql语句
sql='select title from videos_video'
#5、执行sql语句
cur=conn.cursor()
cur.execute(sql)
#6、打印结果
print(cur.fetchall())
#7、关闭连接
conn.close()