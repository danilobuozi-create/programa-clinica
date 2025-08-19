# ClinicApp — Sistema Offline de Documentos (Python)

App desktop 100% offline para clínica odontológica: cadastre pacientes, crie/importe **modelos (HTML/Jinja2 ou DOCX convertido)** e gere **PDF** pronto para impressão.

## Como rodar
```bash
python -m venv .venv
. .venv/Scripts/activate     # Windows (no Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
python clinic_app/app.py
```

> Dica: Se o WeasyPrint não funcionar no seu Windows por faltar Cairo/Pango/GTK, o app usa fallback para **ReportLab** (render simples).

## Build (.exe)
```bash
pip install pyinstaller
pyinstaller --noconfirm --noconsole --name ClinicApp clinic_app/app.py       --add-data "clinic_app/assets;clinic_app/assets"       --add-data "clinic_app/templates_store;clinic_app/templates_store"       --add-data "clinic_app/settings;clinic_app/settings"
```
