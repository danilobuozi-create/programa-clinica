from PySide6 import QtWidgets
from .patients_page import PatientsPage
from .templates_page import TemplatesPage
from .merge_page import MergePage
from .settings_page import SettingsPage

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClinicApp — Documentos Offline")
        self.resize(1100, 720)
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(PatientsPage(), "Pacientes")
        tabs.addTab(TemplatesPage(), "Modelos")
        tabs.addTab(MergePage(), "Mesclar & PDF")
        tabs.addTab(SettingsPage(), "Configurações")
        self.setCentralWidget(tabs)
        self.statusBar().showMessage("Pronto")    
