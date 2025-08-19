    from pathlib import Path
    from datetime import datetime
    from PySide6 import QtWidgets, QtCore
    from ..data.repositories import PacienteRepo, ModeloRepo, DocumentoRepo
    from ..render.renderer import RenderService
    from ..settings_manager import load_clinic_settings

    class MergePage(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.p_repo = PacienteRepo(); self.m_repo = ModeloRepo(); self.d_repo = DocumentoRepo()
            self.renderer = RenderService()
            self._build(); self.refresh_selectors()

        def _build(self):
            lay = QtWidgets.QVBoxLayout(self)
            row = QtWidgets.QHBoxLayout()
            self.cbPac = QtWidgets.QComboBox(); self.cbMod = QtWidgets.QComboBox()
            row.addWidget(QtWidgets.QLabel("Paciente:")); row.addWidget(self.cbPac, 2)
            row.addWidget(QtWidgets.QLabel("Modelo:")); row.addWidget(self.cbMod, 2)
            lay.addLayout(row)

            self.edExtras = QtWidgets.QPlainTextEdit()
            self.edExtras.setPlaceholderText("Extras (um por linha):\nchave=valor\nEx.: cid=K04.7\nprocedimento=Endodontia\nhora_inicio=08:00\nhora_fim=10:40\nrepouso_dias=1")
            lay.addWidget(self.edExtras)

            out = QtWidgets.QHBoxLayout()
            self.edDir = QtWidgets.QLineEdit(str(Path.home() / "Documents" / "ClinicDocs"))
            self.btnDir = QtWidgets.QPushButton("Alterar pasta...")
            out.addWidget(QtWidgets.QLabel("Salvar em:")); out.addWidget(self.edDir, 1); out.addWidget(self.btnDir)
            lay.addLayout(out)

            btns = QtWidgets.QHBoxLayout()
            self.btnCheck = QtWidgets.QPushButton("Verificar variáveis")
            self.btnPDF = QtWidgets.QPushButton("Gerar PDF")
            btns.addWidget(self.btnCheck); btns.addWidget(self.btnPDF); lay.addLayout(btns)

            self.listDocs = QtWidgets.QListWidget(); lay.addWidget(QtWidgets.QLabel("Documentos recentes:")); lay.addWidget(self.listDocs)

            self.btnDir.clicked.connect(self.on_dir)
            self.btnCheck.clicked.connect(self.on_check)
            self.btnPDF.clicked.connect(self.on_pdf)
            self.cbPac.currentIndexChanged.connect(self.refresh_docs)

        def refresh_selectors(self):
            self._pacs = self.p_repo.list()
            self._mods = [self.m_repo.get(m["id"]) for m in self.m_repo.list()]
            self.cbPac.clear(); self.cbMod.clear()
            for p in self._pacs: self.cbPac.addItem(f'{p["nome"]} (#{p["id"]})', p["id"])
            for m in self._mods: self.cbMod.addItem(f'{m["nome"]} (v{m["versao"]})', m["id"])
            self.refresh_docs()

        def on_dir(self):
            d = QtWidgets.QFileDialog.getExistingDirectory(self, "Selecionar pasta")
            if d: self.edDir.setText(d)

        def _extras(self):
            d = {}
            for line in self.edExtras.toPlainText().splitlines():
                if "=" in line:
                    k,v = line.split("=",1); d[k.strip()] = v.strip()
            return d

        def _context(self):
            if self.cbPac.currentIndex()<0 or self.cbMod.currentIndex()<0: return None, None, None
            pid = self.cbPac.currentData(); mid = self.cbMod.currentData()
            pac = next((x for x in self._pacs if x["id"]==pid), None)
            mod = next((x for x in self._mods if x["id"]==mid), None)
            clinica = load_clinic_settings()
            usuario = {"nome": clinica.get("responsavel",""), "cro": clinica.get("cro","")}
            ctx = {"paciente": pac or {}, "clinica": clinica, "procedimentos": [], "usuario": usuario, "extras": self._extras(), "hoje": datetime.now()}
            return pac, mod, ctx

        def on_check(self):
            from ..data.validators import missing_in_context
            pac, mod, ctx = self._context()
            if not mod:
                QtWidgets.QMessageBox.information(self,"Atenção","Selecione um modelo."); return
            miss = missing_in_context(mod["conteudo_html"], ctx)
            if miss: QtWidgets.QMessageBox.information(self,"Atenção","Variáveis possivelmente ausentes:\n- " + "\\n- ".join(miss))
            else: QtWidgets.QMessageBox.information(self,"OK","Tudo certo.")

        def on_pdf(self):
            pac, mod, ctx = self._context()
            if not pac or not mod:
                QtWidgets.QMessageBox.information(self,"Atenção","Selecione paciente e modelo."); return
            out_dir = Path(self.edDir.text().strip()); out_dir.mkdir(parents=True, exist_ok=True)
            try:
                pdf, h = self.renderer.render_to_pdf(mod["conteudo_html"], ctx, out_dir)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro", str(e)); return
            titulo = f'{mod["nome"]} - {pac["nome"]}'
            self.d_repo.create(pac["id"], mod["id"], titulo, ctx, pdf, h)
            QtWidgets.QMessageBox.information(self,"OK", f"PDF gerado em:\\n{pdf}")
            self.refresh_docs()

        def refresh_docs(self):
            self.listDocs.clear()
            if self.cbPac.currentIndex()<0: return
            pid = self.cbPac.currentData()
            for d in self.d_repo.list_by_paciente(pid):
                self.listDocs.addItem(f'{d["criado_em"]} — {d.get("titulo","")} → {d.get("caminho_pdf","")}')
