import asyncpg as sq
from uuid import uuid4
from time import time

class Database:
    
    def __init__(self, dsn) -> None:
        self.__is_connection: bool = False
        self.__db = None
        self.__dsn = dsn
        
    async def __connect(self):
        self.db = await sq.create_pool(
            dsn=self.__dsn,
            min_size=50,
            max_size=100
        )
        self.__is_connection = True
    
    def check_db_connect(method):
        """Async decorator by db connect"""
        async def wrapper(self, *args, **kwargs):
            if not self.__is_connection:
                await self.__connect()
            return await method(self, *args, **kwargs) 
        return wrapper
    
    @check_db_connect
    async def create_tables(self):
        async with self.db.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """--sql
                    CREATE TABLE IF NOT EXISTS job_title(job_id VARCHAR(128) PRIMARY KEY,
                                                        title VARCHAR(256),
                                                        salary INT);

                    CREATE TABLE IF NOT EXISTS document(document_id VARCHAR(128) PRIMARY KEY,
                                                        document_type VARCHAR(128),
                                                        data VARCHAR(256),
                                                        issued_date BIGINT,
                                                        issued_by VARCHAR(256));

                    CREATE TABLE IF NOT EXISTS employee(employee_id VARCHAR(128) PRIMARY KEY,
                                                        name VARCHAR(64),
                                                        lastname VARCHAR(64),
                                                        fatherly VARCHAR(64),
                                                        date_birth BIGINT,
                                                        phone_number BIGINT,
                                                        addres VARCHAR(256),
                                                        citizenship VARCHAR(64),
                                                        job_title_id VARCHAR(128),
                                                        sales_count INT,
                                                        date_acceptance BIGINT,
                                                        experience INT,
                                                        schedule VARCHAR(32),
                                                        document_id VARCHAR(128),
                                                        FOREIGN KEY (job_title_id) REFERENCES job_title(job_id),
                                                        FOREIGN KEY (document_id) REFERENCES document(document_id));

                    CREATE TABLE IF NOT EXISTS client(client_id VARCHAR(128) PRIMARY KEY,
                                                      name VARCHAR(32),
                                                      lastname VARCHAR(32),
                                                      fatherly VARCHAR(32),
                                                      date_birth BIGINT,
                                                      phone_number BIGINT,
                                                      addres VARCHAR(256),
                                                      place_work VARCHAR(256),
                                                      TIN BIGINT,
                                                      bank_card BIGINT,
                                                      count_purchases INT,
                                                      document_id VARCHAR(128),
                                                      FOREIGN KEY (document_id) REFERENCES document(document_id));

                    CREATE TABLE IF NOT EXISTS product(product_id VARCHAR(128) PRIMARY KEY,
                                                       title VARCHAR(256),
                                                       description VARCHAR(1028),
                                                       date_release BIGINT,
                                                       cost INT,
                                                       count_sales INT,
                                                       serial_number VARCHAR(256));

                    CREATE TABLE IF NOT EXISTS sale(sale_id VARCHAR(128) PRIMARY KEY,
                                                     client_id VARCHAR(128),
                                                     employee_id VARCHAR(128),
                                                     product_id VARCHAR(128),
                                                     date BIGINT,
                                                     FOREIGN KEY (client_id) REFERENCES client(client_id),
                                                     FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
                                                     FOREIGN KEY (product_id) REFERENCES product(product_id));

                    CREATE TABLE IF NOT EXISTS agreement(agreement_id VARCHAR(128) PRIMARY KEY,
                                                         employee_id VARCHAR(128),
                                                         client_id VARCHAR(128),
                                                         product_id VARCHAR(128),
                                                         date BIGINT,
                                                         FOREIGN KEY (client_id) REFERENCES client(client_id),
                                                         FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
                                                         FOREIGN KEY (product_id) REFERENCES product(product_id));
                    """
                )
                
    @check_db_connect
    async def __add_document(self, doc_type, data, issue_date, issue_by):
        async with self.db.acquire() as conn:
            document = await conn.fetchval("""--sql
                                           SELECT document_id FROM document WHERE document_type = $1 AND data = $2""", doc_type, data)
            if not document:
                async with conn.transaction():
                    new_document_uuid = str(uuid4())
                    await conn.execute("""--sql
                                       INSERT INTO document VALUES($1, $2, $3, $4, $5)""", new_document_uuid, doc_type, data, issue_date, issue_by)
                    return new_document_uuid
            return document
        
    @check_db_connect
    async def __add_job_title(self, title, salary):
        async with self.db.acquire() as conn:
            job_id = await conn.fetchval("""--sql
                                         SELECT job_id FROM job_title WHERE title = $1 AND salary = $2""", title, salary)
            if not job_id:
                async with conn.transaction():
                    new_job_uuid = str(uuid4())
                    await conn.execute("""--sql
                                    INSERT INTO job_title VALUES($1, $2, $3)""", new_job_uuid, title, salary)
                    return new_job_uuid
            return job_id
                
    @check_db_connect
    async def add_employee(self, job_title, job_salary, doc_type, doc_data, doc_issue_date, doc_issue_by,
                           name, lastname, fatherly, date_birth, phone_number, addres, citizenship, experince, schedule):
        job_id = await self.__add_job_title(job_title, job_salary)
        document_id = await self.__add_document(doc_type, doc_data, doc_issue_date, doc_issue_by)
        async with self.db.acquire() as conn:
            last_employee_id = await conn.fetchval("""--sql
                                                SELECT employee_id FROM employee WHERE document_id = $1 AND job_title_id = $2""", document_id, job_id)
            async with conn.transaction():
                if not last_employee_id:
                    new_employee_id = str(uuid4())
                    await conn.execute("""--sql
                                       INSERT INTO employee VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)""",
                    new_employee_id, name, lastname, fatherly, date_birth, phone_number, addres, citizenship, job_id, 0, int(time()), experince, schedule)
                    return new_employee_id
            return last_employee_id
    
    @check_db_connect
    async def add_client(self, doc_type, doc_data, doc_issue_date, doc_issue_by,
                         name, lastname, fatherly, date_birth, phone_number, addres, place_work, tin, bank_card, count_purchases):
        document_id = await self.__add_document(doc_type, doc_data, doc_issue_date, doc_issue_by)
        async with self.db.acquire() as conn:
            client_id = await conn.fetchval("""--sql
                                            SELECT client_id FROM client WHERE document_id = $1""", document_id)
            async with conn.transaction():
                if not client_id:
                    new_client_id = str(uuid4())
                    await conn.execute("""--sql
                                       INSERT INTO client VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)""",
                    new_client_id, name, lastname, fatherly, date_birth, phone_number, addres, place_work, tin, bank_card, count_purchases, document_id)
                    return new_client_id
                
            return client_id
        
        
        
async def main():
    db = Database('postgresql://izeb:izeb@localhost:5432/main')
    
    await db.create_tables()
    
    print('OK')
    
    await asyncio.sleep(10)
    
    
import asyncio

asyncio.run(main())