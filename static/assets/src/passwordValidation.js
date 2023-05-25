window.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password-input');
    const passwordError = document.getElementById('password-error');
    let errorMessage = "A senha precisa conter letras, números e símbolos."

    passwordInput.addEventListener('input', function () {
        const password = this.value;
        errorMessage = passwordValidation(password);

        if (errorMessage !== "A senha é válida.") {
            passwordError.textContent = errorMessage;
            passwordError.classList.remove('invisible');
            passwordError.classList.remove('text-green-400');
            passwordError.classList.add('text-red-600');
        } else {
            passwordError.textContent = errorMessage;
            passwordError.classList.remove('text-red-600');
            passwordError.classList.add('text-green-400');
        }

    });

    function passwordValidation(password) {
        // Verificar se a senha contém pelo menos um número
        if (!/[0-9]/.test(password)) {
            return "A senha precisa conter pelo menos um número.";
        }

        // Verificar se a senha contém pelo menos uma letra maiúscula
        if (!/[A-Z]/.test(password)) {
            return "A senha precisa conter pelo menos uma letra maiúscula.";
        }

        // Verificar se a senha contém pelo menos uma letra minúscula
        if (!/[a-z]/.test(password)) {
            return "A senha precisa conter pelo menos uma letra minúscula.";
        }

        // Verificar se a senha contém pelo menos um símbolo
        if (!/[^a-zA-Z0-9]/.test(password)) {
            return "A senha precisa conter pelo menos um símbolo.";
        }

        // A senha passou em todas as verificações
        return "A senha é válida.";
    }
});         