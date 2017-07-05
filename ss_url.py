#!/usr/bin/env python3

import json
import base64
import argparse
import qrcode

def get_vars(path):
    f = open(path, "r").read()
    return json.loads(f)

def ss_uri(q, password = True):
    url = ""
    if password:
        url = q["method"] + ":" + q["password"] + "@" + \
              q["server"] + ":" + str(q["server_port"])
    else:
        url = q["method"] + ":@" + \
              q["server"] + ":" + str(q["server_port"])

    url = "ss://" + base64.b64encode(bytes(url, "ascii")).decode()
    return url

def ss_qr(uri):
    qr = qrcode.QRCode()
    qr.add_data(uri)
    return qr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Shadowsocks URL from configuration")
    parser.add_argument("config", help = "Path to the configuration file")
    parser.add_argument("-q", "--qr", help = "Print the QR code",
                        action = "store_true")
    parser.add_argument("-n", "--nopass", help = "Exclude the password field",
                        action = "store_false")
    parser.add_argument("-p", "--png", help = "Save the QR code as a PNG",
                        action = "store_true")

    args = parser.parse_args()

    q = get_vars(args.config)
    url = ss_uri(q, password = args.nopass)
    print(url)
    if args.qr:
        qr = ss_qr(url)
        qr.print_ascii(tty = True)
    if args.png:
        qr = ss_qr(url)
        extension = "png"
        path = q["server"] + "." + extension
        qr.make_image().save(path, extension.upper())

