def verify_status_code(status_code) -> None:
    if not isinstance(status_code, int):
        raise TypeError('status code must be an integer')
    if status_code < 100 and status_code >= 600:
        raise ValueError('invalid status code value')
