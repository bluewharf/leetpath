from urllib.parse import urlsplit


def validate_https_url(value: str | None) -> str | None:
    if value is None or value == "":
        return None
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("链接必须是有效的 HTTPS URL")
    return value


def safe_https_url(value: str | None) -> str | None:
    try:
        return validate_https_url(value)
    except ValueError:
        return None
