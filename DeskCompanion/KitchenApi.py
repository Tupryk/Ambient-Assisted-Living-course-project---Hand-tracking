import requests


def activate_relay(url, shelf_identifier):
    response = requests.get(url)
    if response.status_code == 200:
        return f"Shelf {shelf_identifier} switched successfully"
    else:
        return f"Failed to open shelf. HTTP Status Code: {response.status_code}"

def activateShelf(shelf_identifier: int,
                  esp32_url: str = "http://10.42.8.218"):

    shelve_endpoints = [
        "/relay_left_shelf",
        "/relay_middle_left_shelf",
        "/relay_middle_right_shelf",
        "/relay_right_shelf"
    ]

    try:
        esp32_url += shelve_endpoints[shelf_identifier]
        return activate_relay(esp32_url, shelf_identifier)
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
