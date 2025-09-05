// //登出
function signinCheck() {
  fetch(userAPI)
    .then((res) => res.json())
    .then((data) => {
      if (data.data) {
        try{
          // console.log(data, "登入成功顯示圖表");
          document.getElementById("main").classList.remove("hide");
          document.getElementById("dateselector").classList.remove("hide");
          document.getElementById("strategyselector").classList.remove("hide");
          dropdownList();
        } catch (error) {
          console.log("Error processing sign-in check:", error);
          // Optionally, you can handle errors such as missing `data.data` here
        }
      // else {
      //   console.log("Signin Check Fail ... 登入失敗！");
      }
    });
}
// //進入頁面後先檢查使用者有沒有登入
// Call the signinCheck function after DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  signinCheck();
});


const signoutBtn = document.querySelector("#logOut");
function signout() {
  ``;
  fetch(userAPI, {
    method: "DELETE",
  }).then(() => {
    signinCheck();
    // Remove token and tokenExpiration from local storage
    localStorage.removeItem('token');
    localStorage.removeItem('tokenExpiration');

    // alert("Log Out Successfully");
    // Reset the flag to allow future signouts
    setTimeout(() => {
      // location.reload();
      window.location.href = '/'
    }, 300);
  });
  //         //頁面更新用

}
signoutBtn.addEventListener("click", signout);

