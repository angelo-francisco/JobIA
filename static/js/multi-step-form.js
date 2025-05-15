function initMultiStepForm() {
    const formSteps = document.querySelectorAll('.form-step');
    const progressSteps = document.querySelectorAll('.progress-step');
    let currentStep = 0;

    function showStep(index) {
        formSteps.forEach((step, i) => {
            step.classList.toggle('active', i === index);
            progressSteps[i].classList.toggle('active', i <= index);
        });
    }

    document.querySelectorAll('.btn-next').forEach(button => {
        button.addEventListener('click', () => {
            if (currentStep < formSteps.length - 1) {
                currentStep++;
                showStep(currentStep);
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });

    document.querySelectorAll('.btn-prev').forEach(button => {
        button.addEventListener('click', () => {
            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });

    showStep(currentStep);
}

function initAddAchievements() {
    document.querySelectorAll('.btn-add-achievement').forEach(addBtn => {
        addBtn.addEventListener('click', () => {
            const container = addBtn.closest('.form-group').querySelector('.achievement-container');
            const entries = container.querySelectorAll('.achievement-entry');
            const last = entries[entries.length - 1];
            const clone = last.cloneNode(true);

            const input = clone.querySelector('input');
            input.value = '';

            const removeBtn = clone.querySelector('.btn-remove-achievement');
            removeBtn.addEventListener('click', () => {
                if (container.querySelectorAll('.achievement-entry').length > 1) {
                    clone.remove();
                }
            });

            container.appendChild(clone);
        });
    });

    document.querySelectorAll('.btn-remove-achievement').forEach(removeBtn => {
        removeBtn.addEventListener('click', () => {
            const container = removeBtn.closest('.achievement-container');
            if (container.querySelectorAll('.achievement-entry').length > 1) {
                removeBtn.closest('.achievement-entry').remove();
            }
        });
    });
}

function initDynamicSections() {
    function setupDynamicSection({ buttonId, containerId, entryClass, allowRemove = true }) {
        const button = document.getElementById(buttonId);
        const container = document.getElementById(containerId);

        if (!button || !container) return;

        button.addEventListener('click', () => {
            const entries = container.getElementsByClassName(entryClass);
            const lastEntry = entries[entries.length - 1];
            const newEntry = lastEntry.cloneNode(true);
            const newIndex = entries.length + 1;

            const allInputs = newEntry.querySelectorAll('input, textarea, select, label');

            allInputs.forEach(el => {
                if (el.tagName === 'LABEL' && el.htmlFor) {
                    el.htmlFor = el.htmlFor.replace(/\d+$/, newIndex);
                }

                if (el.id) el.id = el.id.replace(/\d+$/, newIndex);
                if (el.name && el.name.includes('[]')) el.name = el.name.replace(/\[\]/g, '[]');
                if (['INPUT', 'TEXTAREA'].includes(el.tagName)) el.value = '';
            });

            if (allowRemove && !newEntry.querySelector('.btn-remove-entry')) {
                const removeBtn = document.createElement('button');
                removeBtn.type = 'button';
                removeBtn.className = 'btn btn-danger btn-remove-entry mt-2';
                removeBtn.innerHTML = '<i class="fas fa-trash"></i> Remover';
                removeBtn.addEventListener('click', () => {
                    if (container.getElementsByClassName(entryClass).length > 1) {
                        newEntry.remove();
                    }
                });
                newEntry.appendChild(removeBtn);
            }

            container.appendChild(newEntry);
        });

        if (allowRemove) {
            const entries = container.getElementsByClassName(entryClass);
            Array.from(entries).forEach(entry => {
                if (!entry.querySelector('.btn-remove-entry') && entries.length > 1) {
                    const removeBtn = document.createElement('button');
                    removeBtn.type = 'button';
                    removeBtn.className = 'btn btn-danger btn-remove-entry mt-2';
                    removeBtn.innerHTML = '<i class="fas fa-trash"></i> Remover';
                    removeBtn.addEventListener('click', () => {
                        if (container.getElementsByClassName(entryClass).length > 1) {
                            entry.remove();
                        }
                    });
                    entry.appendChild(removeBtn);
                }
            });
        }
    }

    setupDynamicSection({ buttonId: 'addExperience', containerId: 'experienceContainer', entryClass: 'experience-entry' });
    setupDynamicSection({ buttonId: 'addProfessionalExperience', containerId: 'professionalExperienceContainer', entryClass: 'professional-experience-entry' });
    setupDynamicSection({ buttonId: 'addExecExperience', containerId: 'executiveExperienceContainer', entryClass: 'executive-experience-entry' });
    setupDynamicSection({ buttonId: 'addEliteExperience', containerId: 'eliteExperienceContainer', entryClass: 'elite-experience-entry' });

    setupDynamicSection({ buttonId: 'addEducation', containerId: 'educationContainer', entryClass: 'education-entry' });
    setupDynamicSection({ buttonId: 'addEliteEducation', containerId: 'eliteEducationContainer', entryClass: 'elite-education-entry' });

    setupDynamicSection({ buttonId: 'addLanguage', containerId: 'languagesContainer', entryClass: 'language-entry' });
    setupDynamicSection({ buttonId: 'addEliteLanguage', containerId: 'eliteLanguagesContainer', entryClass: 'language-entry' });

    setupDynamicSection({ buttonId: 'addCertification', containerId: 'certificationsContainer', entryClass: 'certification-entry' });
    setupDynamicSection({ buttonId: 'addGlobalCertification', containerId: 'globalCertificationsContainer', entryClass: 'certification-entry' });
    setupDynamicSection({ buttonId: 'addAward', containerId: 'awardsContainer', entryClass: 'award-entry' });
    setupDynamicSection({ buttonId: 'addPhilanthropy', containerId: 'philanthropyContainer', entryClass: 'philanthropy-entry' });
    setupDynamicSection({ buttonId: 'addBoardMembership', containerId: 'boardMembershipsContainer', entryClass: 'board-entry' });
}
