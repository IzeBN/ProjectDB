
SELECT_SALE_OR_AGREEMENT = """--sql
                            SELECT 
                                {table}.{table}_id,
                                cl.*,
                                cl_doc.document_type,
                                cl_doc.data,
                                cl_doc.issued_date,
                                cl_doc.issued_by,
                                em.*,
                                em_doc.document_type,
                                em_doc.data,
                                em_doc.issued_date,
                                em_doc.issued_by,
                                pr.*,
                                {table}.date
                            FROM {table}
                                JOIN employee AS em ON em.employee_id = {table}.employee_id
                                JOIN client AS cl ON cl.client_id = {table}.client_id
                                JOIN product AS pr ON pr.product_id = {table}.product_id
                                JOIN document AS cl_doc ON cl_doc.document_id = cl.document_id
                                JOIN document AS em_doc ON em_doc.document_id = em.document_id
                            {filter}
                            """
                            
SELECT_USER = """--sql
            SELECT 
                {table}.*,
                doc.document_type,
                doc.data,
                doc.issued_date,
                doc.issued_by
            FROM {table}
                JOIN document as doc ON doc.document_id = {table}.document_id
            {filter}
            """
            
def SELECT_ALL(table):
    return f'SELECT * FROM {table}'