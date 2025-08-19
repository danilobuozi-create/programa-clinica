\
    import hashlib
    from datetime import datetime
    from pathlib import Path
    from typing import Dict, Any
    from jinja2 import Environment, BaseLoader, select_autoescape
    from .filters_br import cpf_format, telefone_format, currency, date, idade

    try:
        import weasyprint
    except Exception:
        weasyprint = None
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas as rcanvas
        from reportlab.lib.units import cm
    except Exception:
        A4 = None; rcanvas = None; cm = 28.3465

    class RenderService:
        def __init__(self):
            self.env = Environment(loader=BaseLoader(), autoescape=select_autoescape(['html','xml']))
            self.env.filters.update({
                "cpf_format": cpf_format,
                "telefone_format": telefone_format,
                "currency": currency,
                "date": date,
                "idade": idade,
            })

        def render_html(self, template_html: str, context: Dict[str, Any]) -> str:
            return self.env.from_string(template_html).render(**context)

        def _hash(self, html: str) -> str:
            return hashlib.sha256(html.encode("utf-8")).hexdigest()

        def html_to_pdf(self, html: str, out_path: Path) -> str:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            if weasyprint is not None:
                weasyprint.HTML(string=html).write_pdf(str(out_path))
                return str(out_path)
            # Fallback rudimentar: remove tags e grava texto com ReportLab
            if rcanvas is None: raise RuntimeError("Instale 'weasyprint' ou 'reportlab'.")
            c = rcanvas.Canvas(str(out_path), pagesize=A4)
            w,h = A4; t = c.beginText(2*cm, h-2*cm)
            import re
            for line in html.splitlines():
                clean = re.sub(r"<[^>]+>", "", line)
                t.textLine(clean)
                if t.getY() < 2*cm:
                    c.drawText(t); c.showPage(); t = c.beginText(2*cm, h-2*cm)
            c.drawText(t); c.save()
            return str(out_path)

        def render_to_pdf(self, template_html: str, context: Dict[str, Any], out_dir: Path):
            html = self.render_html(template_html, context)
            h = self._hash(html)
            out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
            name = f"documento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf = out_dir / name
            self.html_to_pdf(html, pdf)
            return str(pdf), h
