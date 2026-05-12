import json
import os

USERS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.json'))

PROFILE_MAP = {
    'aluno': 'alunos',
    'professor': 'professores',
    'coordenacao': 'coordenacao',
    'empresa': 'empresasParceiras'
}


def load_users():
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

PROJECTS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'projetos.json'))
EVALUATIONS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'avaliacoes.json'))


def load_projects():
    with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_projects(projects):
    with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=4, ensure_ascii=False)


def load_evaluations():
    with open(EVALUATIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_evaluations(evaluations):
    with open(EVALUATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(evaluations, f, indent=4, ensure_ascii=False)


def profile_key(profile):
    if profile not in PROFILE_MAP:
        raise ValueError(f'Perfil inválido: {profile}')
    return PROFILE_MAP[profile]


def username_exists(users, username):
    for lista in users.values():
        if any(user.get('username') == username for user in lista):
            return True
    return False


def register_user(username, password, profile):
    users = load_users()

    if username_exists(users, username):
        raise ValueError('Usuário já existe.')

    key = profile_key(profile)
    profile_list = users[key]

    next_id = max(
        (user.get('id', 0) for item in users.values() for user in item),
        default=0
    ) + 1

    new_user = {
        'id': next_id,
        'username': username,
        'password': password
    }
    profile_list.append(new_user)
    save_users(users)
    return new_user


def authenticate_user(username, password, profile):
    users = load_users()
    key = profile_key(profile)
    profile_list = users.get(key, [])

    for user in profile_list:
        if user.get('username') == username and user.get('password') == password:
            return user
    return None
