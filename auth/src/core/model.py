from beanie import Document, Indexed


class User(Document):
    name: str = Indexed(unique=True)        
    role: str              
    password: str         

    class Setting:
        name = 'users'  
