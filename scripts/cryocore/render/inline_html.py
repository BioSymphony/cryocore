#!/usr/bin/env python3
"""Inline an HTML page's local image/video assets (src= / poster=) into base64
data URIs, producing one self-contained, shareable HTML. Reusable for CryoCore
demo reports. http(s)/data:/anchor URLs are left untouched.

Usage:
  python3 inline_html.py page/index.html --out page/standalone.html
"""

from __future__ import annotations

import argparse
import base64
import mimetypes
import os
import re
import sys


def inline(html_path: str, out_path: str) -> None:
    base = os.path.dirname(os.path.abspath(html_path))
    with open(html_path, encoding="utf-8") as fh:
        html = fh.read()

    def repl(m):
        attr, quote, url = m.group(1), m.group(2), m.group(3)
        if url.startswith(("http://", "https://", "data:", "//", "#")):
            return m.group(0)
        path = os.path.join(base, url)
        if not os.path.isfile(path):
            sys.stderr.write(f"[inline] missing asset: {url}\n")
            return m.group(0)
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as af:
            b64 = base64.b64encode(af.read()).decode()
        return f"{attr}={quote}data:{mime};base64,{b64}{quote}"

    html = re.sub(r'\b(src|poster)=(["\'])([^"\']+)\2', repl, html)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"[inline] wrote {out_path} ({os.path.getsize(out_path)//1024} KB, self-contained)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    inline(a.html, a.out)
