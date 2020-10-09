#!/usr/bin/env python3
"""Shadowsocks URLs"""

import sys
import json
import base64
import argparse
from typing import Dict
from pathlib import Path

import qrcode #type: ignore
from qrcode.image.svg import SvgPathImage #type: ignore

def get_config(path: Path) -> Dict[str, str]:
    """Return the config as a dict"""
    with path.open() as config:
        return json.loads(config.read())

def ss_url(config: Dict[str, str], exclude_password: bool = True) -> str:
    """Build the ss:// URL"""
    if exclude_password:
        config["password"] = ""

    url = config["method"] + ":" + config["password"] + "@" \
          + config["server"] + ":" + str(config["server_port"])

    return "ss://" + base64.b64encode(bytes(url, "ascii")).decode()

def ss_qr(url: str) -> qrcode.QRCode:
    """Make the QRCode object"""
    # pylint: disable=invalid-name
    qr = qrcode.QRCode()
    qr.add_data(url)
    return qr

def main() -> None:
    """Entry point"""
    parser = argparse.ArgumentParser(description="Generate Shadowsocks URL from configuration")
    parser.add_argument("config", help="Path to configuration file", type=Path)
    parser.add_argument("-q", "--qr", help="Print QR code",
                        action="store_true")
    parser.add_argument("-n", "--nopass", help="Exclude password field",
                        action="store_true")
    parser.add_argument("-p", "--png", help="Save QR code as PNG",
                        action="store_true")
    parser.add_argument("-s", "--svg", help="Save QR code as SVG",
                        action="store_true")

    args = parser.parse_args()

    config = get_config(args.config)
    url = ss_url(config, exclude_password=args.nopass)
    print(url)

    qr = ss_qr(url) # pylint: disable=invalid-name

    if args.qr:
        qr.print_ascii(tty=True)

    if args.png:
        path = config["server"] + ".png"
        qr.make_image().save(path)
        print(f"Saved to {path}", file=sys.stderr)

    if args.svg:
        path = config["server"] + ".svg"
        qr.make_image(SvgPathImage).save(path)
        print(f"Saved to {path}", file=sys.stderr)

if __name__ == "__main__":
    main()
