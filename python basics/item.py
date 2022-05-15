class Item(object):
    all = []
    def __init__(self, name, quantity=0, price=0):
        self.__name = name
        self.quantity = quantity
        self.__price = price

        Item.all.append(self)

    def __repr__(self):
        return f"{self.__class__.__name__}: (name= {self.name}, quantity={self.quantity}, price={self.price})"

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def price(self):
        return self.__price

    """
    Encapsulation being implemented below by setting the type of values that will be permitted to be entered as price.
    """
    @price.setter
    def price(self, modified_price):
        if not(isinstance(modified_price, (float, int))) or modified_price <= 0:
            raise AttributeError("Please enter a valid price greater than zero")
        self.__price = modified_price

    """
    Abstraction is implemented by providing hidden methods/private methods which can be only used within the instance methods.
    """
    def __connect(self):
        print("Connection established")

    def send_email(self):
        print("sending email")
        self.__connect()
        print("Email sent successfully")



item = Item("new item", 700, 2)
print(item)
item.name = "other item"
print(item)
item.price = 900
print(item)
item.send_email()

