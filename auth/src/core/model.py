from beanie import Document, Indexed



class User(Document):
    name: Indexed(str)            
    role: str              
    password: str         

    class Setting:
        name = 'users'  
