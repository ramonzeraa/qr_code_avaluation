import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
from services.code_service import CodeService
from services.supabase_client import SupabaseClient
from app import stats

# 🔥 EXEMPLO (depois você troca pelo Supabase)
db = SupabaseClient()
code_service = CodeService(db)

print(type(db))
data = db.client.table("scans").select("*").execute().data

def generate_chart(data, mode="month"):
    grouped = defaultdict(int)

    for d in data:
        dt = datetime.fromisoformat(d["created_at"])

        # 📅 DIA
        if mode == "day":
            key = dt.strftime("%Y-%m-%d")

        # 📊 SEMANA
        elif mode == "week":
            year, week, _ = dt.isocalendar()
            key = f"{year}-W{week}"

        # 📆 MÊS
        else:
            key = dt.strftime("%Y-%m")

        grouped[key] += 1

    labels = sorted(grouped.keys())
    values = [grouped[k] for k in labels]

    plt.style.use("seaborn-v0_8-darkgrid")

    plt.figure(figsize=(12,6))

    plt.bar(labels, values, color="#C9A84C")

    plt.title(
        f"Avaliações por {mode.upper()}",
        fontsize=16,
        fontweight="bold",
        color="#2C1F0E"
    )

    plt.xlabel("Período")
    plt.ylabel("Quantidade de Avaliações")

    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.2)

    plt.tight_layout()
    plt.savefig(f"grafico_{mode}.png", dpi=300)
    plt.show()
    
generate_chart(data, mode="day")
