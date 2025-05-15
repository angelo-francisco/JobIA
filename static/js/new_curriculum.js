document.addEventListener('DOMContentLoaded', function () {
    const startCard = document.getElementById('startCard');
    const startBtn = document.getElementById('startBtn');
    const modal = document.getElementById('curriculumModal');
    const backBtn = document.getElementById('backBtn');
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

    backBtn.addEventListener('click', function () {
        modal.style.display = 'none';
        startCard.style.display = 'flex';
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;

        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gerando...';

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

        const allData = {
            ...formEntries,
            ...dynamicFields,
            userId: curriculumRawData.userId,
            plan: curriculumRawData.plan
        };

        fetch('/curriculum/generate/', {
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
                if (data.success) {
                    modal.style.display = 'none';
                    startCard.style.display = 'flex';

                    const btnGroup = document.querySelector('.btn-group');
                    if (btnGroup) {
                        btnGroup.style.display = 'flex';
                        btnGroup.style.justifyContent = 'center';
                        btnGroup.style.alignItems = 'center';
                        btnGroup.style.flexDirection = 'column';
                        btnGroup.innerHTML = `
                <div class="success-checkmark">
                  <div class="check-icon">
                    <span class="icon-line line-tip"></span>
                    <span class="icon-line line-long"></span>
                    <div class="icon-circle"></div>
                    <div class="icon-fix"></div>
                  </div>
                </div>
                <span class="textloader">Currículo gerado com sucesso!</span>
                <a href="${data.download_url}" class="btn btn-primary mt-3" download>
                  <i class="fas fa-download"></i> Baixar Currículo
                </a>
                <a href="/dashboard/" class="btn btn-secondary mt-2">
                  <i class="fas fa-tachometer-alt"></i> Voltar ao Dashboard
                </a>
              `;
                    }
                } else {
                    throw new Error(data.message || 'Erro desconhecido');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;

                alert(`Erro: ${error.message}`);
            });
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