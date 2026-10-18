#!/usr/bin/env python3
"""Verify that LOCKED css/js files were not changed.  Usage: python3 tools/verify_locked.py
Exit code 1 = a locked file was modified (CI / agents must stop).
Only a human maintainer may regenerate checksums:  python3 tools/verify_locked.py --update"""
import hashlib, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
sumfile = root / "assets" / "LOCKED.sha256"
files = sorted(list((root/"assets/css/locked").glob("*.css")) + list((root/"assets/js/locked").glob("*.js")))
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
if "--update" in sys.argv:
    sumfile.write_text("".join(f"{h(p)}  {p.relative_to(root).as_posix()}\n" for p in files)); print("checksums updated"); sys.exit(0)
exp = dict(l.split("  ",1)[::-1] for l in sumfile.read_text().splitlines() if l.strip())
bad = [r.strip() for r,x in ((k.strip(),v) for k,v in exp.items()) if not (root/r).exists() or h(root/r)!=x]
if bad: print("LOCKED FILE CHANGED:", *bad, sep="\n  "); sys.exit(1)
print("OK — all locked files intact")
