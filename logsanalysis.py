#!/usr/bin/env python3

# The Python program answering to 3 questions

import psycopg2

try:
    db = psycopg2.connect("dbname=news")
except psycopg2.Error as e:
    print(e.pgerror)

curr = db.cursor()

query1 = '''select articles.title, count(log.id) as num_logs
    from log, articles
    where log.path = concat('/article/', articles.slug)
    group by articles.title
    order by num_logs desc
    limit 3;
'''

query2 = '''select authors.name, count(log.id) as num_logs
    from log, articles, authors
    where log.path = concat('/article/', articles.slug)
    and articles.author=authors.id
    group by authors.name
    order by num_logs desc;
'''

query3 = '''select TO_CHAR(time::date, 'Mon DD, YYYY'), percent from
    (select requests.time::date,
    round(100.0*errors.errors_number/requests.total_requests,1)
    as percent
    from requests, errors
    where errors.time::date = requests.time::date)as
    pp where percent > 1;
'''

print('QUERY 1')
curr.execute(query1)
result = curr.fetchall()
for (title, count) in result:
    print("\t {} - {} views".format(title, count))
print("-" * 70)

print('QUERY 2')
curr.execute(query2)
result_q2 = curr.fetchall()
for (title, count) in result_q2:
    print("\t {} - {} views".format(title, count))
print("-" * 70)

print('QUERY 3')
curr.execute(query3)
result_q3 = curr.fetchall()
for (date, percent) in result_q3:
    print("\t {} - {}% errors".format(date, percent))
print("-" * 70)

curr.close()
db.close()
