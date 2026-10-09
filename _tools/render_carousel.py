"""Randeaza un carusel Instagram (1080x1350) din spec JSON in stilul Sorin Crisan.

Utilizare: python3 render_carousel.py spec.json out_dir
Spec: {"slides": [[bloc, ...], ...], "cta_last": true}
Blocuri: {"kicker": "TEXT"} | {"h": "text cu *accent*"} | {"hs": "titlu mai mic"}
         {"p": "paragraf"} | {"items": ["a", "b"]} | {"steps": [["Titlu", "descriere"], ...]}
         {"cta": "text casuta teal"} | {"bar": true}
"""
import html, json, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
FONT_SRC = {
    "Archivo.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf",
    "DMSans.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/DMSans%5Bopsz,wght%5D.ttf",
}
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

C = {"bg": "#1A0A2E", "card": "#2A1548", "txt": "#F8F5FF", "soft": "#D9CCF2",
     "mute": "#B9A6DC", "teal": "#00C9A7", "violet": "#8E44EC", "violet_d": "#6B2FB3"}


def fonts():
    FONTS.mkdir(exist_ok=True)
    for name, url in FONT_SRC.items():
        f = FONTS / name
        if not f.exists():
            urllib.request.urlretrieve(url, f)


def rich(t):
    t = html.escape(t)
    return re.sub(r"\*(.+?)\*", rf'<span style="color:{C["teal"]}">\1</span>', t)


def block(b):
    if "kicker" in b:
        return f'<p style="margin:0;font-size:34px;font-weight:700;letter-spacing:.12em;color:{C["teal"]}">{rich(b["kicker"])}</p>'
    if "h" in b:
        size = b.get("size", 100)
        return f'<h1 style="margin:0;font-family:Archivo;font-weight:800;font-size:{size}px;line-height:1.04;letter-spacing:-.02em">{rich(b["h"])}</h1>'
    if "hs" in b:
        return f'<h2 style="margin:0;font-family:Archivo;font-weight:800;font-size:72px;line-height:1.06;letter-spacing:-.02em">{rich(b["hs"])}</h2>'
    if "p" in b:
        return f'<p style="margin:0;font-size:{b.get("size", 50)}px;line-height:1.3;font-weight:500;color:{C["soft"]}">{rich(b["p"])}</p>'
    if "bar" in b:
        return f'<div style="width:140px;height:12px;background:{C["violet"]};border-radius:6px"></div>'
    if "items" in b:
        rows = "".join(
            f'<div style="display:flex;gap:28px;align-items:center;padding:34px 44px;background:{C["card"]};border-radius:24px">'
            f'<span style="font-family:Archivo;font-weight:800;font-size:60px;color:{C["teal"]};line-height:1">{i}</span>'
            f'<span style="font-size:44px;line-height:1.25;font-weight:500">{rich(x)}</span></div>'
            for i, x in enumerate(b["items"], 1))
        return f'<div style="display:flex;flex-direction:column;gap:22px">{rows}</div>'
    if "steps" in b:
        out = []
        for i, (t, d) in enumerate(b["steps"]):
            out.append(
                f'<div style="padding:32px 44px;background:{C["card"]};border-radius:24px;border-left:10px solid {C["teal"]}">'
                f'<div style="font-family:Archivo;font-weight:800;font-size:56px;line-height:1.05">{rich(t)}</div>'
                f'<div style="font-size:38px;line-height:1.3;color:{C["soft"]};margin-top:8px">{rich(d)}</div></div>')
            if i < len(b["steps"]) - 1:
                out.append(f'<div style="display:flex;justify-content:center"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="{C["violet"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14"/><path d="M6 13l6 6 6-6"/></svg></div>')
        return f'<div style="display:flex;flex-direction:column;gap:10px">{"".join(out)}</div>'
    if "cta" in b:
        return f'<p style="margin:0;padding:38px 48px;background:{C["teal"]};color:{C["bg"]};border-radius:24px;font-size:44px;line-height:1.25;font-weight:700">{rich(b["cta"])}</p>'
    raise ValueError(f"bloc necunoscut: {b}")


def page(blocks, idx, total):
    arrow = "" if idx == total else (
        f'<span style="display:flex;align-items:center;gap:16px;color:{C["txt"]}">{"Glisează" if idx == 1 else ""}'
        f'<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="{C["teal"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></span>')
    body = "".join(block(b) for b in blocks)
    return f"""<!doctype html><html lang="ro"><head><meta charset="utf-8"><style>
@font-face{{font-family:Archivo;src:url('file://{FONTS}/Archivo.ttf');font-weight:100 900}}
@font-face{{font-family:'DM Sans';src:url('file://{FONTS}/DMSans.ttf');font-weight:100 1000}}
body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1350px;box-sizing:border-box;padding:96px;background:{C['bg']};color:{C['txt']};font-family:'DM Sans';display:flex;flex-direction:column;justify-content:space-between">
<div style="display:flex;justify-content:space-between;font-size:28px;font-weight:700;letter-spacing:.12em"><span style="color:{C['teal']}">SORIN CRIȘAN</span><span style="color:{C['mute']}">{idx:02d} / {total:02d}</span></div>
<div style="display:flex;flex-direction:column;gap:48px">{body}</div>
<div style="display:flex;justify-content:space-between;align-items:center;font-size:30px;font-weight:500;color:{C['mute']}"><span>@crisansorin</span>{arrow}</div>
</div></body></html>"""


def main(spec_path, out_dir):
    from playwright.sync_api import sync_playwright
    fonts()
    spec = json.loads(pathlib.Path(spec_path).read_text())
    out = pathlib.Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    slides = spec["slides"]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, blocks in enumerate(slides, 1):
            tmp = out / f"_{i}.html"
            tmp.write_text(page(blocks, i, len(slides)))
            pg.goto(f"file://{tmp}")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(250)
            pg.screenshot(path=str(out / f"{i}.png"), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            tmp.unlink()
        b.close()
    print(f"{len(slides)} slide-uri in {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
