import asyncio
from database import Database

async def main():
    db = Database('postgresql://izeb:izeb@localhost:5432/main')
    
    await db.create_tables()
    
    print('OK')
    
    await asyncio.sleep(10)
    await db.find_items(item_type='')
    await db.find_users(user_type='')
    
if __name__ == "__main__":
    asyncio.run(main())