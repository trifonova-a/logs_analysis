#!/usr/bin/env python3
#
#The Python program answering to 3 questions

import psycopg2

try:
	db = psycopg2.connect("dbname=news")
except:
	print("Unable to connect to the database")

curr = db.cursor()

query1 = '''select articles.title, count(log.id) as num_logs 
	from log, articles
	where log.path like '%' ||articles.slug|| '%' 
	group by articles.title
	order by num_logs desc
	limit 3;
'''

query2 = '''select authors.name, count(log.id) as num_logs
	from log, articles, authors
	where log.path like '%' ||articles.slug|| '%'
	and articles.author=authors.id
	group by authors.name
	order by num_logs desc;
'''

query3 = '''select time::date, percent from 
	(select requests.time::date, 
	round(100*errors.errors_number::decimal/requests.total_requests,1) as percent
	from requests, errors
	where errors.time::date = requests.time::date)as
	pp where percent > 1;
'''

print('QUERY 1')
curr.execute(query1)
result = curr.fetchall()
for elem in result:
	print(str(elem[0]) + ' - ' + str(elem[1]) + ' views')
print('\n')

print('QUERY 2')
curr.execute(query2)
result_q2 = curr.fetchall()
for elem in result_q2:
	print(str(elem[0]) + ' - ' + str(elem[1]) + ' views')
print('\n')

print('QUERY 3')
curr.execute(query3)
result_q3 = curr.fetchall()
for elem in result_q3:
	print(str(elem[0].strftime('%B %d, %Y')) + ' - ' + str(elem[1]) + '% errors')
print('\n')

curr.close()
db.close()


"""query 3
create view errors as
 select status, time::date, count(id) as errors_number 
 from log 
 where status='404 NOT FOUND' 
 group by time::date, status;

 create view requests as
  select time::date, count(id) as total_requests
  from log
  group by time::date;

"""