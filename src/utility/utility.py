def is_success_code(code: int) -> bool:
    return code >= 200 or code < 300
