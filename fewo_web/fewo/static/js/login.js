// Login form Enter key submission handler
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');
    const usernameInput = document.getElementById('id_username');
    const passwordInput = document.getElementById('id_password');

    if (form && usernameInput && passwordInput) {
        function handleEnterKey(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                form.submit();
            }
        }

        usernameInput.addEventListener('keydown', handleEnterKey);
        passwordInput.addEventListener('keydown', handleEnterKey);
    }
});
