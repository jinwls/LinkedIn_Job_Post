from itemadapter import ItemAdapter
import psycopg2



class JobPostgreSQL(object):

    def __init__(self):
        self.get_connection()


    def get_connection(self):
        # enter your database, userid, password here
        self.conn = psycopg2.connect(
                host = 'localhost',
                dbname = 'LinkedinPost',
                user = 'postgres',
                password = 'password'
            )
        self.cur = self.conn.cursor()


    def close_spider(self):
        self.cur.close()
        self.conn.close()
    

    def process_item(self, item, spider):

        try:
            self.cur.execute(f"insert into public.JobPost(job, company, city, states, dateposted, jobtype, joblevel, jobindustry, jobfunction, jobdetail) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(
                item['job'],
                item['company'],
                item['city'],
                item['state'],
                item['date'],
                item['type'],
                item['level'],
                item['industry'],
                item['function'],
                item['detail']))
            
            # remove duplicates 
            self.cur.execute("""
                    DELETE FROM public.JobPost a
                        USING   public.JobPost b
                    WHERE   a.id < b.id 
                        AND a.job = b.job
                        AND a.company = b.company
                        AND a.dateposted = b.dateposted
                        AND a.city = b.city
                        AND a.states = b.states
                        AND a.joblevel = b.joblevel;
                    """)
            self.conn.commit()
        except psycopg2.DatabaseError:
            print("Error in transaction")
            self.conn.rollback()
        return item


