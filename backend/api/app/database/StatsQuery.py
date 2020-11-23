from app.database.db import db, BaseModelMixin
from datetime import datetime
from ..common.error_handling import ObjectNotFound
from sqlalchemy import func


def jobsPerCategoryStats():
    res = db.engine.execute('select c."name", count(j) as "value" from category as c, job as j, subcategory as s where j.subcategory_id = s.id and s.category_id = c.id group by c."name"')
    return [row for row in res]

def postulationsXInterviewsStats():
    res = db.engine.execute('select coalesce(DATE(a.created_at), DATE(i.created_at)) as "day", count(distinct a) as "applications", count(distinct i) as "interviews" from application as a FULL OUTER JOIN interview as i ON DATE(a.created_at) = DATE(i.created_at) group by DATE(a.created_at), DATE(i.created_at) order by day limit 30')
    return [row for row in res]

def popularSearches():
    sqlQuery = 'select s.text, count(s.text) '
    sqlQuery += 'from search as s '
    sqlQuery += 'where s.created_at between (now() - interval ' + "'30 days'" + ') and now() '
    sqlQuery += 'and s.text IS NOT NULL '
    sqlQuery += 'and s.text != ' + "'' "
    #TODO en PGADMIN lo hace bien, el problema es cuando se envia desde aca, solucionar
    #sqlQuery += "and s.text not like ' %' "
    sqlQuery += "group by s.text "
    sqlQuery += "order by count(s.text) desc "
    sqlQuery += "limit 10 "

    res = db.engine.execute(sqlQuery)
    #res = db.engine.execute('select s.text, count(s.text) from search as s where s.created_at between (now() - interval ' + "'30 days'" + ') and now() and s.text IS NOT NULL and s.text != ' + "''" + ' and s.text not like ' + "' %'" + ' group by s.text order by count(s.text) desc limit 10')
    return [row for row in res]

def median(category_id):
    sqlQuery = "select j.salary as mediana " 
    sqlQuery += "from job as j " 
    sqlQuery += "where j.salary <> 111111 " 
    sqlQuery += "and j.active = true " 
    sqlQuery += "and j.subcategory_id = " + str(category_id) + " " 
    sqlQuery += "and j.url like '%computrabajo%' " 
    sqlQuery += "or j.url like '%mipleo%' " 
    sqlQuery += "order by j.salary " 
    sqlQuery += "limit 1 " 
    sqlQuery += "offset ((" 
    sqlQuery += "select count(j.salary) " 
    sqlQuery += "from job as j " 
    sqlQuery += "where j.active = true "
    sqlQuery += "and j.salary <> 111111 " 
    sqlQuery += "and j.salary is not null " 
    sqlQuery += "and j.subcategory_id = " + str(category_id) + " " 
    sqlQuery += "and j.url like '%computrabajo%' " 
    sqlQuery += "or j.url like '%mipleo%'" 
    sqlQuery += ") / 2)" 
    print(sqlQuery)
    res = db.session.execute(sqlQuery)
    return [row for row in res]

def medianFreelance(category_id):
    sqlQuery = "select j.salary as mediana " 
    sqlQuery += "from job as j " 
    sqlQuery += "where j.salary <> 111111 " 
    sqlQuery += "and j.active = true " 
    sqlQuery += "and j.subcategory_id = " + str(category_id) + " " 
    sqlQuery += "and j.url like '%workana%' " 
    sqlQuery += "order by j.salary " 
    sqlQuery += "limit 1 " 
    sqlQuery += "offset ((" 
    sqlQuery += "select count(j.salary) " 
    sqlQuery += "from job as j " 
    sqlQuery += "where j.active = true "
    sqlQuery += "and j.salary <> 111111 " 
    sqlQuery += "and j.salary is not null " 
    sqlQuery += "and j.subcategory_id = " + str(category_id) + " " 
    sqlQuery += "and j.url like '%workana%'" 
    sqlQuery += ") / 2)" 
    res = db.session.execute(sqlQuery)
    return [row for row in res]