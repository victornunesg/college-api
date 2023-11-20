# arquivo que serve apenas para inicializar a aplicação em Flask
from app import app

# inicia o app do Flask
if __name__ == '__main__':
    app.run(debug=True)
