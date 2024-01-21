const login_btn = document.querySelector("#login_btn");
login_btn.addEventListener("click", () => {
    const id = document.querySelector("#id");
    const pw = document.querySelector("#pw");
    if (id.value == "") {
        alert("아이디를 입력해 주세요.");
        id.focus();
        return false;
    }
    if (pw.value == "") {
        alert("비밀번호를 입력해 주세요.");
        pw.focus();
        return false;
    }
    const xhr = new XMLHttpRequest();
    // xhr.open("POST", "./login_ok.php", true);

    const login_form = document.querySelector("#login_form");
    const f = new FormData(login_form);

    xhr.send(f);

    xhr.onload = () => {
        console.log(xhr.status);
    }
});