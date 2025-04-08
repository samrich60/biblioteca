from flask import Flask, render_template, request, redirect, url_for, session
import random
import string

app = Flask(__name__)
app.secret_key = 'biblioteca_segura'

livros_disponiveis = [
    {"id": 1, "titulo": "Dom Casmurro", "valor": 10.0, "imagem": "dom.jpg",
        "categoria": "Romance", "resumo": "Um clássico de Machado de Assis sobre amor e ciúmes."},
    {"id": 2, "titulo": "O Cortiço", "valor": 12.0, "imagem": "cortico.jpg",
        "categoria": "Romance", "resumo": "Uma obra naturalista que retrata a vida em um cortiço."},
    {"id": 3, "titulo": "Memórias Póstumas de Brás Cubas", "valor": 13.0, "imagem": "memorias.jpg",
        "categoria": "Filosofia", "resumo": "Narrativa filosófica de um defunto-autor."},
    {"id": 4, "titulo": "1984", "valor": 15.0, "imagem": "1984.jpg", "categoria": "Ficção Científica",
        "resumo": "Distopia de George Orwell sobre um regime totalitário."},
    {"id": 5, "titulo": "Admirável Mundo Novo", "valor": 14.5, "imagem": "admiravel.jpg",
        "categoria": "Ficção Científica", "resumo": "Uma sociedade futurista controlada pela engenharia genética."},
    {"id": 6, "titulo": "Orgulho e Preconceito", "valor": 11.5, "imagem": "orgulho.jpg", "categoria": "Romance",
        "resumo": "Romance clássico de Jane Austen sobre relacionamentos e classe social."},
    {"id": 7, "titulo": "Frankenstein", "valor": 13.5, "imagem": "frankenstein.jpg", "categoria": "Terror",
        "resumo": "O cientista Victor Frankenstein cria um monstro em seu laboratório."},
    {"id": 8, "titulo": "Drácula", "valor": 13.0, "imagem": "dracula.jpg",
        "categoria": "Terror", "resumo": "O famoso vampiro da Transilvânia chega à Inglaterra."},
    {"id": 9, "titulo": "O Hobbit", "valor": 16.0, "imagem": "hobbit.jpg",
        "categoria": "Fantasia", "resumo": "A jornada de Bilbo Bolseiro em uma aventura épica."},
    {"id": 10, "titulo": "Harry Potter e a Pedra Filosofal", "valor": 18.0, "imagem": "hp1.jpg",
        "categoria": "Fantasia", "resumo": "O começo da jornada de Harry Potter no mundo da magia."},
    {"id": 11, "titulo": "Senhor dos Anéis: A Sociedade do Anel", "valor": 20.0, "imagem": "lotr1.jpg",
        "categoria": "Fantasia", "resumo": "Frodo começa sua missão para destruir o Um Anel."},
    {"id": 12, "titulo": "O Pequeno Príncipe", "valor": 9.0, "imagem": "principe.jpg",
        "categoria": "Infantil", "resumo": "Um conto poético sobre a vida e os sentimentos."},
    {"id": 13, "titulo": "Alice no País das Maravilhas", "valor": 10.0, "imagem": "alice.jpg",
        "categoria": "Infantil", "resumo": "A incrível viagem de Alice por um mundo de fantasia."},
    {"id": 14, "titulo": "Percy Jackson: O Ladrão de Raios", "valor": 17.0, "imagem": "percy.jpg",
        "categoria": "Aventura", "resumo": "O jovem semideus precisa impedir uma guerra entre deuses."},
    {"id": 15, "titulo": "O Código Da Vinci", "valor": 16.5, "imagem": "codigo.jpg",
        "categoria": "Suspense", "resumo": "Conspirações e enigmas envolvendo a Igreja e a arte."},
    {"id": 16, "titulo": "Sherlock Holmes: Um Estudo em Vermelho", "valor": 14.0, "imagem": "sherlock.jpg",
        "categoria": "Mistério", "resumo": "A primeira investigação de Holmes e Watson."},
    {"id": 17, "titulo": "A Revolução dos Bichos", "valor": 11.0, "imagem": "bichos.jpg",
        "categoria": "Política", "resumo": "Fábula satírica sobre o totalitarismo."},
    {"id": 18, "titulo": "O Apanhador no Campo de Centeio", "valor": 12.5, "imagem": "apanhador.jpg",
        "categoria": "Drama", "resumo": "As angústias de um adolescente rebelde em Nova York."},
    {"id": 19, "titulo": "Capitães da Areia", "valor": 13.5, "imagem": "capitaes.jpg",
        "categoria": "Drama", "resumo": "A vida de meninos de rua em Salvador."},
    {"id": 20, "titulo": "A Metamorfose", "valor": 12.0, "imagem": "metamorfose.jpg",
        "categoria": "Filosofia", "resumo": "Kafka narra a transformação de um homem em inseto."},
]

reservas = []


@app.route("/")
def index():
    return render_template("index.html", livros=livros_disponiveis)


@app.route("/adicionar_carrinho", methods=["POST"])
def adicionar_carrinho():
    livro_id = int(request.form["livro_id"])
    if "carrinho" not in session:
        session["carrinho"] = []
    if livro_id not in session["carrinho"]:
        session["carrinho"].append(livro_id)
    session.modified = True
    return redirect(url_for("carrinho"))


@app.route("/remover_livro", methods=["POST"])
def remover_livro():
    livro_id = int(request.form["livro_id"])
    if "carrinho" in session and livro_id in session["carrinho"]:
        session["carrinho"].remove(livro_id)
        session.modified = True
    return redirect(url_for("ver_carrinho"))


@app.route("/carrinho")
def carrinho():
    carrinho_ids = session.get("carrinho", [])
    livros_carrinho = [
        livro for livro in livros_disponiveis if livro["id"] in carrinho_ids]
    return render_template("carrinho.html", livros=livros_carrinho)


@app.route("/reservar", methods=["POST"])
def reservar():
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    carrinho_ids = session.get("carrinho", [])
    livros_reservados = [
        livro for livro in livros_disponiveis if livro["id"] in carrinho_ids]

    if livros_reservados:
        codigo = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6))
        reservas.append({
            "codigo": codigo,
            "nome": nome,
            "cpf": cpf,
            "livros": livros_reservados
        })
        session.pop("carrinho", None)
        return render_template("codigo.html", codigo=codigo)
    return "Nenhum livro no carrinho", 400


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/buscar_reserva", methods=["POST"])
def buscar_reserva():
    codigo = request.form["codigo"]
    reserva = next((r for r in reservas if r["codigo"] == codigo), None)
    return render_template("resultado.html", reserva=reserva)
