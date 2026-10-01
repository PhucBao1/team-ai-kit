# Sinh bản đầu của sơ đồ draw.io bằng code

Ba sơ đồ 01–03 được **sinh lần đầu** bằng các script này (Python viết XML draw.io → render bằng chính engine draw.io
trong Chromium headless → xuất `.drawio.svg` có kèm dữ liệu sửa được).

**Sau khi ai đó sửa tay trong draw.io, file `.drawio.svg` trong `docs/architecture/` là nguồn sự thật** — đừng chạy lại
script đè lên. Script chỉ để dựng sơ đồ mới cùng phong cách (màu, cỡ chữ, chú giải).

```bash
cd scripts/diagrams/drawio
B=https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp
mkdir -p js stencils && curl -so js/viewer-static.min.js $B/js/viewer-static.min.js && curl -so stencils/gcp2.xml $B/stencils/gcp2.xml
python3 d01_context.py                           # → 01-context.drawio (XML); d02_system_overview.py, d03_deployment.py
python3 -m http.server 8765 --bind 127.0.0.1 &   # viewer cần tải stencil qua http
npm i playwright && node render.js 01-context.drawio ../../../docs/architecture/01-context.drawio.svg /tmp/01.png
```
`dio.py`: box / group / cyl / icon (GCP `mxgraph.gcp2.*`) / edge / text, bảng màu dùng chung với sơ đồ Mermaid.
(`js/`, `stencils/` không commit — tải khi cần.)
