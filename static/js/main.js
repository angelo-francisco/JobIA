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

function redirectTo(link) {
    window.location.href = link
}

document.addEventListener('DOMContentLoaded', function () {
    const exclusiveFeatures = document.querySelectorAll('.exclusive-feature');
    const closeModalButtons = document.querySelectorAll('.close-modal-btn');
    const upgradeModal = document.getElementById('upgradeModal');
    const curriculumModal = document.getElementById('curriculumModal');


    exclusiveFeatures.forEach(feature => {
        feature.addEventListener('click', function () {
            upgradeModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    });

    closeModalButtons.forEach(button => {
        button.addEventListener('click', function () {
            const modal = document.getElementById(button.dataset.modalId)
            modal.style.display = 'none';
        });
    });

    document.querySelector('#new-curriculum-btn')
        .addEventListener('click', () => {
            curriculumModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        })

});

