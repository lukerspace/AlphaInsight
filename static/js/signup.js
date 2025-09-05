// // 註冊
const signUpForm = document.getElementById("signUpForm");
signUpForm.addEventListener("submit", (evt) => {
  evt.preventDefault();

  const signUpName = document.getElementById("signUpName");
  const signUpEmail = document.getElementById("signUpEmail");
  const signUpPassword = document.getElementById("signUpPassword");

  const name = signUpName.value.trim();
  const email = signUpEmail.value.trim();
  const password = signUpPassword.value.trim();

  if (name === "" || email === "" || password === "") {
    if (name === "") {
      emptyFieldReminder(signUpName, "姓名欄位不得為空白");
    }
    if (email === "") {
      emptyFieldReminder(signUpEmail, "電子信箱欄位不得為空白");
    }
    if (password === "") {
      emptyFieldReminder(signUpPassword, "密碼欄位不得為空白");
    }
  } else {
    const requestBody = JSON.stringify({
      name: name,
      email: email,
      password: password,
    });

    let responseStatus;
  //   alert("Registration Currently Closed")
  // }})

    fetch(`${window.origin}/api/user`, {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      body: requestBody,
      
    })
      .then((res) => {
        responseStatus = res.status
        return res.json();
      })
      .then((data) => {
        console.log(data,"成功!")

        const parsedBody = JSON.parse(requestBody);

        if (data.ok && parsedBody.email.includes('@admin')) {
          signUpMessage.classList.add("success");
          signUpMessage.textContent = "Success";
          const logInLink = document.getElementById("logInLink");
          logInLink.textContent = "Click to LogIn";
        } else if (data.error) {
          error_type = data.message.split(":")[0];
          console.log(error_type, data.message);
          signUpMessage.classList.add("error");
          signUpMessage.textContent = "Invalid Email";
          // showMessage(error_type, signUpMessage);
        } else if (data.error && responseStatus === 500) {
          signUpMessage.classList.add("error");
          signUpMessage.textContent = "Internal Error";
        } else  {
          signUpMessage.classList.add("error");
          signUpMessage.textContent = "acct: test@admin / pw: 0000 ";
        }
      })
      .catch((err) => {
        console.log(`fetch error : ${err}`);
      });
  }
});



