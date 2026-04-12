from app.models import Product

products_db: dict[int, Product] = {
    1: Product(id=1, name="Milk", price=89.9),
    2: Product(id=2, name="Bread", price=49.0),
}
