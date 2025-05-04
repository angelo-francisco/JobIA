// Dashboard Panel Toggle
const dashboardToggle = document.getElementById('dashboardToggle');
const dashboardPanel = document.getElementById('dashboardPanel');
const closePanel = document.getElementById('closePanel');
const panelOverlay = document.getElementById('panelOverlay');

// Toggle dashboard panel
dashboardToggle.addEventListener('click', () => {
    dashboardPanel.classList.add('active');
    panelOverlay.classList.add('active');
    loadDashboardContent();
});

// Close panel
closePanel.addEventListener('click', closeDashboard);
panelOverlay.addEventListener('click', closeDashboard);

function closeDashboard() {
    dashboardPanel.classList.remove('active');
    panelOverlay.classList.remove('active');
}

const profileDropdown = document.querySelector('.profile-dropdown');
const profileBtn = document.querySelector('.profile-btn');

profileBtn.addEventListener('click', () => {
    profileDropdown.classList.toggle('active');
});

document.addEventListener('click', (e) => {
    if (!profileDropdown.contains(e.target)) {
        profileDropdown.classList.remove('active');
    }
});

function loadDashboardContent() {
    const dashboardContent = document.querySelector('.dashboard-content');
    dashboardContent.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
        </div>
    `;

    // Simulate API call
    setTimeout(() => {
        dashboardContent.innerHTML = `
            <div class="dashboard-grid">
                <div class="dashboard-card">
                    <div class="card-header">
                        <div class="card-title">Total de Usuários</div>
                        <div class="card-icon">
                            <i class="fas fa-users"></i>
                        </div>
                    </div>
                    <div class="card-value">1,254</div>
                    <div class="card-change positive">
                        <i class="fas fa-arrow-up"></i> 12.5% desde o último mês
                    </div>
                </div>
                
                <div class="dashboard-card">
                    <div class="card-header">
                        <div class="card-title">Novos Jobs</div>
                        <div class="card-icon">
                            <i class="fas fa-briefcase"></i>
                        </div>
                    </div>
                    <div class="card-value">86</div>
                    <div class="card-change positive">
                        <i class="arrow-up"></i> 8.2% desde o último mês
                    </div>
                </div>
                
                <div class="dashboard-chart">
                    <h3>Atividade Recente</h3>
                    <div class="chart-placeholder">
                        <p>Gráfico de atividades será exibido aqui</p>
                    </div>
                </div>
                
                <div class="dashboard-activity">
                    <h3>Últimas Interações</h3>
                    <div class="activity-list">
                        <div class="activity-item">
                            <div class="activity-icon">
                                <i class="fas fa-user-plus"></i>
                            </div>
                            <div class="activity-content">
                                <p>Novo usuário registrado: João Silva</p>
                                <small>Há 2 horas</small>
                            </div>
                        </div>
                        <div class="activity-item">
                            <div class="activity-icon">
                                <i class="fas fa-briefcase"></i>
                            </div>
                            <div class="activity-content">
                                <p>Novo job postado: Desenvolvedor Front-end</p>
                                <small>Há 4 horas</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }, 1000);
}

// Reactive data example
let dashboardData = {
    users: 1254,
    jobs: 86,
    activities: [
        { type: 'user', action: 'Novo usuário registrado: João Silva', time: 'Há 2 horas' },
        { type: 'job', action: 'Novo job postado: Desenvolvedor Front-end', time: 'Há 4 horas' }
    ]
};

function updateDashboardData(newData) {
    dashboardData = { ...dashboardData, ...newData };
    if (dashboardPanel.classList.contains('active')) {
        loadDashboardContent();
    }
}

setInterval(() => {
    const newUsers = dashboardData.users + Math.floor(Math.random() * 10);
    updateDashboardData({ users: newUsers });
}, 30000); 