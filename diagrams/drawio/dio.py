"""Helper sinh XML draw.io."""

from xml.sax.saxutils import escape, quoteattr

C = {  # màu theo loại
    "llm": ("#ede9fe", "#7c3aed"),
    "code": ("#ecfdf5", "#059669"),
    "write": ("#fff7ed", "#ea580c"),
    "human": ("#fef9c3", "#ca8a04"),
    "data": ("#eff6ff", "#2563eb"),
    "ext": ("#f3f4f6", "#6b7280"),
    "white": ("#ffffff", "#9ca3af"),
}


class D:
    def __init__(self, name):
        self.name, self.cells, self.n = name, [], 0

    def _id(self, i):
        if i:
            return i
        self.n += 1
        return f"c{self.n}"

    def box(
        self,
        x,
        y,
        w,
        h,
        title,
        sub="",
        kind="code",
        id=None,
        extra="",
        size=13,
        parent="1",
        dashed=False,
        rounded=True,
    ):
        f, s = C[kind]
        label = f"<b>{escape(title)}</b>" + (
            f"<br><font style='font-size:{size - 2}px'>{escape(sub).replace(chr(10), '<br>')}</font>"
            if sub
            else ""
        )
        st = (
            f"rounded={1 if rounded else 0};arcSize=8;whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};fontSize={size};"
            f"fontColor=#111827;strokeWidth=1.5;spacing=6;{'dashed=1;' if dashed else ''}{extra}"
        )
        return self._cell(id, label, st, x, y, w, h, parent)

    def group(self, x, y, w, h, title, kind="llm", id=None, dashed=False, extra=""):
        f, s = C[kind]
        st = (
            f"rounded=1;arcSize=3;whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};fontSize=13;fontStyle=1;"
            f"verticalAlign=top;align=left;spacingLeft=10;spacingTop=4;strokeWidth=2;fontColor=#111827;"
            f"{'dashed=1;dashPattern=6 4;' if dashed else ''}container=0;{extra}"
        )
        return self._cell(id, escape(title), st, x, y, w, h, "1")

    def cyl(self, x, y, w, h, title, sub="", kind="data", id=None):
        f, s = C[kind]
        label = f"<b>{escape(title)}</b>" + (
            f"<br><font style='font-size:11px'>{escape(sub)}</font>" if sub else ""
        )
        st = f"shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;size=10;fillColor={f};strokeColor={s};fontSize=13;strokeWidth=1.5;fontColor=#111827;"
        return self._cell(id, label, st, x, y, w, h, "1")

    def icon(self, x, y, shape, title, sub="", id=None, size=44, color="#4284F3", top=False):
        label = f"<b>{escape(title)}</b>" + (
            f"<br><font style='font-size:10px' color='#4b5563'>{escape(sub).replace(chr(10), '<br>')}</font>"
            if sub
            else ""
        )
        st = (
            f"shape=mxgraph.gcp2.{shape};fillColor={color};strokeColor=none;html=1;verticalLabelPosition={'top' if top else 'bottom'};"
            f"verticalAlign={'bottom' if top else 'top'};labelPosition=center;align=center;fontSize=12;fontColor=#111827;"
        )
        return self._cell(id, label, st, x, y, size, size, "1", labelw=True)

    def text(self, x, y, w, h, html, size=12, align="left", id=None, extra=""):
        st = f"text;html=1;whiteSpace=wrap;align={align};verticalAlign=middle;fontSize={size};fontColor=#111827;{extra}"
        return self._cell(id, html, st, x, y, w, h, "1")

    def edge(
        self,
        s,
        t,
        label="",
        dashed=False,
        color="#374151",
        pts=None,
        extra="",
        both=False,
        exitX=None,
        exitY=None,
        entryX=None,
        entryY=None,
        lpos=None,
    ):
        st = (
            f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor={color};strokeWidth=1.6;fontSize=11;"
            f"fontColor=#111827;labelBackgroundColor=#ffffff;endArrow=block;endFill=1;jumpStyle=arc;jumpSize=10;"
            f"{'dashed=1;' if dashed else ''}{'startArrow=block;startFill=1;' if both else ''}"
        )
        for k, v in (("exitX", exitX), ("exitY", exitY), ("entryX", entryX), ("entryY", entryY)):
            if v is not None:
                st += f"{k}={v};"
        st += extra
        i = self._id(None)
        xattr = "" if lpos is None else f' x="{lpos}"'
        geo = "<mxGeometry" + xattr + ' relative="1" as="geometry">'
        if pts:
            geo += (
                '<Array as="points">'
                + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in pts)
                + "</Array>"
            )
        geo += "</mxGeometry>"
        self.cells.append(
            f'<mxCell id="{i}" value={quoteattr(escape(label))} style="{st}" edge="1" parent="1" source="{s}" target="{t}">{geo}</mxCell>'
        )
        return i

    def _cell(self, id, label, st, x, y, w, h, parent, labelw=False):
        i = self._id(id)
        self.cells.append(
            f'<mxCell id="{i}" value={quoteattr(label)} style="{st}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        return i

    def xml(self):
        body = "".join(self.cells)
        return (
            f'<mxfile host="drawio" agent="ev-cx-agent generator"><diagram id="{self.name}" name="{self.name}">'
            f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
            f'page="0" pageScale="1" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>{body}'
            f"</root></mxGraphModel></diagram></mxfile>"
        )
