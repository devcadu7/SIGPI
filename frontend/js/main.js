document.addEventListener('DOMContentLoaded', () => {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const profileSelect = document.getElementById('profile');
    const loginButton = document.getElementById('loginButton');
    const registerButton = document.getElementById('registerButton');
    const messageElement = document.getElementById('message');

    const apiBase = '/api';

    function showMessage(text, isError = false) {
        messageElement.textContent = text;
        messageElement.className = isError ? 'error-message' : 'success-message';
    }

    async function sendRequest(path, body) {
        try {
            const response = await fetch(`${apiBase}/${path}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            return await response.json();
        } catch (error) {
            showMessage('Erro de rede. Tente novamente.', true);
            return null;
        }
    }

    async function handleAuth(action) {
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();
        const profile = profileSelect.value;

        if (!username || !password) {
            showMessage('Preencha usuário e senha.', true);
            return;
        }

        const payload = { username, password, profile };
        const result = await sendRequest(action, payload);
        if (!result) return;

        if (result.error) {
            showMessage(result.error, true);
            return;
        }

        showMessage(result.message || 'Operação concluída com sucesso.');

        if (action === 'login' && result.success) {
            // Aqui você pode redirecionar para o dashboard correto
            // com base no tipo de usuário.
            console.log('Login realizado:', result.user);
        }
    }

    loginButton.addEventListener('click', (event) => {
        event.preventDefault();
        handleAuth('login');
    });

    registerButton.addEventListener('click', (event) => {
        event.preventDefault();
        handleAuth('register');
    });
});