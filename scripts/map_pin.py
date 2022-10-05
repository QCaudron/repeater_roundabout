import argparse

import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("id_code", help="ID code from repeaterbook.com", type=str, nargs="+")
    return parser.parse_args()


def create_js(id_code: str):

    url = f"https://www.repeaterbook.com/repeaters/details.php?state_id=53&ID={id_code}"
    source = requests.get(url)
    
    call = source.text.split("msResult.php?call=")[1].split("&")[0]
    freq = source.text.split("Downlink:</td>\n<td>")[1].split("</td>")[0]
    freq = f"{float(freq):.03f}"
    latlong = source.text.split("center: ")[1].split("\n")[0][:-1]
    
    return f'L.marker({latlong}).bindPopup("{call} {freq}").addTo(map);'


if __name__ == "__main__":

    args = parse_args()

    for code in args.id_code:
        print(create_js(code))