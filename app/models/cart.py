from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, productname, sid, sellerlastname, sellerfirstname,  quantity, unitprice):
        self.uid = uid
        self.pid = pid
        self.productname = productname
        self.sid = sid
        self.sellerlastname = sellerlastname
        self.sellerfirstname = sellerfirstname
        self.quantity = quantity
        self.unitprice = unitprice

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT cart.uid, cart.pid, products.name, cart.sid, users.lastname, users.firstname, cart.quantity, inventory.price
FROM products, cart, users, inventory
WHERE cart.uid = :uid AND cart.pid=products.id
    AND cart.sid=users.id
    AND inventory.pid=products.id   AND inventory.sid=users.id
''',
                              uid=uid)
        return [Cart(*row) for row in rows] if rows is not None else None

