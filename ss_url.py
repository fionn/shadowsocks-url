#!/usr/bin/env python3

import json
import base64
import argparse
import qrcode

def get_vars(path):
    configuration = open(path, "r").read()
    return json.loads(configuration)

def ss_url(q, password = True):
    url = ""
    if not password:
        q["password"] = ""

    url = q["method"] + ":" + q["password"] + "@" \
          + q["server"] + ":" + str(q["server_port"])

    return "ss://" + base64.b64encode(bytes(url, "ascii")).decode()

def ss_qr(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    return qr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Generate Shadowsocks URL from configuration")
    parser.add_argument("config", help = "Path to configuration file")
    parser.add_argument("-q", "--qr", help = "Print QR code",
                        action = "store_true")
    parser.add_argument("-n", "--nopass", help = "Exclude password field",
                        action = "store_false")
    parser.add_argument("-p", "--png", help = "Save QR code as PNG",
                        action = "store_true")
    parser.add_argument("-s", "--svg", help = "Save QR code as SVG",
                        action = "store_true")

    args = parser.parse_args()

    q = get_vars(args.config)
    url = ss_url(q, password = args.nopass)
    print(url)

    if args.qr:
        qr = ss_qr(url)
        qr.print_ascii(tty = True)
    if args.png:
        path = q["server"] + ".png"
        qr = ss_qr(url)
        qr.make_image().save(path)
        print("Saved to", path)
    if args.svg:
        from qrcode.image.svg import SvgPathImage as svg_image
        path = q["server"] + ".svg"
        qr = ss_qr(url)
        img = qr.make_image(svg_image).save(path)
        print("Saved to", path)

