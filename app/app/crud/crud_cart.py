from sqlalchemy.orm import Session

from app import schemas

from app.models.cart import Cart, CartItems
from app.models.product import Product
from app.models.attribute import AttributeMaster,product_attribute_association, AttributeValue


class CrudCart:
    
    def __init__(self):
        pass

    def create(self, current_user, db: Session, params):
        if current_user is None:
            return {'success': False, 'msg': 'Unable to find User'}

        # Check if cart exists, otherwise create one
        cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.add(cart)
            db.commit()
            db.refresh(cart)  # Ensure we get the ID after commit

        if not cart.id:
            return {'success': False, 'msg': 'Failed to create cart'}

        # Check if product already exists in cart
        exist_cart_product = db.query(CartItems).filter(
            CartItems.cart_id == cart.id, 
            CartItems.product_id == params.product_id
        ).first()

        if exist_cart_product:
            return {
                'success': False,
                'msg': 'Product already in cart',
                'data': {
                    'product_id': exist_cart_product.product_id  # Optional but useful for redirection
                }
            }


        # Fetch the product
        product = db.query(Product).filter(Product.id == params.product_id).first()
        if not product:
            return {'success': False, 'msg': 'Product not found'}

        # Extract attributes from request
        attributes = {k.lower(): v for k, v in params.dict().items()}  

        case_material = attributes.get("case_material", None)
        strap_type = attributes.get("strap_type", None)
        dial_color = attributes.get("dial_color", None)

        # 🔥 Validate if attributes exist in product_attribute_association
        valid_attribute_values = db.query(AttributeValue.value).join(
            product_attribute_association, AttributeValue.id == product_attribute_association.c.attribute_value_id
        ).filter(
            product_attribute_association.c.product_id == product.id
        ).all()

        # Convert to a set for faster lookup
        valid_attribute_values = {val[0] for val in valid_attribute_values}

        # 🔴 Check if provided values exist in the valid list
        if case_material and case_material not in valid_attribute_values:
            return {'success': False, 'msg': f'Invalid case_material: {case_material} for product {product.id}'}
        
        if strap_type and strap_type not in valid_attribute_values:
            return {'success': False, 'msg': f'Invalid strap_type: {strap_type} for product {product.id}'}

        if dial_color and dial_color not in valid_attribute_values:
            return {'success': False, 'msg': f'Invalid dial_color: {dial_color} for product {product.id}'}

        # Create cart item entry
        db_cart_item = CartItems(
            cart_id=cart.id,
            product_id=product.id,
            case_material=case_material,  
            strap_type=strap_type,  
            dial_color=dial_color, 
            price=product.price,
            quantity=params.quantity
        )
        
        db.add(db_cart_item)
        db.commit()
        db.refresh(db_cart_item)

        return {'success': True, 'msg': 'Added to cart successfully', "data": {"product_id" : db_cart_item.product_id}}
        

    def get_cart(self, current_user, db: Session):
        if current_user is None:
            return {'success': False, 'msg': 'Unable to find User'}
        cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
        if not cart:
            return {'success': False, 'msg': 'Cart not found'}
        cart_items = db.query(
            CartItems.id.label("cart_item_id"),
            CartItems.product_id,
            CartItems.quantity,
            CartItems.price.label("product_price"),
            CartItems.case_material,
            CartItems.strap_type,
            CartItems.dial_color,
            Product.name.label("product_name"),
            Product.image_path.label("image_path"),
        ).join(Product, CartItems.product_id == Product.id).filter(CartItems.cart_id == cart.id).all()
        if not cart_items:
            return {'success': False, 'msg': 'No items found in cart', 'data': []}
        cart_data = []
        for item in cart_items:
            attributes = {
                "case_material": item.case_material,
                "strap_type": item.strap_type,
                "dial_color": item.dial_color
            }
            cart_data.append({
                "cart_item_id": item.cart_item_id,
                "product_id": item.product_id,
                "product_name": item.product_name,
                "product_price": item.product_price,
                "quantity": item.quantity,
                "total_price": item.quantity * item.product_price,
                "image_path": item.image_path,
                "attributes": {k: v for k, v in attributes.items() if v is not None} 
            })
        return {'success': True, 'msg': 'Successfully fetched cart items', 'data': cart_data}


    def update_cart_quantity(self, params, db: Session):
        cart_item = db.query(CartItems).filter(CartItems.id == params.cart_item_id).first()
        if not cart_item:
            return {"success": False, "message": "Cart item not found"}
        if params.quantity == 0:
            db.delete(cart_item)
            db.commit()
            return {"success": True, "message": "Item removed from cart"}
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
