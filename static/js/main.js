const dashboardToggle = document.getElementById('dashboardToggle');
const dashboardPanel = document.getElementById('dashboardPanel');
const closePanel = document.getElementById('closePanel');
const panelOverlay = document.getElementById('panelOverlay');

dashboardToggle.addEventListener('click', () => {
    dashboardPanel.classList.add('active');
    panelOverlay.classList.add('active');
});

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

document.addEventListener('DOMContentLoaded', function () {
    // Modal de recursos exclusivos
    const exclusiveFeatures = document.querySelectorAll('.exclusive-feature');
    const exclusiveModal = document.getElementById('exclusiveModal');
    const featureNameElement = document.getElementById('featureName');
    const closeModalButtons = document.querySelectorAll('.close-modal');

    exclusiveFeatures.forEach(feature => {
        feature.addEventListener('click', function () {
            const featureName = this.getAttribute('data-feature');
            featureNameElement.textContent = featureName;
            exclusiveModal.classList.add('active');
        });
    });

    closeModalButtons.forEach(button => {
        button.addEventListener('click', function () {
            exclusiveModal.classList.remove('active');
        });
    });

    document.getElementById('upgradePlan').addEventListener('click', function () {
        // Redirecionar para página de planos
        window.location.href = '#planos'; // Substitua pelo link real
    });

    // Fechar modal ao clicar fora
    exclusiveModal.addEventListener('click', function (e) {
        if (e.target === this) {
            this.classList.remove('active');
        }
    });
});