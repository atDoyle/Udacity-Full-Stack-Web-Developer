#!/usr/bin/env python3

import psycopg2


DBNAME = "news"


def get_authors():
    """Return the most popular authors."""
    sql = ("select authors.name as author, count(*) as views "
           "from (authors inner join articles "
           "on (authors.id = articles.author) inner join log "
           "on log.path "
           "like concat('%', articles.slug)) "
           "where log.status = '200 OK' "
           "group by authors.name order by views desc;"
           )
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql)
    authors = c.fetchall()
    colnames = [desc[0] for desc in c.description]
    db.close()
    return colnames, authors


def nice_print(results):
    """Print in a nice way."""
    fh = open('get_authors.txt', 'w')
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

nice_print(get_authors())
