document.getElementById('SignUpForm').addEventListener('submit', function(event) {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;
    var errorDiv = document.getElementById('passwordConfirmError');

    if (password !== confirmPassword) {
        errorDiv.textContent = '비밀번호가 일치하지 않습니다.';
        event.preventDefault();
    } else {
        errorDiv.textContent = '';
    }
});
