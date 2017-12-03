#!/usr/bin/env python3

import psycopg2


DBNAME = "news"


def get_articles():
    """Return the 3 most read articles."""
    sql = ("select articles.title as article, count(*) as views "
           "from (articles inner join log on log.path "
           "like concat('%', articles.slug)) "
           "where log.status = '200 OK' "
           "group by articles.title "
           "order by views desc limit 3;"
           )
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql)
    articles = c.fetchall()
    colnames = [desc[0] for desc in c.description]
    db.close()
    return colnames, articles


def nice_print(results):
    """Print in a nice way."""
    fh = open('get_articles.txt', 'w')
    fh.write(results[0][0].title() + ' | ' + results[0][1].title())
    print results[0][0].title(), "|", results[0][1].title()
    for i in range(len(results[1])):
        print '{} | {:,d} Views'.format(
            results[1][i][0],
            results[1][i][1]
            )
        fh.write('\n{} | {:,d} Views'.format(
            results[1][i][0],
            results[1][i][1]
            ))
    fh.close()


nice_print(get_articles())
