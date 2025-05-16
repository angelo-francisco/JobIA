

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
                    const newFor = el.htmlFor.replace(/\d*$/, '') + newIndex;
                    el.htmlFor = newFor;
                }

                if (el.id) {
                    const newId = el.id.replace(/\d*$/, '') + newIndex;
                    el.id = newId;
                }

                if (['INPUT', 'TEXTAREA'].includes(el.tagName)) {
                    el.value = '';
                    el.removeAttribute('aria-invalid');
                }

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

function initAddAchievements() {
    document.querySelectorAll('.btn-add-achievement').forEach(addBtn => {
        addBtn.addEventListener('click', () => {
            const container = addBtn.closest('.form-group').querySelector('.achievement-container');
            const entries = container.querySelectorAll('.achievement-entry');
            const last = entries[entries.length - 1];
            const clone = last.cloneNode(true);

            const input = clone.querySelector('input');
            input.value = '';

            // Garante que o botão de remover funcione
            const removeBtn = clone.querySelector('.btn-remove-achievement');
            removeBtn.addEventListener('click', () => {
                if (container.querySelectorAll('.achievement-entry').length > 1) {
                    clone.remove();
                }
            });

            container.appendChild(clone);
        });
    });

    // Ativa os botões de remover já existentes
    document.querySelectorAll('.btn-remove-achievement').forEach(removeBtn => {
        removeBtn.addEventListener('click', () => {
            const container = removeBtn.closest('.achievement-container');
            if (container.querySelectorAll('.achievement-entry').length > 1) {
                removeBtn.closest('.achievement-entry').remove();
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const startCard = document.getElementById('startCard');
    const startBtn = document.getElementById('startBtn');
    const modal = document.getElementById('curriculumModal');
    const form = document.getElementById('curriculumForm');

    if (typeof initMultiStepForm === 'function') {
        initMultiStepForm();
    }

    if (typeof initCurriculumForm === 'function') {
        initCurriculumForm(planName);
    }

    initDynamicSections()
    initAddAchievements()

    startBtn.addEventListener('click', function () {
        startCard.style.display = 'none';
        modal.style.display = 'flex';

        modal.scrollTo(0, 0);
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;

        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gerando...';

        const currentStep = document.querySelector('.form-step.active');

        const invalidVisible = [...currentStep.querySelectorAll(':invalid')].find(el => {
            return el.offsetParent !== null;
        });

        if (invalidVisible) {
            e.preventDefault();
            invalidVisible.scrollIntoView({ behavior: 'smooth', block: 'center' });
            invalidVisible.focus();
            return;
        }

        const formData = new FormData(form);
        const formEntries = Object.fromEntries(formData.entries());

        const dynamicFields = {};
        document.querySelectorAll('[name$="[]"]').forEach(input => {
            const fieldName = input.name.replace('[]', '');
            if (!dynamicFields[fieldName]) {
                dynamicFields[fieldName] = [];
            }
            if (input.value) {
                dynamicFields[fieldName].push(input.value);
            }
        });

        const questions = [];

        for (const [key, value] of Object.entries(formEntries)) {
            if (value.trim()) {
                questions.push({
                    question: key,
                    answer: value
                });
            }
        }

        for (const [key, values] of Object.entries(dynamicFields)) {
            values.forEach(value => {
                questions.push({
                    question: key,
                    answer: value
                });
            });
        }

        const allData = {
            questions: questions,
            userId: curriculumRawData.userId,
            plan: curriculumRawData.plan
        };

        let slug = ''

        fetch('/curriculum/get-form-data/', {
            method: 'POST',
            body: JSON.stringify(allData),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrft_token
            }
        }).then(response => {
            if (!response.ok) {
                throw new Error('Falha ao enviar formulário');
            }
            return response.json();
        }).then(data => {
            slug = data.slug

            fetch('/curriculum/generate/' + slug + '/', {
                method: 'POST',
                body: JSON.stringify(allData),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrft_token
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Falha ao enviar formulário');
                    }
                    return response.json();
                })
                .then(data => {
                    modal.style.display = 'none';
                    startCard.style.display = 'flex';

                    const btnGroup = document.querySelector('.btn-group');
                    if (btnGroup) {
                        btnGroup.style.display = 'flex';
                        btnGroup.style.justifyContent = 'center';
                        btnGroup.style.alignItems = 'center';
                        btnGroup.style.flexDirection = 'column';
                        btnGroup.innerHTML = `
                            <input type="text" id="curriculumNameInput" class="name-input" placeholder="Digite o nome do currículo">
                            <button id="saveCurriculumNameBtn" class="btn btn-primary mt-2">
                                <i class="fas fa-save"></i> Salvar Nome
                            </button>
                            <span class="textloader">Currículo gerado com sucesso!</span>
                            <a href="/dashboard/" class="btn btn-secondary mt-2" style="text-decoration: none;">
                                <i class="fas fa-tachometer-alt"></i> Voltar ao Dashboard
                            </a>
                        `;

                        document.getElementById('saveCurriculumNameBtn').addEventListener('click', () => {
                            const input = document.getElementById('curriculumNameInput');
                            const newName = input.value.trim();

                            if (!newName) {
                                alert('Por favor, digite um nome para o currículo.');
                                return;
                            }

                            fetch(`/curriculum/generate/${slug}/?rename=${encodeURI(newName)}`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': csrft_token,
                                },
                            })
                                .then(response => {
                                    if (!response.ok) throw new Error('Erro ao salvar o nome');
                                    return response.json();
                                })
                                .then(data => {
                                    window.location.href = "/dashboard/"
                                })
                                .catch(error => {
                                    console.error(error);
                                    alert('Erro ao salvar nome do currículo.');
                                });
                        });

                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;

                    alert(`Erro: ${error.message}, tente novamente mais tarde.`);
                });
        })

    });

    const expertiseInput = document.getElementById('expertiseInput');
    const expertiseTags = document.getElementById('expertiseTags');

    if (expertiseInput && expertiseTags) {
        expertiseInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter' && this.value.trim()) {
                e.preventDefault();

                const tag = document.createElement('div');
                tag.className = 'expertise-tag';
                tag.innerHTML = `
              ${this.value.trim()}
              <input type="hidden" name="expertiseTags[]" value="${this.value.trim()}">
              <span class="remove-tag">&times;</span>
            `;

                expertiseTags.appendChild(tag);
                this.value = '';

                tag.querySelector('.remove-tag').addEventListener('click', function () {
                    tag.remove();
                });
            }
        });
    }
});