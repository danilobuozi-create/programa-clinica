import sys
from PySide6 import QtWidgets
from clinic_app.db.db import init_db
from clinic_app.ui.main_window import MainWindow
from clinic_app.data.bootstrap_models import bootstrap

def main():
    init_db()
    try:
        bootstrap()
    except Exception:
        pass
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
