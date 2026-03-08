from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# Credenciais e IDs dos planos
PAYPAL_CLIENT_ID = "AS1J_fjGJDoc-hJWyMz5nfqfG-5XvKk3_w_jwARLltFePEogQmCvn68kxAoDMKr6ei8Cp2GJrwjr41lc"
PLAN_PRO_ID = "P-900473855S945552PNGU4B7Q"
PLAN_SCALE_ID = "P-096371535E2645918NGVQGKI"

# Itens do dashboard em memória
items = []

# Página inicial
@app.route("/")
def index():
    return render_template(
        "index.html",
        items=items,
        paypal_client_id=PAYPAL_CLIENT_ID,
        plan_pro_id=PLAN_PRO_ID,
        plan_scale_id=PLAN_SCALE_ID
    )

# Adicionar item no dashboard
@app.route("/add_item", methods=["POST"])
def add_item():
    name = request.form.get("name")
    if name:
        items.append(name)
    return redirect(url_for("index"))

# Webhook do PayPal
@app.route("/paypal-webhook", methods=["POST"])
def paypal_webhook():
    data = request.json
    event_type = data.get("event_type", "")

    if event_type == "BILLING.SUBSCRIPTION.ACTIVATED":
        print("Subscription Activated:", data)

    elif event_type == "PAYMENT.SALE.COMPLETED":
        print("Payment Completed:", data)

    elif event_type == "BILLING.SUBSCRIPTION.CANCELLED":
        print("Subscription Cancelled:", data)

    return jsonify({"status": "ok"}), 200

# Início da aplicação
if __name__ == "__main__":
    import os
    # Usa a porta do Railway se existir, senão localmente 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
