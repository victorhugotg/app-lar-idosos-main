from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'  # Necessário para usar sessões

# Lista para armazenar os dados dos pacientes e seus relatórios
pacientes = []

# Página de Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin1" and password == "12345678":
            session['user'] = username
            return redirect(url_for("home"))
        else:
            return "Credenciais inválidas. Tente novamente."
    return render_template("login.html")

# Página Inicial (cadastro ou busca de paciente)
@app.route("/home")
def home():
    return render_template("home.html")

# Página de cadastro de paciente
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        data_nascimento = request.form["data_nascimento"]
        idade = request.form["idade"]
        genero = request.form["genero"]
        estado_civil = request.form["estado_civil"]
        cpf = request.form["cpf"]
        rg = request.form["rg"]
        telefone = request.form["telefone"]
        endereco = request.form["endereco"]
        nome_responsavel = request.form.get("nome_responsavel", "")
        telefone_responsavel = request.form.get("telefone_responsavel", "")
        grau_parentesco = request.form.get("grau_parentesco", "")

        paciente = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "idade": idade,
            "genero": genero,
            "estado_civil": estado_civil,
            "cpf": cpf,
            "rg": rg,
            "telefone": telefone,
            "endereco": endereco,
            "nome_responsavel": nome_responsavel,
            "telefone_responsavel": telefone_responsavel,
            "grau_parentesco": grau_parentesco,
            "relatorios": [],
            "doencas_cronicas": "",
            "alergias": "",
            "medicamentos": "",
            "cirurgias": "",
            "historico_internacoes": "",
            "vacinas": "",
            "exames": "",
            "condicoes_cognitivas": "",
            "alteracoes_humor": "",
            "comportamento_social": "",
        }

        pacientes.append(paciente)
        return redirect(url_for("cadastrar_info_adicional", cpf=cpf))

    return render_template("cadastrar.html")

# Rota para cadastrar informações adicionais
@app.route("/cadastrar_info_adicional/<cpf>", methods=["GET", "POST"])
def cadastrar_info_adicional(cpf):
    paciente = next((p for p in pacientes if p["cpf"] == cpf), None)
    if not paciente:
        return "<h1>Paciente não encontrado.</h1><a href='/home'>Voltar ao início</a>"

    if request.method == "POST":
        paciente["doencas_cronicas"] = request.form.get("doencas_cronicas", "")
        paciente["alergias"] = request.form.get("alergias", "")
        paciente["medicamentos"] = request.form.get("medicamentos", "")
        paciente["cirurgias"] = request.form.get("cirurgias", "")
        paciente["historico_internacoes"] = request.form.get("historico_internacoes", "")
        paciente["vacinas"] = request.form.get("vacinas", "")
        paciente["exames"] = request.form.get("exames", "")
        paciente["condicoes_cognitivas"] = request.form.get("condicoes_cognitivas", "")
        paciente["alteracoes_humor"] = request.form.get("alteracoes_humor", "")
        paciente["comportamento_social"] = request.form.get("comportamento_social", "")

        return redirect(url_for("ver_relatorios", cpf=cpf))

    return render_template("cadastrar_info_adicional.html", paciente=paciente)

# Página de busca de paciente
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    if request.method == "POST":
        cpf = request.form["cpf"]
        for paciente in pacientes:
            if paciente["cpf"] == cpf:
                return redirect(url_for("ver_relatorios", cpf=cpf))
        return "<h1>Paciente não encontrado.</h1><a href='/home'>Voltar ao início</a>"
    return render_template("buscar.html")

# Página para visualizar e adicionar relatórios
@app.route("/ver_relatorios", methods=["GET", "POST"])
def ver_relatorios():
    cpf = request.args.get("cpf")
    paciente = next((p for p in pacientes if p["cpf"] == cpf), None)

    if not paciente:
        return "<h1>Paciente não encontrado.</h1><a href='/home'>Voltar ao início</a>"

    if request.method == "POST":
        if "adicionar_relatorio" in request.form:
            return redirect(url_for("adicionar_relatorio", cpf=cpf))
        elif "buscar_relatorio" in request.form:
            data = request.form["data"]
            relatorios_encontrados = [relatorio for relatorio in paciente["relatorios"] if relatorio["data"] == data]
            if relatorios_encontrados:
                return render_template("relatorio_por_data.html", relatorios=relatorios_encontrados, paciente=paciente)
            else:
                return "<h1>Nenhum relatório encontrado para essa data.</h1><a href='/home'>Voltar ao início</a>"

    return render_template("ver_relatorios.html", paciente=paciente)

from datetime import datetime

@app.route("/adicionar_relatorio/<cpf>", methods=["GET", "POST"])
def adicionar_relatorio(cpf):
    paciente = next((p for p in pacientes if p["cpf"] == cpf), None)

    if not paciente:
        return "<h1>Paciente não encontrado.</h1><a href='/home'>Voltar ao início</a>"

    if request.method == "POST":
        print(request.form)  # Para verificar o que está sendo enviado
        
        try:
            data = request.form["data"]
            hora = datetime.now().strftime("%H:%M")  # Captura a hora atual
            responsavel = request.form["responsavel"]  # Você pode modificar para usar 'admin1'
            sinais_vitais = {
                "pressao": request.form["pressao"],
                "frequencia_cardiaca": request.form["frequencia_cardiaca"],
                "temperatura": request.form["temperatura"]
            }
            estado_geral = {
                "consciencia": request.form["consciencia"],
                "dor": request.form["dor"]
            }
            alimentacao_hidratacao = {
                "refeicoes": request.form["refeicoes"],
                "hidratacao": request.form["hidratacao"]
            }
            mobilidade_higiene = {
                "mobilidade": request.form["mobilidade"],
                "higiene": request.form["higiene"]
            }
            medicamentos = request.form["medicamentos"]
            observacoes = request.form["observacoes"]

            relatorio = {
                "data": data,
                "hora": hora,  # Adiciona a hora ao relatório
                "responsavel": responsavel,
                "sinais_vitais": sinais_vitais,
                "estado_geral": estado_geral,
                "alimentacao_hidratacao": alimentacao_hidratacao,
                "mobilidade_higiene": mobilidade_higiene,
                "medicamentos": medicamentos,
                "observacoes": observacoes,
                "usuario": session.get('user', 'Desconhecido')  # Pega o usuário da sessão
            }

            paciente["relatorios"].append(relatorio)
            return redirect(url_for("ver_relatorios", cpf=cpf))
        except KeyError as e:
            return f"<h1>Erro: Campo {e} não encontrado no formulário.</h1>"

    return render_template("adicionar_relatorio.html", paciente=paciente)

if __name__ == "__main__":
    app.run(debug=True)