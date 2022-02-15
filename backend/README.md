<div align="center">
  <img src = "https://img.icons8.com/fluency/100/000000/movie.png">
  <h1><b>MASTERCODE FILMS API</b></h1>
  <p>Uma plataforma de streaming em desenvolvimento.<p>
  <img src="https://img.shields.io/github/license/josuelopes512/WstsideFilmes.svg">
  <img src="https://img.shields.io/github/forks/josuelopes512/WstsideFilmes.svg">
  <img src="https://img.shields.io/github/stars/josuelopes512/WstsideFilmes.svg">
  <img src="https://img.shields.io/github/issues/josuelopes512/WstsideFilmes.svg">
</div>


# 🧩 APIs Utilizadas:
- [TMDB's API](https://www.themoviedb.org/documentation/api)
- [API Warezcdn](https://warezcdn.com/docs.php)

# 👨‍💻 Linguagens utilizadas:
<div align="center">
  <img src = "https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
  <img src = "https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white">
 <img src = "https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src = "https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
 <img src = "https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
 <img src = "	https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E">
</div>

# 🛠 Ajustes e Melhorias:
- [ ] Refatorar
- [ ] Tornar totalmente responsivo.
- [ ] Melhorar design da interface.
- [ ] Hospedar Site.

# 💻 Instalando o Mastercode Films API.
#### Para rodar o Mastercode Films em sua máquina, siga estas etapas:
- Você precisará do python em sua máquina.
- Instale o Virtualenv.
  - ``` python3 -m venv venv```
- Ative o Virtualenv:
  - (Para PowerShell)
  - ``` .\venv\Scripts\activate```
  - (Para CMD)
  - ``` venv\Scripts\activate.bat```
  - (Para Linux, Git Bash)
  - ```source venv/Scripts/activate```
  - Você pode encontrar todo o manual de instalação do virtualenv [aqui](https://virtualenv.pypa.io/en/latest/installation.html)
- Atualize o pip.
  - ``` pip install -U pip```
- Instale as dependências do projeto.
  - ``` pip install -r requirements.txt```
- Adicione o valor da [chave da api](https://www.themoviedb.org/documentation/api) na variável local.
  - Renomeie o arquivo chamado ```.env_example``` para ```.env```
  - Adicione a chave da api fornecida pelo https://api.themoviedb.org/
  - Adicione no campo SECRET_KEY
    - Para gerar a SECRET_KEY
    - ```python -c 'import secrets; print(secrets.token_hex())'```
  - Adicione no campo DEBUG_MODE
    - True -  para o modo de produção
    - False -  para o modo de desenvolvimento
  - Adicione no campo API_KEY

- Execute o projeto.
  - ```python main.py```
- Rode o projeto em seu navegador.
  - Acesse em http://localhost:5000



#### Desenvolvido por [@JosueLopes](https://github.com/josuelopes512).
