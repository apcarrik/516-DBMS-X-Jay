from flask import current_app as app
from .user import User


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
        
    @staticmethod
    def checkout(uid):
        cart = Cart.get(uid)
        totalprice = 0
        for cartItem in cart:
            checkQt = app.db.execute('''
SELECT inventory.quantity
FROM inventory
WHERE  inventory.pid=:pid AND inventory.sid=:sid
        AND inventory.quantity >= :quantity
''',        pid=cartItem.pid, sid=cartItem.sid, quantity=cartItem.quantity)
            if not checkQt:
                return "Sorry, no enough quantity for "+str(cartItem.productname)+" from "+ str(cartItem.sellerfirstname)+" "+str(cartItem.sellerlastname)
            totalprice += cartItem.quantity * cartItem.unitprice
        balance = User.get(uid).balance
        if balance < totalprice:
            return "Sorry, no enough balance on your account to pay"
            
        # TODO DB for real purchase. only validation for now
        return "success"

