import pytest
from app import app, db


@pytest.fixture
def cliente():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        with app.test_client() as cliente:
            yield cliente

        db.session.remove()
        db.drop_all()


def test_pagina_inicial(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200


def test_pagina_beneficiarios(cliente):
    resposta = cliente.get("/beneficiarios")
    assert resposta.status_code == 200


def test_pagina_doacoes(cliente):
    resposta = cliente.get("/doacoes")
    assert resposta.status_code == 200


def test_pagina_atendimentos(cliente):
    resposta = cliente.get("/atendimentos")
    assert resposta.status_code == 200


def test_pagina_relatorios(cliente):
    resposta = cliente.get("/relatorios")
    assert resposta.status_code == 200