from dataclasses import dataclass


@dataclass
class Document:
    id: str
    type: str
    data: str
    issue_date: int
    issue_by: str
    
@dataclass
class JobTitle:
    id: str
    title: str
    salary: int
    
@dataclass
class Client:
    id: str
    name: str
    lastname: str
    fatherly: str
    date_birth: int
    phone_number: int
    addres: str
    place_work: str
    tin: int
    bank_card: int
    count_purchases: int
    document: Document
         
    
@dataclass
class Employee:
    id: str
    name: str
    lastname: str
    fatherly: str
    date_birth: int
    phone_number: int
    addres: str
    citizenship: str
    job_tittle: JobTitle
    sales_count: int
    date_acceptance: int
    experince: int
    schedule: str
    document: Document
    
    
@dataclass
class Product:
    id: str
    title: str
    description: str
    date_release: int
    cost: int
    count_sales: int
    serial_number: str
    
    
@dataclass
class Agreement:
    id: str
    employee: Employee
    client: Client
    product: Product
    date_conclusions: int
    
@dataclass
class Sale:
    id: str
    client: Client
    employee: Employee
    product: Product
    date: int
    
@dataclass
class Users:
    employes: list[Employee]
    clients: list[Client]

async def UserForm(list, user_type: str):
    return [Employee(*args[0:-6], document=Document(*args[-6:-1])) for args in list] \
        if user_type == 'employee' else \
            [Client(*args[0:-6], document=Document(*args[-6:-1])) for args in list]
        
async def SaleForm(*args):
    return Sale(
        id=args[0],
        client=Client(*args[1:12],
                      document=Document(*args[12:17])),
        employee=Employee(*args[17:30],
                          document=Document(*args[30:35])),
        product=Product(*args[35:42]),
        date=args[-1]
    )
    
print([1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7][1:6])