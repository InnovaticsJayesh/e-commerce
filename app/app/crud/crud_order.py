from sqlalchemy.orm import Session, aliased

from app.models.order import Order, OrderItem
from app.models.user import User, Address
from app.models.product import Product
from app.models.location import Country, State, City


class CrudOrder:
    
    def __init__(self):
        pass
 

    def read_orders(self, current_user, db: Session):
        if not current_user:
            return {'success': False, 'msg': 'Unable to find User'}

        shipping_address = aliased(Address, name="shipping_address")
        billing_address = aliased(Address, name="billing_address")
        shipping_country = aliased(Country, name="shipping_country")
        shipping_state = aliased(State, name="shipping_state")
        shipping_city = aliased(City, name="shipping_city")
        billing_country = aliased(Country, name="billing_country")
        billing_state = aliased(State, name="billing_state")
        billing_city = aliased(City, name="billing_city")

        order_read = (
            db.query(
                Order.id, Order.total, Order.created_at, Order.updated_at,
                User.name.label("user_name"), User.email.label("user_email"),
                shipping_address.name.label("shipping_name"), shipping_address.address.label("shipping_address"),
                shipping_country.name.label("shipping_country"), shipping_state.name.label("shipping_state"), shipping_city.name.label("shipping_city"),
                shipping_address.landmark.label("shipping_landmark"), shipping_address.pincode.label("shipping_pincode"),
                billing_address.name.label("billing_name"), billing_address.address.label("billing_address"),
                billing_country.name.label("billing_country"), billing_state.name.label("billing_state"), billing_city.name.label("billing_city"),
                billing_address.landmark.label("billing_landmark"), billing_address.pincode.label("billing_pincode"),
                Product.name.label("product_name"), Product.price.label("product_price"),
                OrderItem.quantity.label("product_quantity")
            )
            .join(User, Order.user_id == User.id)
            .join(shipping_address, Order.address_id == shipping_address.id)
            .join(shipping_country, shipping_address.country_id == shipping_country.id)
            .join(shipping_state, shipping_address.state_id == shipping_state.id)
            .join(shipping_city, shipping_address.city_id == shipping_city.id)
            .join(billing_address, Order.billing_address_id == billing_address.id)
            .join(billing_country, billing_address.country_id == billing_country.id)
            .join(billing_state, billing_address.state_id == billing_state.id)
            .join(billing_city, billing_address.city_id == billing_city.id)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .join(Product, OrderItem.product_id == Product.id)
            .filter(Order.user_id == current_user.id)
            .all()
        )

        if not order_read:
            return {'success': False, 'msg': 'No orders found'}

        orders = {}
        for order in order_read:
            if order.id not in orders:
                orders[order.id] = {
                    "order_id": order.id,
                    "total": order.total,
                    "user": {"name": order.user_name, "email": order.user_email},
                    "shipping_address": {
                        "name": order.shipping_name,
                        "address": order.shipping_address,
                        "country": order.shipping_country,
                        "state": order.shipping_state,
                        "city": order.shipping_city,
                        "landmark": order.shipping_landmark,
                        "pincode": order.shipping_pincode
                    },
                    "billing_address": {
                        "name": order.billing_name,
                        "address": order.billing_address,
                        "country": order.billing_country,
                        "state": order.billing_state,
                        "city": order.billing_city,
                        "landmark": order.billing_landmark,
                        "pincode": order.billing_pincode
                    },
                    "products": []
                }

            orders[order.id]["products"].append({
                "name": order.product_name,
                "price": order.product_price,
                "quantity": order.product_quantity
            })

        return {'success': True, 'orders': list(orders.values())}


    
    def read_single_order(self, current_user, order_id: int, db: Session):
        if not current_user:
            return {'success': False, 'msg': 'Unable to find User'}

        # Aliases for table joins
        shipping_address = aliased(Address, name="shipping_address")
        billing_address = aliased(Address, name="billing_address")
        shipping_country = aliased(Country, name="shipping_country")
        shipping_state = aliased(State, name="shipping_state")
        shipping_city = aliased(City, name="shipping_city")
        billing_country = aliased(Country, name="billing_country")
        billing_state = aliased(State, name="billing_state")
        billing_city = aliased(City, name="billing_city")

        # Querying the order details
        order_read = (
            db.query(
                Order.id, Order.total, Order.created_at, Order.updated_at,
                User.name.label("user_name"), User.email.label("user_email"),
                shipping_address.name.label("shipping_name"), shipping_address.address.label("shipping_address"),
                shipping_country.name.label("shipping_country"), shipping_state.name.label("shipping_state"), shipping_city.name.label("shipping_city"),
                shipping_address.landmark.label("shipping_landmark"), shipping_address.pincode.label("shipping_pincode"),
                billing_address.name.label("billing_name"), billing_address.address.label("billing_address"),
                billing_country.name.label("billing_country"), billing_state.name.label("billing_state"), billing_city.name.label("billing_city"),
                billing_address.landmark.label("billing_landmark"), billing_address.pincode.label("billing_pincode"),
                Product.name.label("product_name"), Product.price.label("product_price"),
                OrderItem.quantity.label("product_quantity")
            )
            .join(User, Order.user_id == User.id)
            .join(shipping_address, Order.address_id == shipping_address.id)
            .join(shipping_country, shipping_address.country_id == shipping_country.id)
            .join(shipping_state, shipping_address.state_id == shipping_state.id)
            .join(shipping_city, shipping_address.city_id == shipping_city.id)
            .join(billing_address, Order.billing_address_id == billing_address.id)
            .join(billing_country, billing_address.country_id == billing_country.id)
            .join(billing_state, billing_address.state_id == billing_state.id)
            .join(billing_city, billing_address.city_id == billing_city.id)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .join(Product, OrderItem.product_id == Product.id)
            .filter(Order.user_id == current_user.id, Order.id == order_id)
            .first()
        )

        if not order_read:
            return {'success': False, 'msg': 'Order not found'}

        # Constructing order details
        order_details = {
            "order_id": order_read.id,
            "total": order_read.total,
            "user": {"name": order_read.user_name, "email": order_read.user_email},
            "shipping_address": {
                "name": order_read.shipping_name,
                "address": order_read.shipping_address,
                "country": order_read.shipping_country,
                "state": order_read.shipping_state,
                "city": order_read.shipping_city,
                "landmark": order_read.shipping_landmark,
                "pincode": order_read.shipping_pincode
            },
            "billing_address": {
                "name": order_read.billing_name,
                "address": order_read.billing_address,
                "country": order_read.billing_country,
                "state": order_read.billing_state,
                "city": order_read.billing_city,
                "landmark": order_read.billing_landmark,
                "pincode": order_read.billing_pincode
            },
            "products": [{
                "name": order_read.product_name,
                "price": order_read.product_price,
                "quantity": order_read.product_quantity
            }]
        }

        return {'success': True, 'order': order_details}

crud_order = CrudOrder()