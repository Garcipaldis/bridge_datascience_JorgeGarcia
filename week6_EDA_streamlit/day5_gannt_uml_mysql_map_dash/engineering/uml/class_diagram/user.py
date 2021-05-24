class User(object):
    def __init__(self, userId, password, loginStatus, registerDate):
        self.userId = userId
        self.password = password
        self.loginStatus = loginStatus
        self.registerDate = registerDate
    
    def verifyLogin(self):
        if self.password == "XHG":
            return True
        else: 
            return False

class Administrator(User):
    
    def __init__(self, userId, password, loginStatus, registerDate, aN, em):
        User.__init__(self, userId, password, loginStatus, registerDate)
        self.adminName = aN
        self.email = em
        
gabriel = Administrator(userId=56, password="Hola", loginStatus="True",
                        registerDate="12/02/2020", aN="Gabriel", em="ga@jg.com")
#gabriel.verifyLogin()

class Customer(User):
    def __init__(self, eyes, user):
        x = 2
        _x = 4  # protegido
        __c = 5  # privado
        User.__init__(self, 
                    user.userId,
                    user.password, 
                    user.loginStatus,
                    user.registerDate)
        self.eyes = eyes

c = Customer()
_c = 2
__c = 5
class Order:
    def __init__(self, orderID, dateCreated, customer):
        self.orderID = orderID
        self.dateCreated = dateCreated
        self.customer = customer

# Esta condición de abajo hace que si yo importo este
# fichero desde otro módulo no se ejecuta lo que esté debajo
if __name__ == '__main__':
    usuario = User(userId=2, 
                    password="XHG",
                    loginStatus=True,
                    registerDate="10/02/1999")
    
    cliente = Customer(eyes=2, user=usuario)
    
    pedido = Order(orderID=2662, 
                dateCreated="06/07/2020", 
                customer=cliente)
    
    print(pedido.customer.verifyLogin())

