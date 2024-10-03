
// 若api中有data=客戶資料API則顯示登出
// 若api中無data=NULL則顯示登入
fetch(`${window.origin}/api/user`)
  .then((res) => res.json())
  .then((data) => {
    if (data.data) {
      document.getElementById("logOut").classList.remove("hide");
      document.getElementById("member").classList.remove("hide");
      document.getElementById("data").classList.remove("hide");
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






// document.getElementById('headingDropdown').addEventListener('change', (event) => {
//   console.log(event)
// })
// // ======================================================================
// //選取欄位，登入以及註冊介面
// const signupForm = document.querySelector("#signUpForm");
// const signinForm = document.querySelector("#logInForm");
// const userAPI = `${window.origin}/api/user`;
// // ==========================================================================
// // 登入功能LOGIN
// const logInForm = document.getElementById("logInForm");
// logInForm.addEventListener("submit", (evt) => {
//   evt.preventDefault();

//   const logInEmail = document.getElementById("logInEmail");
//   const logInPassword = document.getElementById("logInPassword");

//   const email = logInEmail.value.trim();
//   const password = logInPassword.value.trim();

//   if (email === "" || password === "") {
//     if (email === "") {
//       emptyFieldReminder(logInEmail, "電子信箱欄位不得為空白");
//     }
//     if (password === "") {
//       emptyFieldReminder(logInPassword, "密碼欄位不得為空白");
//     }
//   } else {
//     const requestBody = JSON.stringify({
//       email: email,
//       password: password,
//       // SEND TO THE BACKEND
//     });

//     let responseStatus;

//     fetch(`${window.origin}/api/user`, {
//       method: "PATCH",
//       headers: new Headers({
//         "Content-Type": "application/json",

//       }),
//       body: requestBody,
      
//     })
//       .then((res) => {
//         responseStatus = res.status;
//         return res.json()

//       })
//       .then((data) => {
//         if (data.ok) {
//           hide(logIn);
//           alert("LogIn Successfully");
//           // LOCAL STORAGE
//           console.log(data)
//           // console.log(data.token,"---")
//           localStorage.setItem('token', data.token);
//           localStorage.setItem('tokenExpiration', data.expired);




//           // slideIn(logInSuccess);
//           // show(logInSuccess);
//           setTimeout(() => {
//             // location.reload();
//             window.location.href = '/'
//           }, 300);





//         } else if (data.error) {
//           logInMessage.classList.add("error");
//           logInMessage.textContent = "Please Check Account & Password";
//           //     error_type = data.message.split(':')[0];
//           //     showMessage(error_type, logInMessage);
//         } else if (data.error && responseStatus === 500) {
//           logInMessage.classList.add("error");
//           logInMessage.textContent = "Server Maintenance";
//         }
//       })
//       .catch((err) => {
//         console.log(`fetch error : ${err}`);
//       });
//   }
// });


// // =================================================================================
// // // 註冊
// const signUpForm = document.getElementById("signUpForm");
// signUpForm.addEventListener("submit", (evt) => {
//   evt.preventDefault();

//   const signUpName = document.getElementById("signUpName");
//   const signUpEmail = document.getElementById("signUpEmail");
//   const signUpPassword = document.getElementById("signUpPassword");

//   const name = signUpName.value.trim();
//   const email = signUpEmail.value.trim();
//   const password = signUpPassword.value.trim();

//   if (name === "" || email === "" || password === "") {
//     if (name === "") {
//       emptyFieldReminder(signUpName, "姓名欄位不得為空白");
//     }
//     if (email === "") {
//       emptyFieldReminder(signUpEmail, "電子信箱欄位不得為空白");
//     }
//     if (password === "") {
//       emptyFieldReminder(signUpPassword, "密碼欄位不得為空白");
//     }
//   } else {
//     const requestBody = JSON.stringify({
//       name: name,
//       email: email,
//       password: password,
//     });

//     let responseStatus;
//   //   alert("Registration Currently Closed")
//   // }})

//     fetch(`${window.origin}/api/user`, {
//       method: "POST",
//       headers: new Headers({
//         "Content-Type": "application/json",
//       }),
//       body: requestBody,
      
//     })
//       .then((res) => {
//         responseStatus = res.status
//         console.log(requestBody);
//         return res.json();
//       })
//       .then((data) => {
//         console.log(data,"成功!")
//         if (data.ok) {
//           signUpMessage.classList.add("success");
//           signUpMessage.textContent = "註冊成功";
//           const logInLink = document.getElementById("logInLink");
//           logInLink.textContent = "點此登入";
//         } else if (data.error) {
//           error_type = data.message.split(":")[0];
//           console.log(error_type, data.message);
//           signUpMessage.classList.add("error");
//           signUpMessage.textContent = "註冊失敗，該emil已使用";
//           // showMessage(error_type, signUpMessage);
//         } else if (data.error && responseStatus === 500) {
//           signUpMessage.classList.add("error");
//           signUpMessage.textContent = "很抱歉，伺服器出現錯誤";
//         }
//       })
//       .catch((err) => {
//         console.log(`fetch error : ${err}`);
//       });
//   }
// });


// for (let inputField of inputFields) {
//   inputField.addEventListener("focus", () => {
//     if (inputField.parentElement.classList.contains("error")) {
//       inputField.parentElement.classList.remove("error");
//     }
//   });
// }

// // ====================================================================================
// // //登出
// const signoutBtn = document.querySelector("#logOut");
// function signout() {
//   ``;
//   fetch(userAPI, {
//     method: "DELETE",
//   }).then(() => {
//     signinCheck();
//     // Remove token and tokenExpiration from local storage
//     localStorage.removeItem('token');
//     localStorage.removeItem('tokenExpiration');

//     // alert("Log Out Successfully");
//     // Reset the flag to allow future signouts
//     setTimeout(() => {
//       // location.reload();
//       window.location.href = '/'
//     }, 300);
//   });
//   //         //頁面更新用
//   try {
//     getUserData();
//   } catch (e) {}
//   try {
//     getBookingData();
//   } catch (e) {}
//   //         try{ fetchOrderAPI() }catch(e){}
// }
// signoutBtn.addEventListener("click", signout);






// const dropdownList = () => {
//   // Wait for 0.5 seconds before executing the code inside setTimeout
//   setTimeout(() => {
//     // Get the dropdown element
//     const dropdown = document.getElementById('headingDropdown');

//     // Fetch data from the API
//     fetch(`${window.origin}/api/user/strategy`)
//       .then(response => {
//         if (!response.ok) {
//           throw new Error('Network response was not ok');
//         }
//         return response.json();
//       })
//       .then(data => {
//         // Clear previous options
//         dropdown.innerHTML = '';

//         // Populate the dropdown with fetched data
//         data["dropdown_list"].forEach(strategy => {
//           const option = document.createElement('option');
//           option.textContent = strategy; // Assuming strategy object has a 'name' property
//           dropdown.appendChild(option);
//         });
//         // Trigger the dropdown change event after fetch is complete
//         dropdown.dispatchEvent(new Event('change'));
//       })
//       .catch(error => {
//         console.error('There was a problem with the fetch operation:', error);
//       });
//   }, 500); // 500 milliseconds = 0.5 seconds



// // Event listener for dropdown change event
// document.getElementById('headingDropdown').addEventListener('change', (event) => {
//     // Get the selected option text content
//     const selectedOptionText = event.target.selectedOptions[0].textContent;
//     // Generate a unique ID based on the selected option text content
//     const uniqueId = 'strategy';
//     // Set the unique ID to the selected option
//     event.target.selectedOptions[0].id = uniqueId;
//     const optionstag = event.target.options;
//     for (let i = 0; i < optionstag.length; i++) {
//         if (optionstag[i] !== event.target.selectedOptions[0]) {
//           optionstag[i].removeAttribute('id');
//         }}
//   });
// };



