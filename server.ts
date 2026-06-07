import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Global In-Memory Persistent State representation (Ideal for proof-of-concept/preview live demoing)
interface Project {
    title: string;
    description: string;
    isHomologated: boolean;
    grade: string | null;
    feedback: string | null;
    evaluationDate: string | null;
    leaderName: string;
    companyDemandAssigned: string | null;
}

interface Submission {
    id: number;
    project: string;
    date: string;
    version: number;
    status: string;
    description: string;
}

interface StudentGrade {
    m1: number;
    m2: number;
    m3: number;
}

interface Student {
    ra: string;
    name: string;
    activeProject: string;
    grades: StudentGrade;
}

interface Company {
    name: string;
    cnpj: string;
    contactEmail: string;
    proposalDemand: string;
    isConvenioActive: boolean;
}

interface MentoredGroup {
    code: string;
    groupName: string;
    projectName: string;
    leader: string;
    membersCount: number;
    status: string;
    nextMeeting: string;
}

let currentUser = {
    role: 'aluno',
    name: 'Lucas Silva',
    email: 'lucas.aluno@sigpi.com'
};

const initialProjects: Project[] = [
    {
        title: "Sistema ERP Escolar",
        description: "Controle de vendas, estoque perecível e gestão de caixa para comércios locais de panificação.",
        isHomologated: true,
        grade: "9.5",
        feedback: "O projeto demonstra excelente maturidade arquitetural e usabilidade intuitiva para pequenos comércios de panificação e panificados.",
        evaluationDate: "12 de Outubro, 2026",
        leaderName: "Lucas Silva",
        companyDemandAssigned: "Automação de Controle de Validade em Panificados (Padaria Alfa)"
    },
    {
        title: "App de Saúde Mental",
        description: "Aplicação multiplataforma para monitoramento de rotinas diárias e meditação guiada.",
        isHomologated: false,
        grade: "8.8",
        feedback: "A metodologia de micro-hábitos está muito bem consolidada, porém necessita detalhar melhor a LGPD nos termos de uso.",
        evaluationDate: "01 de Junho, 2026",
        leaderName: "Mariana Costa",
        companyDemandAssigned: "Gestão Emocional nos Postos de saúde"
    },
    {
        title: "Rede Social Acadêmica",
        description: "Encontros de mentoria e compartilhamento de materiais de pesquisa acadêmica entre pós-graduandos.",
        isHomologated: true,
        grade: "7.6",
        feedback: "Escopo excelente, mas os índices de performance de rede nos testes de carga necessitam otimização de queries de persistência.",
        evaluationDate: "20 de Maio, 2026",
        leaderName: "Rodrigo Alencar",
        companyDemandAssigned: null
    }
];

const initialSubmissions: Submission[] = [
    {
        id: 1,
        project: "Sistema ERP Escolar",
        date: "12 de Outubro, 2026",
        version: 2,
        status: "Aprovado",
        description: "Ajuste na modelagem de estoque de perecíveis de panificação."
    },
    {
        id: 2,
        project: "App de Saúde Mental",
        date: "01 de Junho, 2026",
        version: 1,
        status: "Pendente",
        description: "Envio de diagramas UML de caso de uso e termos de consinto da LGPD."
    }
];

const initialStudents: Student[] = [
    {
        ra: "20240192",
        name: "Lucas Silva",
        activeProject: "Sistema ERP Escolar",
        grades: { m1: 9.0, m2: 9.5, m3: 10.0 }
    },
    {
        ra: "20240311",
        name: "Mariana Costa",
        activeProject: "App de Saúde Mental",
        grades: { m1: 8.5, m2: 8.0, m3: 9.0 }
    },
    {
        ra: "20240409",
        name: "Rodrigo Alencar",
        activeProject: "Rede Social Acadêmica",
        grades: { m1: 7.0, m2: 7.5, m3: 8.0 }
    }
];

