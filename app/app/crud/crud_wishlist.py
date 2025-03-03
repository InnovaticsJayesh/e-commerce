from sqlalchemy.orm import Session

from app import schemas

from app.models.product import Product
from app.models.wishlist import WishList


class WishLists:

    def __init__(self):
        pass


    def toggle_wishlist(self, current_user, db: Session, params):
        if not current_user:
            return {'success': False, 'msg': 'Unable to find User'}

        product = db.query(Product).filter(Product.id == params.product_id).first()
        if not product:
            return {'success': False, 'msg': 'Product not found'}
        
        wishlist_entry = db.query(WishList).filter(
            WishList.user_id == current_user.id,
            WishList.product_id == params.product_id
        ).first()

        if params.isFavourite:
            if wishlist_entry:
                return {'success': False, 'msg': 'Product already in the wishlist'}
            else:
                wishlist = WishList(user_id=current_user.id, product_id=params.product_id)
                db.add(wishlist)
                product.is_favourite = True
                msg = 'Added to wishlist successfully'
        else:
            if wishlist_entry:
                db.delete(wishlist_entry)
                product.is_favourite = False
                msg = 'Removed from wishlist successfully'
            else:
                return {'success': False, 'msg': 'Product not found in the wishlist'}
        db.commit()
        db.refresh(product)

        return {'success': True, 'msg': msg, 'data': []}


    def get_wishlist_products(self, current_user, db: Session):
        if not current_user:
            return {'success': False, 'msg': 'Unable to find User'}
        
        wishlist_products = (
            db.query(Product)
            .join(WishList, Product.id == WishList.product_id)
            .filter(WishList.user_id == current_user.id)
            .all()
        )

        if not wishlist_products:
            return {'success': True, 'msg': 'Wishlist is empty', 'data': []}
        
        all_products = [
            {
                "id": product.id,                     
                "name": product.name,
                "price": product.price,
                "image_url": product.image_path,
                "is_favourite": product.is_favourite,
            }
            for product in wishlist_products
        ]
        
        return {'success': True, 'msg': 'All wishlist products', 'data': all_products}





wish_list = WishLists()