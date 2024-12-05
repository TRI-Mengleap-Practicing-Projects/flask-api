class UserJSON:
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.password = user.password
        self.created_at = user.created_at
        self.addresses = [AddressJSON(address).to_dict() for address in user.addresses]
        self.orders = [OrderJSON(order).to_dict() for order in user.orders]
        self.reviews = [ReviewJSON(review).to_dict() for review in user.reviews]

    def to_dict(self):
        return self.__dict__


class AddressJSON:
    def __init__(self, address):
        self.id = address.id
        self.user_id = address.user_id
        self.address_line1 = address.address_line1
        self.address_line2 = address.address_line2
        self.city = address.city
        self.state = address.state
        self.zip_code = address.zip_code
        self.country = address.country

    def to_dict(self):
        return self.__dict__


class CategoryJSON:
    def __init__(self, category):
        self.id = category.id
        self.name = category.name
        self.products = [ProductJSON(product).to_dict() for product in category.products]

    def to_dict(self):
        return self.__dict__


class ProductJSON:
    def __init__(self, product):
        self.id = product.id
        self.name = product.name
        self.category_id = product.category_id
        self.barcode = product.barcode
        self.price = product.price
        self.stock = product.stock
        self.created_at = product.created_at
        self.reviews = [ReviewJSON(review).to_dict() for review in product.reviews]
        self.order_details = [OrderDetailJSON(od).to_dict() for od in product.order_details]

    def to_dict(self):
        return self.__dict__


class OrderJSON:
    def __init__(self, order):
        self.id = order.id
        self.user_id = order.user_id
        self.order_date = order.order_date
        self.status = order.status
        self.total_amount = order.total_amount
        self.order_details = [OrderDetailJSON(od).to_dict() for od in order.order_details]
        self.payment = PaymentJSON(order.payment).to_dict() if order.payment else None
        self.shipment = ShipmentJSON(order.shipment).to_dict() if order.shipment else None

    def to_dict(self):
        return self.__dict__


class OrderDetailJSON:
    def __init__(self, order_detail):
        self.id = order_detail.id
        self.order_id = order_detail.order_id
        self.product_id = order_detail.product_id
        self.quantity = order_detail.quantity
        self.price = order_detail.price

    def to_dict(self):
        return self.__dict__


class PaymentJSON:
    def __init__(self, payment):
        self.id = payment.id
        self.order_id = payment.order_id
        self.amount = payment.amount
        self.payment_date = payment.payment_date
        self.payment_method = payment.payment_method
        self.status = payment.status

    def to_dict(self):
        return self.__dict__


class ShipmentJSON:
    def __init__(self, shipment):
        self.id = shipment.id
        self.order_id = shipment.order_id
        self.address_id = shipment.address_id
        self.shipment_date = shipment.shipment_date
        self.delivery_date = shipment.delivery_date
        self.tracking_number = shipment.tracking_number
        self.status = shipment.status

    def to_dict(self):
        return self.__dict__


class ReviewJSON:
    def __init__(self, review):
        self.id = review.id
        self.product_id = review.product_id
        self.user_id = review.user_id
        self.rating = review.rating
        self.comment = review.comment
        self.review_date = review.review_date

    def to_dict(self):
        return self.__dict__
