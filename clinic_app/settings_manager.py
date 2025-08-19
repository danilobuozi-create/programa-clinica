\
    import json
    from pathlib import Path

    CONFIG_FILE = Path(__file__).resolve().parent / "settings" / "config.json"

    def load_clinic_settings() -> dict:
        try:
            data = json.loads(Path(CONFIG_FILE).read_text(encoding="utf-8"))
            return data.get("clinica", {})
        except Exception:
            return {}

    def save_clinic_settings(clinica: dict):
        root = {"clinica": clinica}
        Path(CONFIG_FILE).parent.mkdir(parents=True, exist_ok=True)
        Path(CONFIG_FILE).write_text(json.dumps(root, indent=2, ensure_ascii=False), encoding="utf-8")
