BODY_DELIMITER = b"\r\n\r\n"
IMG_POSITION = 1


def get_parsed_boundary(headers) -> bytes:
    boundary = headers["content-type"].split("boundary=")
    boundary = boundary[-1]
    return boundary.encode()


def parse_img_bytes(body: bytes, boundary: bytes):
    img_bytes = body.replace(boundary, b"")
    img_bytes = img_bytes.split(BODY_DELIMITER)[IMG_POSITION]
    return img_bytes.replace(b"\r\n----\r\n", b"")
