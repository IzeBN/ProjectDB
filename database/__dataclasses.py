from dataclasses import dataclass
from datetime import datetime

@dataclass
class Document:
    id: str
    type: str
    data: str
    issue_date: datetime
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
    date_birth: datetime
    phone_number: int
    addres: str
    place_work: str
    tin: int
    bank_card: int
    count_purchases: int = None
    document: Document = None
         
    
@dataclass
class Employee:
    id: str
    name: str
    lastname: str
    fatherly: str
    date_birth: datetime
    phone_number: int
    addres: str
    citizenship: str
    job_tittle: JobTitle
    sales_count: int
    date_acceptance: datetime
    experince: int
    schedule: str = None
    document: Document = None
    
    
@dataclass
class Product:
    id: str
    title: str
    description: str
    date_release: datetime
    cost: int
    count_sales: int
    serial_number: str
    
    
@dataclass
class Agreement:
    id: str
    client: Client
    employee: Employee
    product: Product
    date: datetime
    
@dataclass
class Sale:
    id: str
    client: Client
    employee: Employee
    product: Product
    date: datetime
    
@dataclass
class Users:
    employes: list[Employee]
    clients: list[Client]

@dataclass
class Items:
    sales: list[Sale]
    agreements: list[Agreement]

async def UserForm(list, user_type: str):
    return [Employee(*args[0:-6], document=Document(*args[-6:-1])) for args in list] \
        if user_type == 'employee' else \
            [Client(*args[0:-6], document=Document(*args[-6:-1])) for args in list]
        
async def ItemForm(list, item_type: str):
    return [Sale(
                id=args[0],
                client=Client(*args[1:12],
                            document=Document(*args[12:17])),
                employee=Employee(*args[17:30],
                                document=Document(*args[30:35])),
                product=Product(*args[35:42]),
                date=args[-1]
            ) for args in list
        ] if item_type == 'sale' \
    else [Agreement(
                id=args[0],
                client=Client(*args[1:12],
                            document=Document(*args[12:17])),
                employee=Employee(*args[17:30],
                                document=Document(*args[30:35])),
                product=Product(*args[35:42]),
                date=args[-1]
            ) for args in list
        ]
    