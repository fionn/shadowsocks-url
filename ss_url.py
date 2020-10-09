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

class SSConfigurationError(Exception):
    """Raised when configuration fails to validate"""

class SS:
    """Shadowsocks"""

    def __init__(self, config: Dict[str, str], nopass: bool = True) -> None:
        self.config = config
        self.exclude_password = nopass
        self._validate()

    def _validate(self) -> None:
        keys = ["method", "server", "server_port"]

        if not self.exclude_password:
            keys.append("password")

        for key in keys:
            if key not in self.config:
                raise SSConfigurationError(f"Config must contain a key for \"{key}\"")

    @property
    def url(self) -> str:
        """Build the ss:// URL"""
        if self.exclude_password:
            self.config["password"] = ""

        url = self.config["method"] + ":" + self.config["password"] + "@" \
            + self.config["server"] + ":" + str(self.config["server_port"])

        return "ss://" + base64.b64encode(bytes(url, "ascii")).decode()

    @property
    def qr(self) -> qrcode.QRCode:
        """Make the QRCode object"""
        # pylint: disable=invalid-name
        qr = qrcode.QRCode()
        qr.add_data(self.url)
        return qr

def main() -> None:
    """Entry point"""
    parser = argparse.ArgumentParser(description="Generate Shadowsocks URL from configuration")
    parser.add_argument("config", help="Path to configuration file", type=Path)
    parser.add_argument("-q", "--qr", help="Print QR code",
                        action="store_true")
    parser.add_argument("-n", "--nopass", help="Exclude password field",
                        action="store_true")
    parser.add_argument("-s", "--svg", help="Save QR code as SVG",
                        action="store_true")

    args = parser.parse_args()

    with args.config.open() as config:
        ss = SS(json.loads(config.read()), args.nopass) # pylint: disable=invalid-name

    print(ss.url)

    if args.qr:
        ss.qr.print_ascii(tty=True)

    if args.svg:
        path = ss.config["server"] + ".svg"
        ss.qr.make_image(SvgPathImage).save(path)
        print(f"Saved to {path}", file=sys.stderr)

if __name__ == "__main__":
    main()
