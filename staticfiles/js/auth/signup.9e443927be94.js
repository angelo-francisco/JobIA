const successIcon = `
  <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 200 100" style="vertical-align: middle;">
    <circle cx="50" cy="50" r="40" fill="#4CAF50" />
    <path d="M30 50 L45 65 L70 35" stroke="white" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round" />
  </svg>`;

const errorIcon = `
  <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 200 100" style="vertical-align: middle;">
    <circle cx="150" cy="50" r="40" fill="#F44336" />
    <path d="M130 30 L170 70 M170 30 L130 70" stroke="white" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round" />
  </svg>`;

function signupForm() {
    return {
        username: '',
        email: '',
        password: '',
        usernameValid: null,
        emailValid: null,
        usernameMessage: '',
        emailMessage: '',

        init() {
            this.usernameValid = null
            this.emailValid = null
        },

        async checkUsername() {
            this.usernameValid = null
            this.emailValid = null
            this.password = ''
            this.usernameMessage = ''
            
            try {
                const res = await fetch(`/auth/check-username/${this.username}/`)
                const data = await res.json()

                if (res.ok) {
                    this.usernameValid = true;
                    this.usernameMessage = `${successIcon}${data.msg}`;
                } else {
                    this.usernameValid = false;
                    this.usernameMessage = `${errorIcon}${data.msg}`;
                }

            } catch {
                this.usernameValid = false
                this.usernameMessage = "Erro na verificação."
            }
        },

        async checkEmail() {
            const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
            this.emailValid = pattern.test(this.email)

            try {
                if (!this.emailValid) {
                    this.emailValid = false;
                    this.emailMessage = `${errorIcon}Email inválido`;
                    return
                }
                const res = await fetch(`/auth/check-email/${this.email}/`)
                const data = await res.json()

                if (res.ok) {
                    this.emailValid = true;
                    this.emailMessage = `${successIcon}${data.msg}`;
                } else {
                    this.emailValid = false;
                    this.emailMessage = `${errorIcon}${data.msg}`;
                }

            } catch {
                console.warn("Campos zerados")
            }
        },
    }
}
