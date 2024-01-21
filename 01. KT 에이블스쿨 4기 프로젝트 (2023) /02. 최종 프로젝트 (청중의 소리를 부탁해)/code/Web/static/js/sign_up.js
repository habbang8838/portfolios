document.getElementById('checkUserIdButton').addEventListener('click', checkUserId);
document.getElementById('userid').addEventListener('input', validateUserId);
document.getElementById('password').addEventListener('input', validatePassword);
document.getElementById('password').addEventListener('input', validatePasswordConfirmation);
document.getElementById('confirmPassword').addEventListener('input', validatePasswordConfirmation);
document.getElementById('signupButton').addEventListener('click', validateUserIdBeforeSignup);
document.getElementById('signupButton').addEventListener('click', validateTermsBeforeSignup);

function checkUserId() {
    const userid = document.getElementById('userid').value;
    if (!userid) {
        alert('아이디를 입력해주세요.');
        return;
    }

    fetch(`/user/check_userid/?userid=${encodeURIComponent(userid)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('서버에서 응답이 없습니다. 다시 시도해주세요.');
            }
            return response.json();
        })
        .then(data => {
            if (data.is_taken) {
                alert('이미 사용 중인 아이디입니다.');
            } else {
                alert('사용 가능한 아이디입니다.');
                document.getElementById('userid').setAttribute('data-userid-valid', 'true');
            }
        })
        .catch(error => {
            alert(error.message);
        });
}


function validateUserId() {
    let userid = document.getElementsByName('userid')[0].value;
    let userIdError = document.getElementById('user_id_check');

    if (userid.length < 6 || userid.length > 15 || !/^[a-zA-Z0-9]+$/.test(userid)) {
        userIdError.innerHTML = '아이디는 6~15자리의 영문자와 숫자로 이루어져야 합니다.';
    } else {
        userIdError.innerHTML = '';
    }
}

function validatePassword() {
    let password = document.getElementsByName('password')[0].value;
    let passwordError = document.getElementById('password_check');
    let patterns = [/[0-9]/, /[a-z]/, /[A-Z]/, /[^0-9a-zA-Z]/];
    let count = patterns.reduce((acc, pattern) => acc + pattern.test(password), 0);

    if (password.length < 8) {
        passwordError.innerHTML = '비밀번호는 최소 8자 이상이어야 합니다.';
    } else if (count < 3) {
        passwordError.innerHTML = '비밀번호는 숫자, 소문자, 대문자, 특수 문자 중 최소 3가지를 포함해야 합니다.';
    } else {
        passwordError.innerHTML = '';
    }
}

function validatePasswordConfirmation() {
    let password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirmPassword').value;
    let passwordConfirmError = document.getElementById('password_confirm_check');

    if (confirmPassword !== password) {
        passwordConfirmError.textContent = '비밀번호가 일치하지 않습니다.';
    } else {
        passwordConfirmError.textContent = '';
    }
}

function validateUserIdBeforeSignup(event) {
    let useridValid = document.getElementById('userid').getAttribute('data-userid-valid');
    if (useridValid !== 'true') {
        let userIdError = document.getElementById('user_id_check');
        userIdError.innerHTML = '아이디 중복 확인을 해주세요.';
        event.preventDefault();
    }
}

const terms = {
    '1': {
        'modal': document.getElementById('terms1Modal'),
        'button': document.getElementById('terms1Button'),
        'checkbox': document.getElementById('terms1'),
        'confirm': document.getElementById('confirm1')
    },
    '2': {
        'modal': document.getElementById('terms2Modal'),
        'button': document.getElementById('terms2Button'),
        'checkbox': document.getElementById('terms2'),
        'confirm': document.getElementById('confirm2')
    }
};

for (const key in terms) {
    (function (key) {
        const term = terms[key];

        term.button.onclick = function () {
            term.modal.style.display = "block";
        };

        term.confirm.addEventListener('click', function () {
            term.checkbox.checked = true;
            term.modal.style.display = 'none';
        });
    })(key);
}

function validateTermsBeforeSignup() {
    for (const key in terms) {
        if (!terms[key].checkbox.checked) {
            alert('모든 약관에 동의해주셔야 회원가입이 가능합니다.');
            return false;
        }
    }
}
