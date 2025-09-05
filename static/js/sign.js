// 若api中有data=客戶資料API則顯示登出
// 若api中無data=NULL則顯示登入
fetch(`${window.origin}/api/user`)
  .then((res) => res.json())
  .then((data) => {
    if (data.data) {
      document.getElementById("logOut").classList.remove("hide");
      document.getElementById("memberonly").classList.add("hide")
    } else {
      document.getElementById("logInSignUp").classList.remove("hide");
    }
  })
  .catch((err) => {
    console.log(`==> fetch error : ${err}`);
  });


// ============ pop up modal ================
// 點取navigator的資料顯示
const logInSignUp = document.getElementById("logInSignUp");
// 點選會員訂單紀錄
const memberOrder = document.getElementById("member");

// 切換選單列表
const signUpLink = document.getElementById("signUpLink");
const logInLink = document.getElementById("logInLink");

// 得到選單列表
const logIn = document.getElementById("logIn");
const signUp = document.getElementById("signUp");

// 顯示登入訊息
const signUpMessage = document.getElementById("signUpMessage");
const logInMessage = document.getElementById("logInMessage");
const inputFields = document.querySelectorAll(".form-control input");

// =========================================================================

// 函數區
// 基礎功能:
// 提示字元消失，顯示登入介面，隱藏介面，顯示狀況，移除狀況
function clearMessage(element) {
  element.classList.remove("error");
  element.classList.remove("success");
  element.textContent = "";
}
function slideIn(element) {
  element.classList.add("slide-in");
}
function hide(element) {
  element.classList.remove("slide-in");
  element.classList.remove("show");
  // clear existed input
  const allInput = element.querySelectorAll("input");
  for (let input of allInput) {
    input.value = "";
  }
}
function show(element) {
  element.classList.add("show");
  document.body.addEventListener("click", (evt) => {
    if (
      !evt.target.closest("li#logInSignUp") &&
      !evt.target.closest("div.pop-up-modal")
    ) {
      hide(element);
      clearMessage(element.querySelector("span"));
    }
  });
}
//顯示小提醒
function emptyFieldReminder(inputField, message) {
  const formControl = inputField.parentElement;
  formControl.classList.add("error");
  const errorMessage = formControl.querySelector("small");
  errorMessage.textContent = message;
}

//去除小提醒
//
function removeEmptyFieldReminder() {
  for (let inputField of inputFields) {
    if (inputField.parentElement.classList.contains("error")) {
      inputField.parentElement.classList.remove("error");
    }
  }
}


// code part
// 以下事件處理，函數處理 
//點下顯示視窗
logInSignUp.addEventListener("click", (e) => {
  e.preventDefault;
  slideIn(logIn);
  show(logIn);
});

//點下切換註冊介面
signUpLink.addEventListener("click", () => {
  clearMessage(logInMessage);
  hide(logIn);
  removeEmptyFieldReminder();
  show(signUp);
});

//點下切換至登入介面
logInLink.addEventListener("click", () => {
  clearMessage(signUpMessage);
  hide(signUp);
  removeEmptyFieldReminder();
  show(logIn);
});
//關閉選單列表
const logInClose = document.getElementById("logInClose");
const signUpClose = document.getElementById("signUpClose");
logInClose.addEventListener("click", () => {
  hide(logIn);
});
signUpClose.addEventListener("click", () => {
  hide(signUp);
});




