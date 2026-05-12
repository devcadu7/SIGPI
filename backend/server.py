import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

from auth import (
    authenticate_user,
    register_user,
    load_users,
    load_projects,
    save_projects,
    load_evaluations,
    save_evaluations
)


class RequestHandler(SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_error(self, code, message=None, explain=None):
        self.send_response(code, message)
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().send_error(code, message, explain)

    def read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        return json.loads(body.decode('utf-8'))

    def normalize_frontend_path(self):
        if self.path.startswith('/frontend/'):
            self.path = self.path[len('/frontend'):]
        if self.path == '':
            self.path = '/'

    def do_HEAD(self):
        self.normalize_frontend_path()
        return super().do_HEAD()

    def do_GET(self):
        self.normalize_frontend_path()
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        segments = path.strip('/').split('/')

        if path == '/api/usuarios':
            users = load_users()
            self.send_json(users)
            return

        if path == '/api/projetos':
            self.handle_get_projects()
            return

        if path == '/api/avaliacoes':
            self.handle_get_evaluations()
            return

        if len(segments) == 3 and segments[0] == 'api' and segments[1] == 'projetos':
            self.handle_get_project(segments[2])
            return

        if len(segments) == 3 and segments[0] == 'api' and segments[1] == 'avaliacoes':
            self.handle_get_evaluation(segments[2])
            return

        return super().do_GET()

    def do_POST(self):
        self.normalize_frontend_path()
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/api/register':
            self.handle_register()
            return
        if parsed_path.path == '/api/login':
            self.handle_login()
            return
        if parsed_path.path == '/api/projetos':
            self.handle_create_project()
            return
        if parsed_path.path == '/api/avaliacoes':
            self.handle_create_evaluation()
            return
        self.send_error(404, 'Rota não encontrada')

    def do_PUT(self):
        self.normalize_frontend_path()
        parsed_path = urlparse(self.path)
        segments = parsed_path.path.strip('/').split('/')

        if len(segments) == 3 and segments[0] == 'api' and segments[1] == 'projetos':
            self.handle_update_project(segments[2])
            return

        if len(segments) == 3 and segments[0] == 'api' and segments[1] == 'avaliacoes':
            self.handle_update_evaluation(segments[2])
            return

        self.send_error(404, 'Rota não encontrada')

    def do_DELETE(self):
        self.normalize_frontend_path()
        parsed_path = urlparse(self.path)
        segments = parsed_path.path.strip('/').split('/')

        if len(segments) == 3 and segments[0] == 'api' and segments[1] == 'projetos':
            self.handle_delete_project(segments[2])
            return

        if len(segments) == 3 and segments[0] == 'api' and segments[1] == 'avaliacoes':
            self.handle_delete_evaluation(segments[2])
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

    def handle_get_projects(self):
        projects = load_projects()
        self.send_json(projects)

    def handle_get_project(self, project_id):
        try:
            project_id = int(project_id)
        except ValueError:
            self.send_json({'error': 'ID de projeto inválido.'}, 400)
            return

        projects = load_projects()
        project = next((proj for proj in projects if proj.get('id') == project_id), None)
        if project is None:
            self.send_json({'error': 'Projeto não encontrado.'}, 404)
            return

        self.send_json(project)

    def handle_create_project(self):
        try:
            payload = self.read_json()
            titulo = payload.get('titulo', '').strip()
            alunoId = payload.get('alunoId')
            status = payload.get('status', '').strip() or 'Pendente'

            if not titulo or not alunoId:
                self.send_json({'error': 'Título e aluno são obrigatórios.'}, 400)
                return

            projects = load_projects()
            next_id = max((proj.get('id', 0) for proj in projects), default=0) + 1
            new_project = {
                'id': next_id,
                'titulo': titulo,
                'alunoId': int(alunoId),
                'status': status
            }
            projects.append(new_project)
            save_projects(projects)
            self.send_json({'success': True, 'project': new_project}, 201)
        except Exception:
            self.send_json({'error': 'Erro ao criar projeto.'}, 500)

    def handle_update_project(self, project_id):
        try:
            project_id = int(project_id)
        except ValueError:
            self.send_json({'error': 'ID de projeto inválido.'}, 400)
            return

        try:
            payload = self.read_json()
            titulo = payload.get('titulo', '').strip()
            alunoId = payload.get('alunoId')
            status = payload.get('status', '').strip()

            projects = load_projects()
            project = next((proj for proj in projects if proj.get('id') == project_id), None)
            if project is None:
                self.send_json({'error': 'Projeto não encontrado.'}, 404)
                return

            if titulo:
                project['titulo'] = titulo
            if alunoId is not None:
                project['alunoId'] = int(alunoId)
            if status:
                project['status'] = status

            save_projects(projects)
            self.send_json({'success': True, 'project': project})
        except Exception:
            self.send_json({'error': 'Erro ao atualizar projeto.'}, 500)

    def handle_delete_project(self, project_id):
        try:
            project_id = int(project_id)
        except ValueError:
            self.send_json({'error': 'ID de projeto inválido.'}, 400)
            return

        projects = load_projects()
        new_projects = [proj for proj in projects if proj.get('id') != project_id]
        if len(new_projects) == len(projects):
            self.send_json({'error': 'Projeto não encontrado.'}, 404)
            return

        save_projects(new_projects)
        self.send_json({'success': True, 'message': 'Projeto excluído com sucesso.'})

    def handle_get_evaluations(self):
        evaluations = load_evaluations()
        self.send_json(evaluations)

    def handle_get_evaluation(self, evaluation_id):
        try:
            evaluation_id = int(evaluation_id)
        except ValueError:
            self.send_json({'error': 'ID de avaliação inválido.'}, 400)
            return

        evaluations = load_evaluations()
        evaluation = next((eval_ for eval_ in evaluations if eval_.get('id') == evaluation_id), None)
        if evaluation is None:
            self.send_json({'error': 'Avaliação não encontrada.'}, 404)
            return

        self.send_json(evaluation)

    def handle_create_evaluation(self):
        try:
            payload = self.read_json()
            projetoId = payload.get('projetoId')
            professorId = payload.get('professorId')
            nota = payload.get('nota')
            feedback = payload.get('feedback', '').strip()

            if not projetoId or not professorId or nota is None:
                self.send_json({'error': 'Projeto, professor e nota são obrigatórios.'}, 400)
                return

            evaluations = load_evaluations()
            next_id = max((eval_.get('id', 0) for eval_ in evaluations), default=0) + 1
            new_evaluation = {
                'id': next_id,
                'projetoId': int(projetoId),
                'professorId': int(professorId),
                'nota': float(nota),
                'feedback': feedback
            }
            evaluations.append(new_evaluation)
            save_evaluations(evaluations)
            self.send_json({'success': True, 'evaluation': new_evaluation}, 201)
        except Exception:
            self.send_json({'error': 'Erro ao criar avaliação.'}, 500)

    def handle_update_evaluation(self, evaluation_id):
        try:
            evaluation_id = int(evaluation_id)
        except ValueError:
            self.send_json({'error': 'ID de avaliação inválido.'}, 400)
            return

        try:
            payload = self.read_json()
            projetoId = payload.get('projetoId')
            professorId = payload.get('professorId')
            nota = payload.get('nota')
            feedback = payload.get('feedback', '').strip()

            evaluations = load_evaluations()
            evaluation = next((eval_ for eval_ in evaluations if eval_.get('id') == evaluation_id), None)
            if evaluation is None:
                self.send_json({'error': 'Avaliação não encontrada.'}, 404)
                return

            if projetoId is not None:
                evaluation['projetoId'] = int(projetoId)
            if professorId is not None:
                evaluation['professorId'] = int(professorId)
            if nota is not None:
                evaluation['nota'] = float(nota)
            if feedback:
                evaluation['feedback'] = feedback

            save_evaluations(evaluations)
            self.send_json({'success': True, 'evaluation': evaluation})
        except Exception:
            self.send_json({'error': 'Erro ao atualizar avaliação.'}, 500)

    def handle_delete_evaluation(self, evaluation_id):
        try:
            evaluation_id = int(evaluation_id)
        except ValueError:
            self.send_json({'error': 'ID de avaliação inválido.'}, 400)
            return

        evaluations = load_evaluations()
        new_evaluations = [eval_ for eval_ in evaluations if eval_.get('id') != evaluation_id]
        if len(new_evaluations) == len(evaluations):
            self.send_json({'error': 'Avaliação não encontrada.'}, 404)
            return

        save_evaluations(new_evaluations)
        self.send_json({'success': True, 'message': 'Avaliação excluída com sucesso.'})


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    os.chdir(base_dir)
    port = 8000
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print(f'Servindo em http://localhost:{port}')
    server.serve_forever()
