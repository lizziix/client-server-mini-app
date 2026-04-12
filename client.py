import requests

BASE_URL = "http://127.0.0.1:8000"

def print_response(resp):
    print("Status:", resp.status_code)
    print("JSON:", resp.json())

def demo():
    # GET: получить список продуктов
    print("=== GET /products ===")
    resp = requests.get(f"{BASE_URL}/products")
    print_response(resp)

    # GET: получить продукт по id
    print("\n=== GET /products/1 ===")
    resp = requests.get(f"{BASE_URL}/products/1")
    print_response(resp)

    # GET: запрос несуществующего продукта -> 404
    print("\n=== GET /products/999 ===")
    resp = requests.get(f"{BASE_URL}/products/999")
    print("Status:", resp.status_code)
    print("Body:", resp.text)

    # POST: создать новый продукт
    print("\n=== POST /products ===")
    new_product = {"id": 4, "name": "Butterr", "price": 120.5}
    resp = requests.post(f"{BASE_URL}/products", json=new_product)
    print_response(resp)

    # Повторный POST с тем же id -> 400
    print("\n=== POST /products (duplicate id) ===")
    resp = requests.post(f"{BASE_URL}/products", json=new_product)
    print("Status:", resp.status_code)
    print("Body:", resp.text)

    # Искусственная 500
    print("\n=== GET /error ===")
    resp = requests.get(f"{BASE_URL}/error")
    print("Status:", resp.status_code)
    print("Body:", resp.text)

if __name__ == "__main__":
    demo()