const initialCompanies: Company[] = [
    {
        name: "Padaria Alfa Ltda",
        cnpj: "12.333.444/0001-90",
        contactEmail: "tecnologia@padariaalfa.com",
        proposalDemand: "Automação de Controle de Validade em Panificados - sistema que evite o desperdício de lotes frescos de pães.",
        isConvenioActive: true
    },
    {
        name: "Frigorífico Beta S/A",
        cnpj: "42.111.222/0001-11",
        contactEmail: "projetos@frigorificobeta.com.br",
        proposalDemand: "Monitoramento de temperatura estática de câmaras de congelamento em tempo real por IoT.",
        isConvenioActive: true
    }
];

const initialMentoredGroups: MentoredGroup[] = [
    {
        code: "PI-01",
        groupName: "Alpha Engineers",
        projectName: "Sistema ERP Escolar",
        leader: "Lucas Silva",
        membersCount: 4,
        status: "Em Progresso",
        nextMeeting: "14 Jun 2026 às 14:00"
    },
    {
        code: "PI-02",
        groupName: "Heal Minds",
        projectName: "App de Saúde Mental",
        leader: "Mariana Costa",
        membersCount: 3,
        status: "Em Progresso",
        nextMeeting: "16 Jun 2026 às 09:00"
    }
];

// Persistent variables pointers
let projects = [...initialProjects];
let submissions = [...initialSubmissions];
let students = [...initialStudents];
let companies = [...initialCompanies];
let mentoredGroups = [...initialMentoredGroups];

// API Endpoints
app.get('/api/data', (req, res) => {
    res.json({
        projects,
        submissions,
        students,
        companies,
        mentoredGroups,
        currentUser
    });
});

// Submit project delivery endpoint
app.post('/api/submit', (req, res) => {
    const { project, title, desc, linkedin, github, fileName } = req.body;
    
    // Add submission record
    const nextId = submissions.length + 1;
    const dateToday = new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' });
    
    const newSub: Submission = {
        id: nextId,
        project: project,
        date: dateToday,
        version: 1, // Start at version 1 for new filings
        status: "Pendente",
        description: desc
    };
    
    submissions.unshift(newSub);

    // If matches custom project title, update grades or parameters
    const targetProj = projects.find(p => p.title === project);
    if (targetProj) {
        targetProj.isHomologated = false; // Requires review
        targetProj.feedback = `Envio de Trabalho de entrega realizado: "${title}". Justificativa de submissão: "${desc}".`;
    } else {
        // Create matching temporary project
        projects.push({
            title: project,
            description: desc,
            isHomologated: false,
            grade: null,
            feedback: "Aguardando avaliação do orientador clínico.",
            evaluationDate: null,
            leaderName: currentUser.name,
            companyDemandAssigned: null
        });
    }

    res.json({ success: true });
});

// Update grades from class diary
app.post('/api/grade-update', (req, res) => {
    const { ra, m1, m2, m3 } = req.body;
    const student = students.find(s => s.ra === ra);
    if(student) {
        student.grades.m1 = parseFloat(m1) || 0;
        student.grades.m2 = parseFloat(m2) || 0;
        student.grades.m3 = parseFloat(m3) || 0;

        // Propagate average inside associated projects representation
        const targetProj = projects.find(p => p.title === student.activeProject);
        if(targetProj) {
            const finalMed = ((student.grades.m1 * 0.3) + (student.grades.m2 * 0.3) + (student.grades.m3 * 0.4)).toFixed(1);
            targetProj.grade = finalMed;
        }

        res.json({ success: true });
    } else {
        res.status(404).json({ success: false, message: 'Student selection failed' });
    }
});

// Coordinator Homologate Projects endpoint
app.post('/api/homologar', (req, res) => {
    const { title, status } = req.body;
    const proj = projects.find(p => p.title === title);
    if (proj) {
        proj.isHomologated = status;
        res.json({ success: true });
    } else {
        res.status(404).json({ success: false, message: 'Project not found' });
    }
});

// Add Partner Company or challenge demand
app.post('/api/empresa-add', (req, res) => {
    const { name, cnpj, contactEmail, proposalDemand } = req.body;
    
    const nextComp: Company = {
        name,
        cnpj,
        contactEmail,
        proposalDemand,
        isConvenioActive: true
    };
    
    companies.unshift(nextComp);
    res.json({ success: true });
});

