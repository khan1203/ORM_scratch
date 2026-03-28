from webob import Request, Response

from core import app
from roob.constants import HttpStatus
from core.data import inventory
from core.service.product_service import ProductService
from roob.models.responses import JSONResponse



@app.route('/api/products')
class ProductCreatController:
    def __init__(self):
        self.service = ProductService()

    def get(self, request: Request) -> Response:
        return Response(
            json_body=self.service.get_all_products()
        )

    # Create
    def post(self, request: Request) -> Response:
        products = self.service.create_new_product(
            request.json
        )
        return Response(
            json_body=products
        )


@app.route('/api/products/{id:d}')
class ProductModifyController:
    def __init__(self):
        self.service = ProductService()

    def _get_product_not_found_response(self, product_id: int) -> Response:
        return Response(
            json_body={
                "message": f"No product found with product id {product_id}"
            },
            status=HttpStatus.NOT_FOUND
        )

    def get(self, request: Request, id: int) -> Response:
        product = self.service.get_product_by_id(id)
        if not product:
            return self._get_product_not_found_response(id)
        return Response(
            json_body=product
        )

    def delete(self, request: Request, id: int):
        try:
            products = self.service.delete_product_by_id(id)
            return Response(
                json_body=products
            )
        except Exception as e:
            return Response(
                json_body={"message": str(e)},
                status=HttpStatus.NOT_FOUND
            )


@app.route('/api/products/{category}', allowed_methods = ["GET"])
def get_products_by_cat(request: Request, category: str) -> Response:
    if category not in inventory:
        return Response(
            json_body={
                "message": f"{category} doesn't exist in the inventory",
            },
            status=HttpStatus.NOT_FOUND,
        )
    return JSONResponse(
        inventory[category],
    )


class ExceptionController:
    def get_value_error(self, request: Request) -> Response:
        raise ValueError("This is a test exception")

    def get_generic_exception(self, request: Request) -> Response:
        raise Exception("This is an unhandled exception")


exception_controller = ExceptionController()
app.add_route('/api/exception/value-error', exception_controller.get_value_error, allowed_methods=["GET"])
app.add_route('/api/exception', exception_controller.get_generic_exception, allowed_methods=["GET"])