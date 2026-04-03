"""
strip_portals.py — Remove ZonePortal faces from UT2004 OBJ exports
===================================================================
Usage:
    python strip_portals.py MyMap.obj
    python strip_portals.py MyMap.obj --out MyMap_clean.obj
    python strip_portals.py Maps/         (process entire folder)

If no --out is given, the cleaned file is saved as MyMap_clean.obj
(the original is never overwritten unless you use --inplace).
"""

import sys
import os
import re
import argparse


# Materials whose faces should be removed.
# Add any extra material prefixes here if needed.
PORTAL_PREFIXES = (
    "ZonePortal",   # green zone portal planes
)


def is_portal_material(name: str) -> bool:
    """Return True if this usemtl name belongs to a portal surface."""
    low = name.strip().lower()
    return any(low.startswith(p.lower()) for p in PORTAL_PREFIXES)


def strip_portals(text: str) -> tuple[str, int]:
    """
    Parse the OBJ text, remove all faces that use a portal material,
    and return (cleaned_text, faces_removed).
    """
    lines = text.splitlines(keepends=True)
    out = []
    current_mat = None
    skip = False
    faces_removed = 0

    for line in lines:
        stripped = line.strip()

        # Track current material
        if stripped.lower().startswith("usemtl"):
            parts = stripped.split(None, 1)
            mat = parts[1] if len(parts) > 1 else ""
            current_mat = mat
            skip = is_portal_material(mat)
            # Always keep the usemtl line itself (switching material is harmless)
            out.append(line)
            continue

        # Skip face lines for portal materials
        if stripped.startswith("f ") or stripped.startswith("f\t"):
            if skip:
                faces_removed += 1
                continue  # drop this face

        out.append(line)

    return "".join(out), faces_removed


def process_file(src: str, dst: str) -> None:
    print(f"  Reading  : {src}")
    with open(src, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    cleaned, removed = strip_portals(text)

    with open(dst, "w", encoding="utf-8") as f:
        f.write(cleaned)

    size_before = os.path.getsize(src)
    size_after  = os.path.getsize(dst)
    print(f"  Removed  : {removed} portal faces")
    print(f"  Size     : {size_before:,} → {size_after:,} bytes")
    print(f"  Written  : {dst}")


def main():
    parser = argparse.ArgumentParser(
        description="Strip ZonePortal faces from UT2004 OBJ exports"
    )
    parser.add_argument("input", help=".obj file or folder of .obj files")
    parser.add_argument("--out", help="output file (single file mode only)")
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="overwrite the original file instead of creating a _clean copy",
    )
    args = parser.parse_args()

    target = args.input

    # ── Folder mode ──
    if os.path.isdir(target):
        files = [
            os.path.join(target, f)
            for f in os.listdir(target)
            if f.lower().endswith(".obj")
        ]
        if not files:
            print(f"No .obj files found in {target}")
            sys.exit(0)
        for src in sorted(files):
            if args.inplace:
                dst = src
            else:
                base, ext = os.path.splitext(src)
                dst = base + "_clean" + ext
            print(f"\n[{os.path.basename(src)}]")
            process_file(src, dst)
        print("\nDone.")
        return

    # ── Single file mode ──
    if not os.path.isfile(target):
        print(f"File not found: {target}")
        sys.exit(1)

    if args.out:
        dst = args.out
    elif args.inplace:
        dst = target
    else:
        base, ext = os.path.splitext(target)
        dst = base + "_clean" + ext

    print(f"\n[{os.path.basename(target)}]")
    process_file(target, dst)
    print("\nDone.")


if __name__ == "__main__":
    main()
