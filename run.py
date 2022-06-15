from app import create_app
from livereload import Server

app = create_app()

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.serve(host='0.0.0.0', port=5000)
