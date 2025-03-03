from sqlalchemy.orm import Session

from app import schemas

from app.models.cart import Cart, CartItems
from app.models.product import Product


class CrudCart:
    
    def __init__(self):
        pass


    def create(self, current_user, db: Session, params):
        if current_user is None:
            return {'success': False, 'msg': 'Unable to find User'}
        cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.add(cart)
            db.commit()
        if not cart.id:
            return {'success': False, 'msg': 'Failed to create cart'}
        exist_cart_product = db.query(CartItems).filter(CartItems.cart_id == cart.id, CartItems.product_id == params.product_id).first()
        if exist_cart_product:
            return {'success': False, 'msg': 'Product already in cart'}
        product = db.query(Product).filter(Product.id == params.product_id).first()
        if not product:
            return {'success': False, 'msg': 'Product not found'}
        db_cart_item = CartItems(cart_id=cart.id, product_id=product.id,
                                 case_material=params.case_material, strap_type=params.strap_type,           
                                 dial_color=params.dial_color, price=product.price, 
                                 quantity=params.quantity)
        db.add(db_cart_item)
        db.commit()
        db.refresh(db_cart_item)
        return {'success': True, 'msg': 'Added to cart successfully'}
    

    def get_cart(self, current_user, db: Session):
        if current_user is None:
            return {'success': False, 'msg': 'Unable to find User'}
        cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            return {'success': False, 'msg': 'Unable to find cart items'}
        # INNER JOIN
        query = (db.query(CartItems, Product)
                .join(Product, CartItems.product_id == Product.id)
                .filter(CartItems.cart_id == cart.id))
        cart_items = query.all()
        if not cart_items:
            return {'success': False, 'msg': 'No items found in cart', 'data': []}
        cart_data = [
            {
                "cart_item_id": item.CartItems.id,
                "product_id": item.Product.id,
                "product_name": item.Product.name,
                "product_price": item.Product.price,
                "quantity": item.CartItems.quantity,
                "total_price": item.CartItems.quantity * item.Product.price,
                "image_path": item.Product.image_path
            }
            for item in cart_items
        ]

        return {'success': True, 'msg': 'Successfully fetched cart items', 'data': cart_data}


    def update_cart_quantity(self, params, db: Session):
        cart_item = db.query(CartItems).filter(CartItems.id == params.cart_item_id).first()
        if not cart_item:
            return {"success": False, "message": "Cart item not found"}
        cart_item.quantity = params.quantity
        db.commit()
        db.refresh(cart_item)
        return {
            "success": True,
            "message": "Quantity updated successfully",
            "cart_item": {
                "id": cart_item.id,
                "quantity": cart_item.quantity
            }
        }

         
        
    
crud_cart = CrudCart()