// Edit Partner Company
app.post('/api/empresa-edit', (req, res) => {
    const { originalCnpj, name, cnpj, contactEmail, proposalDemand } = req.body;
    const index = companies.findIndex(c => c.cnpj === originalCnpj);
    if (index !== -1) {
        companies[index] = {
            ...companies[index],
            name,
            cnpj,
            contactEmail,
            proposalDemand
        };
        res.json({ success: true });
    } else {
        res.status(404).json({ success: false, message: 'Empresa não encontrada.' });
    }
});

// Delete Partner Company
app.post('/api/empresa-delete', (req, res) => {
    const { cnpj } = req.body;
    const index = companies.findIndex(c => c.cnpj === cnpj);
    if (index !== -1) {
        companies.splice(index, 1);
        res.json({ success: true });
    } else {
        res.status(404).json({ success: false, message: 'Empresa não encontrada.' });
    }
});

// Corporate feedback on solver project endpoint
app.post('/api/empresa-feedback', (req, res) => {
    const { title, grade, feedback } = req.body;
    const proj = projects.find(p => p.title === title);
    if (proj) {
        proj.grade = grade;
        proj.feedback = feedback;
        proj.evaluationDate = new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' });
        res.json({ success: true });
    } else {
        res.status(404).json({ success: false });
    }
});

// Login redirection logic
app.post('/api/auth/login', (req, res) => {
    const { role, email } = req.body;
    currentUser.role = role;
    currentUser.email = email;
    
    // Set human names for demo representation context
    if(role === 'aluno') currentUser.name = "Lucas Silva";
    else if(role === 'professor') currentUser.name = "Prof. Dr. Carlos Silva";
    else if(role === 'coordenacao') currentUser.name = "Coord. Dr. Ricardo Oliveira";
    else if(role === 'empresa') currentUser.name = "Padaria Alfa Ltda";

    // Direct url destination mapping
    let redirectUrl = '/aluno/dashboard/';
    if (role === 'professor') redirectUrl = '/professor/dashboard/';
    else if (role === 'coordenacao') redirectUrl = '/coordenacao/dashboard/';
    else if (role === 'empresa') redirectUrl = '/empresa/dashboard/';

    res.json({ success: true, redirectUrl });
});

// Native routing mapping static serving of files
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'login.html'));
});

app.get('/login/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'login.html'));
});

app.get('/logout/', (req, res) => {
    currentUser = { role: 'aluno', name: 'Lucas Silva', email: 'lucas.aluno@sigpi.com' };
    res.redirect('/');
});

// Student Views Routes
app.get('/aluno/dashboard/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'aluno', 'dashboard.html'));
});
app.get('/aluno/submissoes/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'aluno', 'submissoes.html'));
});
app.get('/aluno/historico/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'aluno', 'historico.html'));
});
app.get('/aluno/avaliacoes/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'aluno', 'avaliacoes.html'));
});
app.get('/aluno/feedback-alternativa/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'aluno', 'feedback_alternativa.html'));
});

// Professor Views Routes
app.get('/professor/dashboard/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'professor', 'dashboard.html'));
});
app.get('/professor/turmas/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'professor', 'turmas.html'));
});
app.get('/professor/notas/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'professor', 'notas.html'));
});
app.get('/professor/orientandos/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'professor', 'orientandos.html'));
});

// Coordination Views Routes
app.get('/coordenacao/dashboard/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'coordenacao', 'dashboard.html'));
});
app.get('/coordenacao/projetos/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'coordenacao', 'projetos.html'));
});
app.get('/coordenacao/empresas/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'coordenacao', 'empresas.html'));
});

// Corporate Partner Views Routes
app.get('/empresa/dashboard/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'empresa', 'dashboard.html'));
});
app.get('/empresa/demandas/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'empresa', 'demandas.html'));
});
app.get('/empresa/projetos/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'empresa', 'projetos.html'));
});

// Listen Connection
app.listen(PORT, '0.0.0.0', () => {
    console.log(`SIGPI full-stack Express server listening successfully on port ${PORT}`);
});
