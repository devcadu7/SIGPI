import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

from auth import authenticate_user, register_user, load_users


class RequestHandler(SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        return json.loads(body.decode('utf-8'))

    def do_GET(self):
        if self.path == '/api/usuarios':
            users = load_users()
            self.send_json(users)
            return
        return super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/api/register':
            self.handle_register()
            return
        if parsed_path.path == '/api/login':
            self.handle_login()
            return
        self.send_error(404, 'Rota não encontrada')

    def handle_register(self):
        try:
            payload = self.read_json()
            username = payload.get('username', '').strip()
            password = payload.get('password', '').strip()
            profile = payload.get('profile', '').strip()

            if not username or not password or not profile:
                self.send_json({'error': 'Preencha todos os campos.'}, 400)
                return

            user = register_user(username, password, profile)
            self.send_json({
                'success': True,
                'message': 'Cadastro realizado com sucesso.',
                'user': user
            })
        except ValueError as error:
            self.send_json({'error': str(error)}, 400)
        except Exception as error:
            self.send_json({'error': 'Erro interno no servidor.'}, 500)

    def handle_login(self):
        try:
            payload = self.read_json()
            username = payload.get('username', '').strip()
            password = payload.get('password', '').strip()
            profile = payload.get('profile', '').strip()

            if not username or not password or not profile:
                self.send_json({'error': 'Preencha todos os campos.'}, 400)
                return

            user = authenticate_user(username, password, profile)
            if user is None:
                self.send_json({'error': 'Usuário ou senha inválidos.'}, 401)
                return

            self.send_json({
                'success': True,
                'message': 'Login realizado com sucesso.',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'profile': profile
                }
            })
        except Exception:
            self.send_json({'error': 'Erro interno no servidor.'}, 500)


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(base_dir)
    port = 8000
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print(f'Servindo em http://localhost:{port}')
    server.serve_forever()
