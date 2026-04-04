# UT2004 MapIQ — Map Strategy Tool

- A browser-based map viewer and strategy tool for **Unreal Tournament 2004** maps.
- Check it out in action here: https://hitscan.pro/ut2004mapiq.html

![UT2004 MapIQ](https://img.shields.io/badge/UT2004-MapIQ-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## Features

- **📂 Import OBJ** — Import `.obj` map exports from UnrealEd directly in the browser
- **📁 Import Folder** — Import an entire export folder including textures (`.dds`, `.tga`, `.png`, `.bmp`)
- **🗂 Server Maps** — Browse and load maps hosted in a `Maps/` folder on your web server (requires `maps.php`)
- **Normal View** — Wireframe top/front/side views with entity overlays
- **◈ Simple View** — Solid filled top-down minimap (Valorant-style) with height shading, front/side tabs
- **◈ 3D View** — Free-rotate WebGL 3D viewer with texture support and entity labels
- **✂ Slice** — Progressive Y-axis slicer to remove ceiling/roof layers
- **🏷 Labels** — Toggle entity name labels in all views including 3D
- **✏ Draw** — Annotation tools (pen, line, rect, circle, text, pins) with undo/export
- **⬇ Export** — Export current view as PNG or PDF with watermark
- **Auto ZonePortal strip** — ZonePortal faces are automatically removed on import (no more green planes)
- **Texture support** — DXT1/DXT3/DXT5 DDS decoder, TGA decoder, all built into the browser
- **Entity detection** — Automatically classifies weapons, ammo, health, spawns, flags, powerups, vehicles, and more

---

## Getting Started

### Option A — Local use (no server needed)

1. Download `ut2004-map-viewer.html`
2. Open it in any modern browser
3. Use **📂 Import OBJ** or **📁 Import Folder** to load your map

### Option B — Web server with map browser

Deploy to your web server:
```
your-site/
  ut2004-map-viewer.html
  maps.php
  Maps/
    CTF-Face3/
      CTF-Face3.obj
      Textures/
        PackageName/
          texture.dds
    DM-Rankin/
      DM-Rankin.obj
      ...
```
Requires **PHP 7+**. Click **🗂 Maps** to browse available maps.

---

## Exporting Maps from UT2004

### OBJ Geometry
1. Open your map in **UnrealEd 3**
2. `File → Export` → save as `.obj`

### Textures
**UnrealEd Texture Browser:**
1. `View → Texture Browser`
2. Tick all boxes under "In Use Filter" `File → Export All in Use`
3. Make sure the export target is the same folder as the .obj file


### Importing with Textures
Use **📁 Import Folder** — the viewer matches material names to texture filenames automatically.

### ZonePortal Planes
The viewer automatically strips ZonePortal brush faces on import — no green planes in any view.

To pre-clean OBJ files before importing, use the included `strip_portals.py`:

```bash
python strip_portals.py MyMap.obj              # → MyMap_clean.obj
python strip_portals.py MyMap.obj --inplace    # overwrite original
python strip_portals.py Maps/                  # process whole folder
```

---

## Supported Texture Formats

| Format | Support |
|--------|---------|
| `.dds` (DXT1/DXT3/DXT5) | ✅ Full |
| `.tga` (uncompressed + RLE) | ✅ Full |
| `.png` / `.bmp` / `.jpg` | ✅ Native |

All decoding happens in the browser — no server processing needed.

---

## Tech Stack

- **Vanilla HTML/CSS/JS** — single self-contained file, no dependencies, no build step
- **WebGL** — hardware-accelerated 3D with per-material texture batches
- **Canvas 2D** — normal/simple views, draw tools, entity overlays
- `maps.php` — optional PHP backend for server-side map browsing
- `strip_portals.py` — optional Python utility to pre-clean OBJ files

---

## Credits

Built by **inics** with Claude — © 2026 MapIQ 
- https://hitscan.pro/
---

## License

MIT — free to use, modify, and distribute.
