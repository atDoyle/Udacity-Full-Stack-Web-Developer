import psycopg2
import calendar


DBNAME = "news"


def get_errors():
    """Return dates where more thann 1% of requests lead to errors."""
    sql = ("select * "
           "from "
           "(select total_table.date, "
           "errors, "
           "total, "
           "errors/total as percentage "
           "from "
           "(select "
           "cast(time as date) as date, "
           "cast(count(*) as float) as errors "
           "from log "
           "where status != '200 OK' "
           "group by date) "
           "as error_table "
           "inner join "
           "(select cast(time as date) as date, "
           "cast(count(*) as float) as total "
           "from log group by date) as total_table "
           "on error_table.date = total_table.date "
           "order by percentage desc) as perc_table "
           "where percentage > .01;"
           )
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql)
    errors = c.fetchall()
    colnames = [desc[0] for desc in c.description]
    colnames[3] = 'Error Percentage'
    db.close()
    return colnames, errors


def nice_print(results):
    """Print in a nice way."""
    fh = open('get_errors.txt', 'w')
    fh.write(results[0][0].title() + ' | ' + results[0][3].title())
    print results[0][0].title(), "|", results[0][3].title()
    for i in range(len(results[1])):
        print '{} {}, {} | {:04.2f}%'.format(
            calendar.month_name[results[1][i][0].month],
            results[1][i][0].day,
            results[1][i][0].year,
            100 * results[1][i][3]
            )
        fh.write('\n{} {}, {} | {:04.2f}%'.format(
            calendar.month_name[results[1][i][0].month],
            results[1][i][0].day,
            results[1][i][0].year,
            100 * results[1][i][3]
            ))
    fh.close()


nice_print(get_errors())
