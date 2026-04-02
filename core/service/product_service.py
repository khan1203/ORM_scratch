from core.data import products, inventory
from exceptions import ResourceNotFoundException

class ProductService:
    def get_all_products(self) -> list[dict]:
        return inventory

    def get_product_by_id(self, product_id: int) -> dict | None:
        for product in products:
            if product['id'] == product_id:
                return product
        raise ResourceNotFoundException(
            message=f"No product found with product id {product_id}"
        )

    def create_new_product(self, product: dict) -> list[dict]:
        products.append(product)
        return products

    def delete_product_by_id(self, product_id: int) -> list[dict]:
        product = self.get_product_by_id(product_id)
        products.remove(product)
        return products