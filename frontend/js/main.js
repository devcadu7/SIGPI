document.addEventListener('DOMContentLoaded', () => {
    const apiBase = '/api';
    const authForm = document.getElementById('authForm');
    const dashboardContainer = document.getElementById('dashboard-container');
    const dashboardMessage = document.getElementById('dashboardMessage');

    function showMessage(text, isError = false, target = null) {
        const element = target || document.getElementById('message') || dashboardMessage;
        if (!element) {
            alert(text);
            return;
        }
        element.textContent = text;
        element.className = 'message ' + (isError ? 'error-message show' : 'success-message show');
    }

    async function fetchJson(path, options = {}) {
        const response = await fetch(`${apiBase}/${path}`, options);
        const text = await response.text();
        let data;
        try {
            data = text ? JSON.parse(text) : {};
        } catch {
            throw new Error('Resposta inválida do servidor');
        }
        if (!response.ok) {
            const message = data.error || data.message || `Erro ${response.status}`;
            throw new Error(message);
        }
        return data;
    }

    function saveSession(user) {
        localStorage.setItem('sigpiUser', JSON.stringify(user));
    }

    function loadSession() {
        const raw = localStorage.getItem('sigpiUser');
        if (!raw) return null;
        try {
            return JSON.parse(raw);
        } catch {
            return null;
        }
    }

    function clearSession() {
        localStorage.removeItem('sigpiUser');
    }

    async function handleAuth(action) {
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const profileSelect = document.getElementById('profile');

        if (!usernameInput || !passwordInput || !profileSelect) {
            showMessage('Erro de carregamento do formulário.', true);
            return;
        }

        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();
        const profile = profileSelect.value;

        if (!username || !password) {
            showMessage('Preencha usuário e senha.', true);
            return;
        }

        try {
            const result = await fetchJson(`${action}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, profile })
            });
            showMessage(result.message || 'Operação concluída com sucesso.');
            if (action === 'login') {
                saveSession(result.user);
                window.location.href = getDashboardPath();
            }
        } catch (error) {
            showMessage(error.message, true);
        }
    }

    function getLoginPath() {
        return '/index.html';
    }

    function getDashboardPath() {
        return '/dashboard.html';
    }

    function isLoginPage() {
        return !!authForm;
    }

    function isDashboardPage() {
        return !!dashboardContainer;
    }

    async function loadUsers() {
        const users = await fetchJson('usuarios');
        return users;
    }

    async function loadProjects() {
        return await fetchJson('projetos');
    }

    async function loadEvaluations() {
        return await fetchJson('avaliacoes');
    }

    function normalizeUsers(users) {
        return {
            alunos: users.alunos || [],
            professores: users.professores || [],
            coordenacao: users.coordenacao || [],
            empresasParceiras: users.empresasParceiras || []
        };
    }

    function buildSummary(user, projects, evaluations, users) {
        const summaryGrid = document.getElementById('summaryGrid');
        if (!summaryGrid) return;
        const alunosCount = users.alunos.length;
        const professoresCount = users.professores.length;
        const projetosCount = projects.length;
        const avaliacoesCount = evaluations.length;
        summaryGrid.innerHTML = `
            <article class="summary-card">
                <h4>Usuário</h4>
                <p>${user.username}</p>
                <span>${user.profile}</span>
            </article>
            <article class="summary-card">
                <h4>Projetos</h4>
                <p>${projetosCount}</p>
                <span>Total de projetos cadastrados</span>
            </article>
            <article class="summary-card">
                <h4>Avaliações</h4>
                <p>${avaliacoesCount}</p>
                <span>Total de avaliações registradas</span>
            </article>
            <article class="summary-card">
                <h4>Alunos</h4>
                <p>${alunosCount}</p>
                <span>Alunos cadastrados</span>
            </article>
            <article class="summary-card">
                <h4>Professores</h4>
                <p>${professoresCount}</p>
                <span>Professores cadastrados</span>
            </article>
        `;
    }

    function buildProjectsTable(projects, users) {
        const section = document.getElementById('projectsSection');
        if (!section) return;

        const alunosMap = new Map((users.alunos || []).map((user) => [user.id, user.username]));
        section.innerHTML = `
            <table class="entity-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Título</th>
                        <th>Aluno</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    ${projects
                        .map(
                            (project) => `
                                <tr>
                                    <td>${project.id}</td>
                                    <td>${project.titulo}</td>
                                    <td>${alunosMap.get(project.alunoId) || 'Desconhecido'}</td>
                                    <td>${project.status}</td>
                                    <td class="table-actions">
                                        <button class="btn-secondary small" data-action="edit-project" data-id="${project.id}">Editar</button>
                                        <button class="btn-danger small" data-action="delete-project" data-id="${project.id}">Excluir</button>
                                    </td>
                                </tr>
                            `
                        )
                        .join('')}
                </tbody>
            </table>
        `;
    }

    function buildEvaluationsTable(evaluations, projects, users) {
        const section = document.getElementById('evaluationsSection');
        if (!section) return;

        const projectsMap = new Map((projects || []).map((project) => [project.id, project.titulo]));
        const professoresMap = new Map((users.professores || []).map((user) => [user.id, user.username]));
        section.innerHTML = `
            <table class="entity-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Projeto</th>
                        <th>Professor</th>
                        <th>Nota</th>
                        <th>Feedback</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    ${evaluations
                        .map(
                            (evaluation) => `
                                <tr>
                                    <td>${evaluation.id}</td>
                                    <td>${projectsMap.get(evaluation.projetoId) || 'Desconhecido'}</td>
                                    <td>${professoresMap.get(evaluation.professorId) || 'Desconhecido'}</td>
                                    <td>${evaluation.nota}</td>
                                    <td>${evaluation.feedback || '-'}</td>
                                    <td class="table-actions">
                                        <button class="btn-secondary small" data-action="edit-evaluation" data-id="${evaluation.id}">Editar</button>
                                        <button class="btn-danger small" data-action="delete-evaluation" data-id="${evaluation.id}">Excluir</button>
                                    </td>
                                </tr>
                            `
                        )
                        .join('')}
                </tbody>
            </table>
        `;
    }

    function populateSelect(select, options, selectedId) {
        if (!select) return;
        select.innerHTML = options
            .map((option) => `<option value="${option.value}"${option.value === selectedId ? ' selected' : ''}>${option.label}</option>`)
            .join('');
    }

    function setDashboardTitle(user) {
        const subtitle = document.getElementById('dashboardSubtitle');
        if (!subtitle) return;
        const profileLabel = {
            aluno: 'Aluno',
            professor: 'Professor',
            coordenacao: 'Coordenação',
            empresa: 'Empresa Parceira'
        }[user.profile] || 'Usuário';
        subtitle.textContent = `Perfil: ${profileLabel}`;
    }

    function resetProjectForm() {
        const form = document.getElementById('projectForm');
        if (!form) return;
        form.dataset.editing = '';
        document.getElementById('projectFormTitle').textContent = 'Cadastrar projeto';
        form.reset();
    }

    function resetEvaluationForm() {
        const form = document.getElementById('evaluationForm');
        if (!form) return;
        form.dataset.editing = '';
        document.getElementById('evaluationFormTitle').textContent = 'Cadastrar avaliação';
        form.reset();
    }

    function toggleFormVisibility(cardId, visible) {
        const card = document.getElementById(cardId);
        if (!card) return;
        card.style.display = visible ? 'block' : 'none';
    }

    async function refreshDashboard() {
        const user = loadSession();
        if (!user) {
            window.location.href = getLoginPath();
            return;
        }

        try {
            const users = normalizeUsers(await loadUsers());
            const projects = await loadProjects();
            const evaluations = await loadEvaluations();
            setDashboardTitle(user);
            buildSummary(user, projects, evaluations, users);
            buildProjectsTable(projects, users);
            buildEvaluationsTable(evaluations, projects, users);
            populateSelect(document.getElementById('projectAluno'), users.alunos.map((u) => ({ value: u.id, label: u.username })));
            populateSelect(document.getElementById('evaluationProject'), projects.map((p) => ({ value: p.id, label: p.titulo })));
            populateSelect(document.getElementById('evaluationProfessor'), users.professores.map((u) => ({ value: u.id, label: u.username })));
            attachTableListeners(projects, evaluations, users);
            resetProjectForm();
            resetEvaluationForm();
            toggleFormVisibility('projectFormCard', false);
            toggleFormVisibility('evaluationFormCard', false);
        } catch (error) {
            showMessage(error.message, true, dashboardMessage);
        }
    }

    function attachTableListeners(projects, evaluations, users) {
        const projectsSection = document.getElementById('projectsSection');
        const evaluationsSection = document.getElementById('evaluationsSection');

        if (projectsSection) {
            projectsSection.querySelectorAll('button[data-action]').forEach((button) => {
                const action = button.dataset.action;
                const id = button.dataset.id;
                button.addEventListener('click', async () => {
                    if (action === 'edit-project') {
                        const project = projects.find((item) => item.id === Number(id));
                        if (!project) return;
                        document.getElementById('projectTitle').value = project.titulo;
                        document.getElementById('projectAluno').value = project.alunoId;
                        document.getElementById('projectStatus').value = project.status;
                        document.getElementById('projectFormTitle').textContent = 'Editar projeto';
                        document.getElementById('projectForm').dataset.editing = project.id;
                        toggleFormVisibility('projectFormCard', true);
                    }
                    if (action === 'delete-project') {
                        if (!confirm('Deseja realmente excluir este projeto?')) return;
                        await removeProject(id);
                    }
                });
            });
        }

        if (evaluationsSection) {
            evaluationsSection.querySelectorAll('button[data-action]').forEach((button) => {
                const action = button.dataset.action;
                const id = button.dataset.id;
                button.addEventListener('click', async () => {
                    if (action === 'edit-evaluation') {
                        const evaluation = evaluations.find((item) => item.id === Number(id));
                        if (!evaluation) return;
                        document.getElementById('evaluationProject').value = evaluation.projetoId;
                        document.getElementById('evaluationProfessor').value = evaluation.professorId;
                        document.getElementById('evaluationGrade').value = evaluation.nota;
                        document.getElementById('evaluationFeedback').value = evaluation.feedback || '';
                        document.getElementById('evaluationFormTitle').textContent = 'Editar avaliação';
                        document.getElementById('evaluationForm').dataset.editing = evaluation.id;
                        toggleFormVisibility('evaluationFormCard', true);
                    }
                    if (action === 'delete-evaluation') {
                        if (!confirm('Deseja realmente excluir esta avaliação?')) return;
                        await removeEvaluation(id);
                    }
                });
            });
        }
    }

    async function createProject(projectData) {
        await fetchJson('projetos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(projectData)
        });
        await refreshDashboard();
        showMessage('Projeto salvo com sucesso.', false, dashboardMessage);
    }

    async function updateProject(projectId, projectData) {
        await fetchJson(`projetos/${projectId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(projectData)
        });
        await refreshDashboard();
        showMessage('Projeto atualizado com sucesso.', false, dashboardMessage);
    }

    async function removeProject(projectId) {
        await fetchJson(`projetos/${projectId}`, { method: 'DELETE' });
        await refreshDashboard();
        showMessage('Projeto excluído com sucesso.', false, dashboardMessage);
    }

    async function createEvaluation(evaluationData) {
        await fetchJson('avaliacoes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(evaluationData)
        });
        await refreshDashboard();
        showMessage('Avaliação salva com sucesso.', false, dashboardMessage);
    }

    async function updateEvaluation(evaluationId, evaluationData) {
        await fetchJson(`avaliacoes/${evaluationId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(evaluationData)
        });
        await refreshDashboard();
        showMessage('Avaliação atualizada com sucesso.', false, dashboardMessage);
    }

    async function removeEvaluation(evaluationId) {
        await fetchJson(`avaliacoes/${evaluationId}`, { method: 'DELETE' });
        await refreshDashboard();
        showMessage('Avaliação excluída com sucesso.', false, dashboardMessage);
    }

    async function initializeDashboard() {
        const currentUser = loadSession();
        if (!currentUser) {
            window.location.href = getLoginPath();
            return;
        }

        setDashboardTitle(currentUser);
        await refreshDashboard();

        document.getElementById('refreshBtn')?.addEventListener('click', refreshDashboard);
        document.getElementById('newProjectBtn')?.addEventListener('click', () => {
            resetProjectForm();
            toggleFormVisibility('projectFormCard', true);
        });
        document.getElementById('newEvaluationBtn')?.addEventListener('click', () => {
            resetEvaluationForm();
            toggleFormVisibility('evaluationFormCard', true);
        });

        document.getElementById('projectForm')?.addEventListener('submit', async (event) => {
            event.preventDefault();
            const form = event.target;
            const projectData = {
                titulo: document.getElementById('projectTitle').value.trim(),
                alunoId: Number(document.getElementById('projectAluno').value),
                status: document.getElementById('projectStatus').value
            };
            const editingId = form.dataset.editing;
            try {
                if (editingId) {
                    await updateProject(editingId, projectData);
                } else {
                    await createProject(projectData);
                }
                resetProjectForm();
                toggleFormVisibility('projectFormCard', false);
            } catch (error) {
                showMessage(error.message, true, dashboardMessage);
            }
        });

        document.getElementById('evaluationForm')?.addEventListener('submit', async (event) => {
            event.preventDefault();
            const form = event.target;
            const evaluationData = {
                projetoId: Number(document.getElementById('evaluationProject').value),
                professorId: Number(document.getElementById('evaluationProfessor').value),
                nota: Number(document.getElementById('evaluationGrade').value),
                feedback: document.getElementById('evaluationFeedback').value.trim()
            };
            const editingId = form.dataset.editing;
            try {
                if (editingId) {
                    await updateEvaluation(editingId, evaluationData);
                } else {
                    await createEvaluation(evaluationData);
                }
                resetEvaluationForm();
                toggleFormVisibility('evaluationFormCard', false);
            } catch (error) {
                showMessage(error.message, true, dashboardMessage);
            }
        });

        document.getElementById('projectFormCancel')?.addEventListener('click', () => {
            resetProjectForm();
            toggleFormVisibility('projectFormCard', false);
        });

        document.getElementById('evaluationFormCancel')?.addEventListener('click', () => {
            resetEvaluationForm();
            toggleFormVisibility('evaluationFormCard', false);
        });

        document.getElementById('logoutBtn')?.addEventListener('click', (event) => {
            event.preventDefault();
            clearSession();
            window.location.href = getLoginPath();
        });
    }

    if (isLoginPage()) {
        const currentUser = loadSession();
        if (currentUser) {
            window.location.href = getDashboardPath();
            return;
        }

        document.getElementById('authForm')?.addEventListener('submit', (event) => {
            event.preventDefault();
            handleAuth('login');
        });

        document.getElementById('registerButton')?.addEventListener('click', (event) => {
            event.preventDefault();
            handleAuth('register');
        });
    }

    if (isDashboardPage()) {
        initializeDashboard();
    }
});