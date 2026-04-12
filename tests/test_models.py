import pytest
from pydantic import ValidationError

from app.models import Product, ProductUpdate


class TestProduct:
    def test_valid_product(self):
        p = Product(id=1, name="Milk", price=89.9)
        assert p.id == 1
        assert p.name == "Milk"
        assert p.price == 89.9

    @pytest.mark.parametrize("price", [0, -1, -100])
    def test_invalid_price(self, price):
        """Цена должна быть строго больше нуля."""
        with pytest.raises(ValidationError):
            Product(id=1, name="Milk", price=price)

    @pytest.mark.parametrize("field", ["id", "name", "price"])
    def test_missing_required_field(self, field):
        data = {"id": 1, "name": "Milk", "price": 10.0}
        del data[field]
        with pytest.raises(ValidationError):
            Product(**data)

    def test_serialization(self):
        p = Product(id=1, name="Milk", price=89.9)
        d = p.model_dump()
        assert d == {"id": 1, "name": "Milk", "price": 89.9}


class TestProductUpdate:
    def test_all_fields_optional(self):
        """ProductUpdate можно создать без полей — partial update."""
        u = ProductUpdate()
        assert u.name is None
        assert u.price is None

    def test_partial_name_only(self):
        u = ProductUpdate(name="Butter")
        assert u.name == "Butter"
        assert u.price is None

    def test_partial_price_only(self):
        u = ProductUpdate(price=150.0)
        assert u.price == 150.0
        assert u.name is None

    @pytest.mark.parametrize("price", [0, -5])
    def test_invalid_price(self, price):
        with pytest.raises(ValidationError):
            ProductUpdate(price=price)
