from supabase import create_client, Client
from config import Config


class SupabaseClient:
    def __init__(self):
        self.client: Client = create_client(
            Config.SUPABASE_URL,
            Config.SUPABASE_ANON_KEY
        )

    # ─── INSERT ───────────────────────────────────────────────────────────────
    def inserir_codigo(self, code: str) -> bool:
        """Insere um novo código. Retorna True se sucesso, False se duplicado."""
        try:
            self.client.table("scans").insert({ "code": code }).execute()
            return True
        except Exception:
            return False

    # ─── SELECT ───────────────────────────────────────────────────────────────
    def buscar_codigo_hoje(self, code: str) -> dict | None:
        """Busca um código gerado hoje. Retorna o registo ou None."""
        from datetime import date
        hoje = date.today().isoformat()
        amanha = date.today().replace(day=date.today().day + 1).isoformat()

        try:
            res = (
                self.client.table("scans")
                .select("*")
                .eq("code", code)
                .gte("created_at", f"{hoje}T00:00:00")
                .lt("created_at", f"{amanha}T00:00:00")
                .single()
                .execute()
            )
            return res.data
        except Exception:
            return None

    # ─── UPDATE ───────────────────────────────────────────────────────────────
    def marcar_como_resgatado(self, record_id: str) -> bool:
        """Marca um código como usado e regista a hora."""
        from datetime import datetime, timezone
        try:
            self.client.table("scans").update({
                "used": True,
                "used_at": datetime.now(timezone.utc).isoformat()
            }).eq("id", record_id).execute()
            return True
        except Exception:
            return False

    # ─── DADOS DO DIA ─────────────────────────────────────────────────────────
    def codigos_do_dia(self) -> list:
        """Retorna todos os códigos gerados hoje, ordenados do mais recente."""
        from datetime import date
        hoje = date.today().isoformat()
        amanha = date.today().replace(day=date.today().day + 1).isoformat()

        try:
            res = (
                self.client.table("scans")
                .select("*")
                .gte("created_at", f"{hoje}T00:00:00")
                .lt("created_at", f"{amanha}T00:00:00")
                .order("created_at", desc=True)
                .execute()
            )
            return res.data or []
        except Exception:
            return []