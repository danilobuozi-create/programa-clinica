\
    from pathlib import Path
    from .repositories import ModeloRepo

    def bootstrap():
        repo = ModeloRepo()
        # Load examples if DB empty
        if not repo.list():
            base = Path(__file__).resolve().parents[1] / "templates_store" / "examples"
            for name in ["atestado.html","receita.html","contrato.html","prontuario.html"]:
                html = (base / name).read_text(encoding="utf-8")
                repo.create(name.replace(".html","").capitalize(), html, "html", {})
