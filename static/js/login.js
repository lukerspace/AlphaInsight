//選取欄位，登入以及註冊介面
const signupForm = document.querySelector("#signUpForm");
const signinForm = document.querySelector("#logInForm");
const userAPI = `${window.origin}/api/user`;
// ==========================================================================
// 登入功能LOGIN
const logInForm = document.getElementById("logInForm");
logInForm.addEventListener("submit", (evt) => {
  evt.preventDefault();

  const logInEmail = document.getElementById("logInEmail");
  const logInPassword = document.getElementById("logInPassword");

  const email = logInEmail.value.trim();
  const password = logInPassword.value.trim();

  if (email === "" || password === "") {
    if (email === "") {
      emptyFieldReminder(logInEmail, "電子信箱欄位不得為空白");
    }
    if (password === "") {
      emptyFieldReminder(logInPassword, "密碼欄位不得為空白");
    }
  } else {
    const requestBody = JSON.stringify({
      email: email,
      password: password,
      // SEND TO THE BACKEND
    });

    let responseStatus;

    fetch(`${window.origin}/api/user`, {
      method: "PATCH",
      headers: new Headers({
        "Content-Type": "application/json",

      }),
      body: requestBody,
      
    })
      .then((res) => {
        responseStatus = res.status;
        return res.json()

      })
      .then((data) => {
        if (data.ok) {
          hide(logIn);
          alert("LogIn Successfully");
          // LOCAL STORAGE
          console.log(data)
          // console.log(data.token,"---")
          localStorage.setItem('token', data.token);
          localStorage.setItem('tokenExpiration', data.expired);




          // slideIn(logInSuccess);
          // show(logInSuccess);
          setTimeout(() => {
            // location.reload();
            window.location.href = '/'
          }, 300);





        } else if (data.error) {
          logInMessage.classList.add("error");
          logInMessage.textContent = "Please Check Account & Password";
          //     error_type = data.message.split(':')[0];
          //     showMessage(error_type, logInMessage);
        } else if (data.error && responseStatus === 500) {
          logInMessage.classList.add("error");
          logInMessage.textContent = "Server Maintenance";
        }
      })
      .catch((err) => {
        console.log(`fetch error : ${err}`);
      });
  }
});

