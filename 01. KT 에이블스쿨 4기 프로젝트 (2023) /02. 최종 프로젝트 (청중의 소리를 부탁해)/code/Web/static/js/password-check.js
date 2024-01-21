document.getElementById('SignUpForm').addEventListener('submit', function(event) {
    var password = document.getElementById('password').value;
    var errorDiv = document.getElementById('passwordError');

    if (!validatePassword(password)) {
        errorDiv.textContent = '비밀번호는 숫자, 소문자, 대문자, 특수 문자 중 최소 3가지를 포함해야 합니다.';
        event.preventDefault();
    } else {
        errorDiv.textContent = '';
    }
});

function validatePassword(password) {
    var count = 0;
    if (/[A-Z]/.test(password)) count++;
    if (/[a-z]/.test(password)) count++;
    if (/[0-9]/.test(password)) count++;
    if (/[^A-Za-z0-9]/.test(password)) count++;

    return count >= 3 && password.length >= 8;
}
