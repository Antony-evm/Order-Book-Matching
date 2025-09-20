from fastapi import HTTPException, status


class OrderNotFoundException(HTTPException):
    def __init__(self, order_id: int):
        super().__init__(
            # Documenting as 500, as if we have an order_id that doesn't exist,
            # something went wrong on our end. Therefore it's not 404
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": f"Order with id {order_id} not found.",
                "message": 'Encountered unexpected error... Please contact us for more information!'
            }
        )
