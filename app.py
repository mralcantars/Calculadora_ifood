from flask import Flask, render_template, request

app = Flask(__name__)
historico = []

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    lucro = None

    if request.method == "POST":
        try:
            preco_loja = float(request.form.get("preco_loja", 0))
            entrega = float(request.form.get("entrega", 0))
            campanha = float(request.form.get("campanha", 0))
            cupom = float(request.form.get("cupom", 0))
            comissao = float(request.form.get("comissao", 0))

            preco_sugerido = ((preco_loja + entrega + campanha) / (1 - comissao)) + cupom
            resultado = round(preco_sugerido, 2)
            preco_por_kg = round(resultado, 2)
            preco_100g = round(resultado / 10, 2)
            lucro = round(resultado - preco_loja, 2)

            historico.insert(0, {
                "preco_loja": preco_loja,
                "entrega": entrega,
                "campanha": campanha,
                "cupom": cupom,
                "comissao": comissao,
                "resultado": resultado,
                "preco_por_kg": preco_por_kg,
                "preco_100g": preco_100g,
                "lucro": lucro
            })

        except ValueError:
            resultado = "Erro: preencha todos os campos corretamente."

    return render_template("index.html", resultado=resultado, historico=historico)

@app.route("/explicacao")
def explicacao():
    return render_template("explicacao.html")

@app.route("/lucros")
def lucros():
    return render_template("lucros.html", historico=historico)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
