    from pathlib import Path
    from PySide6 import QtWidgets, QtCore
    from ..data.repositories import ModeloRepo
    from ..render.renderer import RenderService

    class TemplatesPage(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.repo = ModeloRepo(); self.renderer = RenderService()
            self._build(); self.refresh()

        def _build(self):
            lay = QtWidgets.QVBoxLayout(self)
            self.list = QtWidgets.QListWidget(); lay.addWidget(self.list)
            form = QtWidgets.QFormLayout()
            self.edNome = QtWidgets.QLineEdit()
            form.addRow("Nome do modelo*", self.edNome)
            lay.addLayout(form)
            self.edHtml = QtWidgets.QPlainTextEdit(); self.edHtml.setPlaceholderText("HTML + Jinja2")
            self.edHtml.setMinimumHeight(220); lay.addWidget(self.edHtml)
            row = QtWidgets.QHBoxLayout()
            self.btnNovo = QtWidgets.QPushButton("Novo")
            self.btnSalvar = QtWidgets.QPushButton("Salvar")
            self.btnExcluir = QtWidgets.QPushButton("Excluir")
            self.btnDocx = QtWidgets.QPushButton("Importar DOCX")
            self.btnPreview = QtWidgets.QPushButton("Pré-visualizar")
            row.addWidget(self.btnNovo); row.addWidget(self.btnSalvar); row.addWidget(self.btnExcluir)
            row.addWidget(self.btnDocx); row.addWidget(self.btnPreview)
            lay.addLayout(row)

            self.list.itemSelectionChanged.connect(self.on_sel)
            self.btnNovo.clicked.connect(self.on_new)
            self.btnSalvar.clicked.connect(self.on_save)
            self.btnExcluir.clicked.connect(self.on_del)
            self.btnDocx.clicked.connect(self.on_docx)
            self.btnPreview.clicked.connect(self.on_preview)

        def refresh(self):
            self.list.clear()
            for m in self.repo.list():
                it = QtWidgets.QListWidgetItem(f'#{m["id"]} — {m["nome"]} (v{m["versao"]})')
                it.setData(QtCore.Qt.UserRole, m["id"]); self.list.addItem(it)

        def on_new(self):
            self.edNome.clear(); self.edHtml.clear(); self.list.clearSelection()

        def on_save(self):
            nome = self.edNome.text().strip(); html = self.edHtml.toPlainText()
            if not nome or not html:
                QtWidgets.QMessageBox.warning(self,"Atenção","Informe nome e conteúdo.")
                return
            sel = self.list.currentItem()
            if sel:
                self.repo.update(sel.data(QtCore.Qt.UserRole), nome, html, {})
            else:
                self.repo.create(nome, html, "html", {})
            self.refresh()

        def on_del(self):
            sel = self.list.currentItem()
            if not sel: return
            if QtWidgets.QMessageBox.question(self,"Confirmar","Excluir modelo?")==QtWidgets.QMessageBox.Yes:
                self.repo.delete(sel.data(QtCore.Qt.UserRole)); self.refresh(); self.on_new()

        def on_sel(self):
            sel = self.list.currentItem()
            if not sel: return
            m = self.repo.get(sel.data(QtCore.Qt.UserRole))
            if m: self.edNome.setText(m["nome"]); self.edHtml.setPlainText(m["conteudo_html"])

        def on_docx(self):
            try:
                import mammoth
            except Exception:
                QtWidgets.QMessageBox.information(self,"Falta dependência","Instale 'mammoth' para importar DOCX.")
                return
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Selecionar DOCX", "", "DOCX (*.docx)")
            if not path: return
            with open(path, "rb") as f:
                html = mammoth.convert_to_html(f).value
            self.edHtml.setPlainText(html)
            if not self.edNome.text(): self.edNome.setText(Path(path).stem)

        def on_preview(self):
            try:
                html = self.renderer.render_html(self.edHtml.toPlainText(), {})
            except Exception as e:
                QtWidgets.QMessageBox.critical(self,"Erro no template", str(e)); return
            import tempfile, webbrowser
            fd, tmp = tempfile.mkstemp(suffix=".html"); Path(tmp).write_text(html, encoding="utf-8")
            webbrowser.open(f"file://{tmp}")
