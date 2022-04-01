from flask import current_app as app


class Product:
    def __init__(self, id, name, available, category):
        self.id = id
        self.name = name
        self.available = available
        self.category = category


    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, available, category
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, available, category
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
        

    @staticmethod
    def add_product(name, price):
        try:
            rows = app.db.execute("""
INSERT INTO Products(name, price, available)
VALUES(:name, :price, true)
RETURNING id
""",
                                  name = name,
                                  price = price)
            id = rows[0][0]
            return Product.get(id)
        except Exception as e:
            # likely product already exist; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def getSellerInfo(pid):
        rows = app.db.execute('''
SELECT users.id, users.firstname, users.lastname, inventory.price, inventory.quantity, inventory.description
FROM inventory, users
WHERE inventory.pid = :id AND inventory.sid = users.id
''',
                              id=pid)
        return rows if rows is not None else None
