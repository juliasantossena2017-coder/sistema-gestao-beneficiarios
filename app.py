from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///beneficiarios.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Beneficiario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(150))
    bairro = db.Column(db.String(100))


class Doacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(150), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.String(20), nullable=False)
    responsavel = db.Column(db.String(100))


class Atendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beneficiario = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    observacoes = db.Column(db.Text)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/beneficiarios", methods=["GET", "POST"])
def beneficiarios():
    if request.method == "POST":
        novo = Beneficiario(
            nome=request.form["nome"],
            telefone=request.form["telefone"],
            endereco=request.form["endereco"],
            bairro=request.form["bairro"]
        )
        db.session.add(novo)
        db.session.commit()
        return redirect("/lista-beneficiarios")

    return render_template("beneficiarios.html")


@app.route("/lista-beneficiarios")
def lista_beneficiarios():
    pessoas = Beneficiario.query.all()
    return render_template("lista_beneficiarios.html", beneficiarios=pessoas)


@app.route("/editar-beneficiario/<int:id>", methods=["GET", "POST"])
def editar_beneficiario(id):
    pessoa = Beneficiario.query.get_or_404(id)

    if request.method == "POST":
        pessoa.nome = request.form["nome"]
        pessoa.telefone = request.form["telefone"]
        pessoa.endereco = request.form["endereco"]
        pessoa.bairro = request.form["bairro"]
        db.session.commit()
        return redirect("/lista-beneficiarios")

    return render_template("editar_beneficiario.html", pessoa=pessoa)


@app.route("/doacoes", methods=["GET", "POST"])
def doacoes():
    if request.method == "POST":
        nova = Doacao(
            descricao=request.form["descricao"],
            quantidade=request.form["quantidade"],
            data=request.form["data"],
            responsavel=request.form["responsavel"]
        )
        db.session.add(nova)
        db.session.commit()
        return redirect("/lista-doacoes")

    return render_template("doacoes.html")


@app.route("/lista-doacoes")
def lista_doacoes():
    registros = Doacao.query.all()
    return render_template("lista_doacoes.html", doacoes=registros)


@app.route("/atendimentos", methods=["GET", "POST"])
def atendimentos():
    if request.method == "POST":
        novo = Atendimento(
            beneficiario=request.form["beneficiario"],
            tipo=request.form["tipo"],
            data=request.form["data"],
            observacoes=request.form["observacoes"]
        )
        db.session.add(novo)
        db.session.commit()
        return redirect("/lista-atendimentos")

    return render_template("atendimentos.html")


@app.route("/lista-atendimentos")
def lista_atendimentos():
    registros = Atendimento.query.all()
    return render_template(
        "lista_atendimentos.html",
        atendimentos=registros
    )


@app.route("/relatorios")
def relatorios():
    total_beneficiarios = Beneficiario.query.count()
    total_doacoes = Doacao.query.count()
    total_quantidade_doada = db.session.query(
        db.func.sum(Doacao.quantidade)
    ).scalar() or 0
    total_atendimentos = Atendimento.query.count()

    return render_template(
        "relatorios.html",
        total_beneficiarios=total_beneficiarios,
        total_doacoes=total_doacoes,
        total_quantidade_doada=total_quantidade_doada,
        total_atendimentos=total_atendimentos
    )


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True) 