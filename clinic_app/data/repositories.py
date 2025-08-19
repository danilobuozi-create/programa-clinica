\
    import json
    from datetime import datetime
    from typing import Dict, Any, List, Optional
    from ..db.db import get_connection

    def now():
        return datetime.now().isoformat(timespec="seconds")

    class PacienteRepo:
        def create(self, data: Dict[str, Any]) -> int:
            conn = get_connection(); cur = conn.cursor()
            cols = ("nome","cpf","rg","sexo","nascimento","telefone","email","endereco","alergias","anamnese","obs","criado_em","atualizado_em")
            vals = [data.get(c) for c in cols[:-2]] + [now(), now()]
            cur.execute(f"INSERT INTO pacientes ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})", vals)
            conn.commit(); rid = cur.lastrowid; conn.close(); return rid

        def list(self) -> List[Dict[str, Any]]:
            conn = get_connection(); rows = conn.execute("SELECT * FROM pacientes ORDER BY nome").fetchall(); conn.close()
            return [dict(r) for r in rows]

        def get(self, pid: int) -> Optional[Dict[str, Any]]:
            conn = get_connection(); r = conn.execute("SELECT * FROM pacientes WHERE id=?", (pid,)).fetchone(); conn.close()
            return dict(r) if r else None

        def update(self, pid: int, data: Dict[str, Any]):
            conn = get_connection(); cur = conn.cursor()
            cols = ["nome","cpf","rg","sexo","nascimento","telefone","email","endereco","alergias","anamnese","obs","atualizado_em"]
            vals = [data.get(c) for c in cols[:-1]] + [now()]
            cur.execute(f"UPDATE pacientes SET {','.join([c+'=?' for c in cols])} WHERE id=?", (*vals, pid))
            conn.commit(); conn.close()

        def delete(self, pid: int):
            conn = get_connection(); conn.execute("DELETE FROM pacientes WHERE id=?", (pid,)); conn.commit(); conn.close()

    class ModeloRepo:
        def create(self, nome: str, conteudo_html: str, tipo: str="html", meta: Optional[dict]=None) -> int:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("""
                INSERT INTO modelos (nome, tipo, conteudo_html, meta, versao, criado_em, atualizado_em)
                VALUES (?, ?, ?, ?, 1, ?, ?)
            """, (nome, tipo, conteudo_html, json.dumps(meta or {}, ensure_ascii=False), now(), now()))
            conn.commit(); rid = cur.lastrowid; conn.close(); return rid

        def list(self) -> List[Dict[str, Any]]:
            conn = get_connection(); rows = conn.execute("SELECT id,nome,versao,atualizado_em FROM modelos ORDER BY atualizado_em DESC").fetchall(); conn.close()
            return [dict(r) for r in rows]

        def get(self, mid: int) -> Optional[Dict[str, Any]]:
            conn = get_connection(); r = conn.execute("SELECT * FROM modelos WHERE id=?", (mid,)).fetchone(); conn.close()
            return dict(r) if r else None

        def update(self, mid: int, nome: str, conteudo_html: str, meta: Optional[dict]=None):
            conn = get_connection()
            conn.execute("UPDATE modelos SET nome=?, conteudo_html=?, meta=?, versao=versao+1, atualizado_em=? WHERE id=?",
                         (nome, conteudo_html, json.dumps(meta or {}, ensure_ascii=False), now(), mid))
            conn.commit(); conn.close()

        def delete(self, mid: int):
            conn = get_connection(); conn.execute("DELETE FROM modelos WHERE id=?", (mid,)); conn.commit(); conn.close()

    class DocumentoRepo:
        def create(self, paciente_id: int, modelo_id: int, titulo: str, dados_json: dict, caminho_pdf: str, h: str):
            conn = get_connection()
            conn.execute("""
                INSERT INTO documentos (paciente_id, modelo_id, titulo, dados_json, caminho_pdf, hash, criado_em)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (paciente_id, modelo_id, titulo, json.dumps(dados_json, ensure_ascii=False), caminho_pdf, h, now()))
            conn.commit(); conn.close()

        def list_by_paciente(self, pid: int) -> List[Dict[str, Any]]:
            conn = get_connection(); rows = conn.execute("SELECT * FROM documentos WHERE paciente_id=? ORDER BY criado_em DESC", (pid,)).fetchall(); conn.close()
            return [dict(r) for r in rows]
