import pytest


class TestListProducts:
    def test_returns_200(self, client):
        response = client.get("/products")
        assert response.status_code == 200

    def test_returns_list(self, client):
        response = client.get("/products")
        assert isinstance(response.json(), list)

    def test_initial_count(self, client):
        """После reset_db должно быть ровно 2 продукта."""
        response = client.get("/products")
        assert len(response.json()) == 2

    def test_product_fields(self, client):
        products = client.get("/products").json()
        for p in products:
            assert "id" in p
            assert "name" in p
            assert "price" in p


class TestGetProduct:
    def test_existing_product(self, client):
        response = client.get("/products/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Milk"

    @pytest.mark.parametrize("product_id", [999, 0, -1])
    def test_not_found(self, client, product_id):
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 404

    def test_error_message(self, client):
        response = client.get("/products/999")
        assert response.json()["detail"] == "Product not found"


class TestCreateProduct:
    NEW_PRODUCT = {"id": 10, "name": "Cheese", "price": 200.0}

    def test_returns_201(self, client):
        response = client.post("/products", json=self.NEW_PRODUCT)
        assert response.status_code == 201

    def test_returns_created_product(self, client):
        response = client.post("/products", json=self.NEW_PRODUCT)
        data = response.json()
        assert data["id"] == 10
        assert data["name"] == "Cheese"
        assert data["price"] == 200.0

    def test_product_appears_in_list(self, client):
        client.post("/products", json=self.NEW_PRODUCT)
        ids = [p["id"] for p in client.get("/products").json()]
        assert 10 in ids

    def test_duplicate_id_returns_400(self, client):
        client.post("/products", json=self.NEW_PRODUCT)
        response = client.post("/products", json=self.NEW_PRODUCT)
        assert response.status_code == 400

    @pytest.mark.parametrize("price", [0, -1])
    def test_invalid_price_returns_422(self, client, price):
        response = client.post("/products", json={"id": 99, "name": "X", "price": price})
        assert response.status_code == 422


class TestUpdateProduct:
    def test_update_name(self, client):
        response = client.put("/products/1", json={"name": "Whole Milk"})
        assert response.status_code == 200
        assert response.json()["name"] == "Whole Milk"

    def test_update_price(self, client):
        response = client.put("/products/1", json={"price": 99.9})
        assert response.status_code == 200
        assert response.json()["price"] == 99.9

    def test_update_both_fields(self, client):
        response = client.put("/products/1", json={"name": "Kefir", "price": 75.0})
        data = response.json()
        assert data["name"] == "Kefir"
        assert data["price"] == 75.0

    def test_id_unchanged_after_update(self, client):
        response = client.put("/products/1", json={"name": "Kefir"})
        assert response.json()["id"] == 1

    def test_update_not_found(self, client):
        response = client.put("/products/999", json={"name": "Ghost"})
        assert response.status_code == 404

    def test_update_persists(self, client):
        """После PUT изменения должны быть видны в GET."""
        client.put("/products/1", json={"name": "Kefir"})
        response = client.get("/products/1")
        assert response.json()["name"] == "Kefir"


class TestDeleteProduct:
    def test_returns_204(self, client):
        response = client.delete("/products/1")
        assert response.status_code == 204

    def test_no_content_body(self, client):
        response = client.delete("/products/1")
        assert response.content == b""

    def test_product_removed_from_list(self, client):
        client.delete("/products/1")
        ids = [p["id"] for p in client.get("/products").json()]
        assert 1 not in ids

    def test_get_after_delete_returns_404(self, client):
        client.delete("/products/1")
        response = client.get("/products/1")
        assert response.status_code == 404

    def test_delete_not_found(self, client):
        response = client.delete("/products/999")
        assert response.status_code == 404

    def test_delete_reduces_count(self, client):
        before = len(client.get("/products").json())
        client.delete("/products/1")
        after = len(client.get("/products").json())
        assert after == before - 1
