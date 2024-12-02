import base64
import requests


def get_file_content(file):
    handle = None
    content = ""
    try:
        handle = file.open("rb")
        content = base64.b64encode(handle.read())
    finally:
        if handle:
            handle.close()
    return content


def get_url_content(url):
    content = requests.get(url).content
    return base64.b64encode(content)
