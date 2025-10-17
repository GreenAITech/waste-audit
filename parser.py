import re


# ---------- parsing ----------

def _clean_num(txt: str) -> float:
    t = txt.strip()
    if t.startswith('='):
        t = t[1:].strip()
    t = t.replace(' ', '')
    if t in ('', '.', '-.', '+.'):
        return 0.0
    try:
        return float(t)
    except ValueError:
        t2 = re.sub(r'[^0-9+\.-]', '', t)
        return float(t2) if t2 else 0.0

def _parse_flags(dtxt: str):
    dtxt = dtxt.strip()
    try:
        v = int(dtxt, 16) if dtxt.lower().startswith('0x') else int(dtxt, 10)
    except ValueError:
        m = re.search(r'(0x[0-9a-fA-F]+|\d+)', dtxt)
        v = int(m.group(1), 16 if (m and m.group(1).lower().startswith('0x')) else 10) if m else 0
    return {
        "ZeroFlag":   bool(v & 0b0001),
        "StableFlag": bool(v & 0b0010),
        "TareFlag":   bool(v & 0b0100),
        "Overload":   bool(v & 0b1000),
    }

def parse_line(payload: str):
    s = payload.strip()
    parts = s.split('/')
    if len(parts) != 4:
        return None
    A, B, C, D = parts
    data = {
        "RoughWeight": _clean_num(A),
        "TareWeight":  _clean_num(B),
        "NetWeight":   _clean_num(C)
    }
    data.update(_parse_flags(D))
    return data
