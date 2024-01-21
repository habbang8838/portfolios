document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("InputPassword").addEventListener('click', function () {
        var passwordInput = document.getElementById("password");
        var toggleIcon = this;
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            toggleIcon.classList.add("fa-eye-slash");
            toggleIcon.classList.remove("fa-eye");
        } else {
            passwordInput.type = "password";
            toggleIcon.classList.remove("fa-eye-slash");
            toggleIcon.classList.add("fa-eye");
        }
    });
    
    document.getElementById("InputConfirmPassword").addEventListener('click', function () {
        var confirmPasswordInput = document.getElementById("confirmPassword");
        var toggleIcon = this;
        if (confirmPasswordInput.type === "password") {
            confirmPasswordInput.type = "text";
            toggleIcon.classList.add("fa-eye-slash");
            toggleIcon.classList.remove("fa-eye");
        } else {
            confirmPasswordInput.type = "password";
            toggleIcon.classList.remove("fa-eye-slash");
            toggleIcon.classList.add("fa-eye");
        }
    });
});
