# Logs analysis
### Description
logsanalysis.py is a simple reporting tool that uses information from the database and prints out reports to the command line.
This reporting tools answers 3 questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### Database setup
To access to the database you should follow the steps:
1. Download and unzip [the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
2. Put this file into the `vagrant` shared directory.
3. `cd` into the `vagrant` directory.
4. Load the data using the command `psql -d news -f newsdata.sql`
5. Connect to the database using `psql -d news`

### Database description
The `news` database consists of 3 tables:
##### Articles
| Field name | datatype |
| --- | --- |
| id | integer|
| author | integer |
| title | text |
| slug | text |
| lead | text |
| body | text |
| time | timestamptz |

##### Authors
| Field name | datatype |
| --- | --- |
| id | integer |
| name | text |
| bio | text |
##### Logs
| Field name | datatype |
| --- | --- |
| path | text |
| ip | integer |
| method | text |
| status | text |
| time | timestamptz |
| id | integer | 

### How to run
To run the reporting tool the next command should be written to the command line:

```python logsanalysis.py ```

### View defifnitions
To answer the question #3 two views were created:

1. Errors: the view contains the number of requests with the status "404 NOT FOUND" groupped by day.
```sql
create view errors as
  select status, time::date, count(id) as errors_number 
  from log 
  where status != '200 OK' 
  group by time::date, status;
```
2. Requests: the view contains the total number of requests by day
```sql 
create view requests as
  select time::date, count(id) as total_requests
  from log
  group by time::date;
```