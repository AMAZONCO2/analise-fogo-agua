"""Fixa underscore>=1.13.8 no frontend do streamlit-folium após pip install."""
from __future__ import annotations

import json
import site
from pathlib import Path


def main() -> None:
    for sp in site.getsitepackages():
        pkg_json = Path(sp) / "streamlit_folium" / "frontend" / "package.json"
        if not pkg_json.is_file():
            continue
        data = json.loads(pkg_json.read_text(encoding="utf-8"))
        data.setdefault("dependencies", {})["underscore"] = "1.13.8"
        overrides = data.setdefault("overrides", {})
        overrides["underscore"] = "1.13.8"
        pkg_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"Atualizado: {pkg_json}")
        return
    raise SystemExit("streamlit_folium/frontend/package.json não encontrado.")


if __name__ == "__main__":
    main()
