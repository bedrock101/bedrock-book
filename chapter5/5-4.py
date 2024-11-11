def generate_qr_code(url, size=6, transparent=False):
    base_url = "https://qrtag.net/api/qr"

    if transparent:
        base_url += "_transparent"
    qr_url = f"{base_url}_{size}.png?url={url}"
    
    return qr_url
