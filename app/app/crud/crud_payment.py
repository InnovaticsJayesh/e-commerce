from sqlalchemy.orm import Session

from app import schemas

from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.cart import CartItems


class CrudPayments:
    
    def __init__(self):
        pass

    def make_payment(self, current_user, db: Session, params):
        if current_user is None:
            return {'success': False, 'msg': 'Unable to find User'}
        cart_items = db.query(CartItems).filter(CartItems.id.in_(params.cart_items_ids)).all()
        if not cart_items:
            return {'success': False, 'msg': 'No valid cart items found'}
        total_price = sum(item.price * item.quantity for item in cart_items)
        payment = Payment(user_id=current_user.id, amount=total_price, is_paid=True)
        db.add(payment)
        db.commit()
        order = Order(user_id=current_user.id, 
                      address_id=params.shipping_address_id,   
                      billing_address_id=params.billing_address_id,
                      total=total_price)
        db.add(order)   
        db.commit()
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                cart_id=item.cart_id,
                price=item.price,
                quantity=item.quantity,
                payment_id=payment.id
            )
            db.add(order_item)
            db.delete(item)
        db.commit()
        db.refresh(payment)
        return {'success': True, 'msg': 'Payment and order created successfully', 'order_id': order.id}
    

crud_payment = CrudPayments()