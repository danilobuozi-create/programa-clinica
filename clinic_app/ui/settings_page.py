    from PySide6 import QtWidgets
    from ..settings_manager import load_clinic_settings, save_clinic_settings

    class SettingsPage(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent); self._build(); self.load()

        def _build(self):
            f = QtWidgets.QFormLayout(self)
            self.edNome = QtWidgets.QLineEdit()
            self.edCNPJ = QtWidgets.QLineEdit()
            self.edCRO = QtWidgets.QLineEdit()
            self.edEPAO = QtWidgets.QLineEdit()
            self.edEnd = QtWidgets.QLineEdit()
            self.edTel = QtWidgets.QLineEdit()
            self.edEmail = QtWidgets.QLineEdit()
            self.edLogo = QtWidgets.QLineEdit()
            self.edAss = QtWidgets.QLineEdit()
            self.edResp = QtWidgets.QLineEdit()
            self.cbTema = QtWidgets.QComboBox(); self.cbTema.addItems(["light","dark"])
            f.addRow("Nome", self.edNome); f.addRow("CNPJ", self.edCNPJ); f.addRow("CRO", self.edCRO)
            f.addRow("EPAO", self.edEPAO); f.addRow("Endereço", self.edEnd); f.addRow("Telefone", self.edTel)
            f.addRow("E-mail", self.edEmail); f.addRow("Logo", self.edLogo); f.addRow("Assinatura", self.edAss)
            f.addRow("Responsável", self.edResp); f.addRow("Tema", self.cbTema)
            btn = QtWidgets.QPushButton("Salvar"); f.addRow(btn); btn.clicked.connect(self.save)

        def load(self):
            c = load_clinic_settings()
            self.edNome.setText(c.get("nome","")); self.edCNPJ.setText(c.get("cnpj",""))
            self.edCRO.setText(c.get("cro","")); self.edEPAO.setText(c.get("epao",""))
            self.edEnd.setText(c.get("endereco","")); self.edTel.setText(c.get("telefone",""))
            self.edEmail.setText(c.get("email","")); self.edLogo.setText(c.get("logo_path",""))
            self.edAss.setText(c.get("assinatura_path","")); self.edResp.setText(c.get("responsavel",""))
            self.cbTema.setCurrentText(c.get("tema","light"))

        def save(self):
            save_clinic_settings({
                "nome": self.edNome.text().strip(),
                "cnpj": self.edCNPJ.text().strip(),
                "cro": self.edCRO.text().strip(),
                "epao": self.edEPAO.text().strip(),
                "endereco": self.edEnd.text().strip(),
                "telefone": self.edTel.text().strip(),
                "email": self.edEmail.text().strip(),
                "logo_path": self.edLogo.text().strip(),
                "assinatura_path": self.edAss.text().strip(),
                "responsavel": self.edResp.text().strip(),
                "tema": self.cbTema.currentText(),
            })
            QtWidgets.QMessageBox.information(self,"OK","Configurações salvas.")
