import random
import string
from datetime import datetime, timezone


class CodeService:
    def __init__(self, db):
        self.db = db
        self._chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

    # ─── GERAÇÃO ──────────────────────────────────────────────────────────────
    def _gerar_code(self) -> str:
        """Gera um código aleatório no formato ALMA-XXXX-XXXX-XXX"""
        def bloco(n): return "".join(random.choices(self._chars, k=n))
        return f"ALMA-{bloco(4)}-{bloco(4)}-{bloco(3)}"

    def gerar_codigo_unico(self, max_tentativas: int = 10) -> str:
        """Gera e persiste um código único. Tenta até max_tentativas vezes."""
        for _ in range(max_tentativas):
            code = self._gerar_code()
            if self.db.inserir_codigo(code):
                return code
        raise Exception("Não foi possível gerar um código único. Tenta novamente.")

    # ─── VALIDAÇÃO ────────────────────────────────────────────────────────────
    def validar_e_resgatar(self, code: str) -> dict:
        """
        Valida e resgata um código.
        Retorna dict com: success, status, message, (e gerado_as se válido)
        """
        if not code.startswith("ALMA-"):
            return {
                "success": False,
                "status": "formato_invalido",
                "message": "Formato de código não reconhecido."
            }

        registo = self.db.buscar_codigo_hoje(code)

        if not registo:
            return {
                "success": False,
                "status": "nao_encontrado",
                "message": "Código não encontrado ou não gerado hoje."
            }

        if registo.get("used"):
            usado_as = registo.get("used_at")
            hora = self._formatar_hora(usado_as) if usado_as else ""
            return {
                "success": False,
                "status": "ja_utilizado",
                "message": f"Esta cortesia já foi resgatada{' às ' + hora if hora else ''}."
            }

        resgatado = self.db.marcar_como_resgatado(registo["id"])

        if not resgatado:
            return {
                "success": False,
                "status": "erro_update",
                "message": "Erro ao processar. Tenta novamente."
            }

        return {
            "success": True,
            "status": "valido",
            "message": "Válido! Pode liberar a cortesia.",
            "gerado_as": self._formatar_hora(registo.get("created_at"))
        }

    # ─── PAINEL ───────────────────────────────────────────────────────────────
    def dados_do_dia(self) -> dict:
        """Retorna estatísticas e lista de códigos do dia para o painel."""
        codigos = self.db.codigos_do_dia()
        total = len(codigos)
        resgatados = sum(1 for c in codigos if c.get("used"))

        lista = [
            {
                "code":       c["code"],
                "gerado_as":  self._formatar_hora(c.get("created_at")),
                "resgatado_as": self._formatar_hora(c.get("used_at")) if c.get("used") else None,
                "usado":      c.get("used", False)
            }
            for c in codigos
        ]

        return {
            "total_scans":   total,
            "total_codigos": total,
            "resgatados":    resgatados,
            "codigos":       lista
        }

    # ─── HELPERS ──────────────────────────────────────────────────────────────
    @staticmethod
    def _formatar_hora(iso_string: str | None) -> str:
        if not iso_string:
            return ""
        try:
            dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
            return dt.astimezone().strftime("%H:%M")
        except Exception:
            return ""