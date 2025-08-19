    from PySide6 import QtWidgets
    from ..data.repositories import PacienteRepo

    class PatientsPage(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.repo = PacienteRepo()
            self._build(); self.refresh()

        def _build(self):
            lay = QtWidgets.QVBoxLayout(self)
            self.table = QtWidgets.QTableWidget(0,5)
            self.table.setHorizontalHeaderLabels(["ID","Nome","CPF","Telefone","Email"])
            self.table.horizontalHeader().setStretchLastSection(True)
            lay.addWidget(self.table)

            form = QtWidgets.QFormLayout()
            self.edNome = QtWidgets.QLineEdit()
            self.edCPF = QtWidgets.QLineEdit()
            self.edRG = QtWidgets.QLineEdit()
            self.edSexo = QtWidgets.QLineEdit()
            self.edNasc = QtWidgets.QLineEdit()
            self.edTel = QtWidgets.QLineEdit()
            self.edEmail = QtWidgets.QLineEdit()
            self.edEnd = QtWidgets.QLineEdit()
            self.edAler = QtWidgets.QLineEdit()
            self.edAnam = QtWidgets.QLineEdit()
            self.edObs = QtWidgets.QLineEdit()
            form.addRow("Nome*", self.edNome); form.addRow("CPF", self.edCPF); form.addRow("RG", self.edRG)
            form.addRow("Sexo", self.edSexo); form.addRow("Nascimento YYYY-MM-DD", self.edNasc)
            form.addRow("Telefone", self.edTel); form.addRow("Email", self.edEmail)
            form.addRow("Endereço", self.edEnd); form.addRow("Alergias", self.edAler)
            form.addRow("Anamnese", self.edAnam); form.addRow("Obs", self.edObs)
            lay.addLayout(form)

            btns = QtWidgets.QHBoxLayout()
            self.btnSalvar = QtWidgets.QPushButton("Salvar/Atualizar")
            self.btnExcluir = QtWidgets.QPushButton("Excluir selecionado")
            self.btnLimpar = QtWidgets.QPushButton("Limpar")
            btns.addWidget(self.btnSalvar); btns.addWidget(self.btnExcluir); btns.addWidget(self.btnLimpar)
            lay.addLayout(btns)

            self.btnSalvar.clicked.connect(self.on_save)
            self.btnExcluir.clicked.connect(self.on_delete)
            self.btnLimpar.clicked.connect(self.on_clear)

        def refresh(self):
            data = self.repo.list()
            self.table.setRowCount(0)
            for r in data:
                i = self.table.rowCount(); self.table.insertRow(i)
                self.table.setItem(i,0, QtWidgets.QTableWidgetItem(str(r["id"])))
                self.table.setItem(i,1, QtWidgets.QTableWidgetItem(r.get("nome","")))
                self.table.setItem(i,2, QtWidgets.QTableWidgetItem(r.get("cpf","")))
                self.table.setItem(i,3, QtWidgets.QTableWidgetItem(r.get("telefone","")))
                self.table.setItem(i,4, QtWidgets.QTableWidgetItem(r.get("email","")))

        def _collect(self):
            return {
                "nome": self.edNome.text().strip(),
                "cpf": self.edCPF.text().strip(),
                "rg": self.edRG.text().strip(),
                "sexo": self.edSexo.text().strip(),
                "nascimento": self.edNasc.text().strip(),
                "telefone": self.edTel.text().strip(),
                "email": self.edEmail.text().strip(),
                "endereco": self.edEnd.text().strip(),
                "alergias": self.edAler.text().strip(),
                "anamnese": self.edAnam.text().strip(),
                "obs": self.edObs.text().strip(),
            }

        def on_save(self):
            d = self._collect()
            if not d["nome"]:
                QtWidgets.QMessageBox.warning(self,"Atenção","Nome é obrigatório.")
                return
            row = self.table.currentRow()
            if row >= 0:
                try:
                    pid = int(self.table.item(row,0).text())
                    self.repo.update(pid, d)
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self,"Erro",str(e))
                    return
            else:
                self.repo.create(d)
            self.refresh(); self.on_clear()

        def on_delete(self):
            row = self.table.currentRow()
            if row < 0: return
            pid = int(self.table.item(row,0).text())
            if QtWidgets.QMessageBox.question(self,"Confirmar","Excluir paciente?")==QtWidgets.QMessageBox.Yes:
                self.repo.delete(pid); self.refresh()

        def on_clear(self):
            for w in [self.edNome,self.edCPF,self.edRG,self.edSexo,self.edNasc,self.edTel,self.edEmail,self.edEnd,self.edAler,self.edAnam,self.edObs]:
                w.clear()
