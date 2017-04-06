import psycopg2
import getpass
import time
from collections import defaultdict


def timeDec(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print '%r %2.2f sec' % (method.__name__, te - ts)
        return result
    return timed


class PostgresDb(object):
    def __init__(self, host, db_name):
        self.params = {
            'dbname': db_name,
            'user': raw_input('User name (%s):' % db_name).lower(),
            'password': getpass.getpass('Password (%s):' % db_name),
            'host': host,
            'port': 5432
        }
        self.dbConnect()

    def dbConnect(self):
        self.conn = psycopg2.connect(**self.params)

    def dbClose(self):
        self.conn.close()
        
    def query(self, qry, columns=False):
        cur = self.conn.cursor()
        qry = qry.replace('%', '%%')
        qry = qry.replace('-pct-', '%')
        try:
            cur.execute(qry)
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                data = cur.fetchall()
            else:
                data = None
                columns = None
                self.conn.commit()
                print 'Update sucessfull'
            del cur
            if columns:
                return data, columns
            else:
                return data
        except:
            print 'Query Failed:\n'
            for i in qry.split('\n'):
                print '\t{0}'.format(i)
            self.conn.rollback()
            del cur


def data_to_dict_data(data, columns):
    dictdata = defaultdict(list)
    for row in data:
        # loop through columns to get index
        for c in range(len(columns)):
            # add row's value by index to dict
            dictdata[columns[c]].append(row[c])
    return dictdata

                     

    
    