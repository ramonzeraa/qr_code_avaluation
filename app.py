from flask import Flask, render_template, request, jsonify
from services.code_service import CodeService
from services.supabase_client import SupabaseClient
from services.qr_service import generate_qr
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SupabaseClient()
code_service = CodeService(db)


# ─── PÁGINA CLIENTE (QR aponta para cá) ───────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", google_url=Config.GOOGLE_REVIEW_URL)


# ─── GERAR CÓDIGO (chamado pelo JS da página cliente) ─────────────────────────
@app.route("/api/gerar-codigo", methods=["POST"])
def gerar_codigo():
    try:
        code = code_service.gerar_codigo_unico()
        return jsonify({ "success": True, "code": code })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500


# ─── VALIDAR CÓDIGO (garçom) ──────────────────────────────────────────────────
@app.route("/api/validar-codigo", methods=["POST"])
def validar_codigo():
    data = request.get_json()
    code = data.get("code", "").strip().upper()

    if not code:
        return jsonify({ "success": False, "status": "invalid", "message": "Código não fornecido." }), 400

    resultado = code_service.validar_e_resgatar(code)
    return jsonify(resultado)


# ─── PAINEL DO DONO ───────────────────────────────────────────────────────────
@app.route("/painel")
def painel():
    return render_template("painel.html")


# ─── API DO PAINEL (dados em tempo real) ──────────────────────────────────────
@app.route("/api/painel-dados", methods=["GET"])
def painel_dados():
    password = request.args.get("pw", "")
    if password != Config.OWNER_PASSWORD:
        return jsonify({ "success": False, "message": "Não autorizado." }), 401

    dados = code_service.dados_do_dia()
    return jsonify({ "success": True, **dados })


# ─── GARÇOM ───────────────────────────────────────────────────────────────────
@app.route("/garcom")
def garcom():
    return render_template("garcom.html")


# ─── HEALTH CHECK (Render precisa disto) ──────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({ "status": "ok" }), 200


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)