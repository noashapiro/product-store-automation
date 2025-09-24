from be.infrastructure.responsesDTO.responses import ProductResponseDTO, CartResponseDTO


def get_products_from_response(resp):
    return [ProductResponseDTO(**p) for p in resp.json()]

def get_cart_from_response_list(resp):
    return [CartResponseDTO(**c) for c in resp.json()]

def get_cart_from_response(resp):
    return CartResponseDTO(**resp.json())