const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');

registerLink.addEventListener('click', ()=>{
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', ()=>{
    wrapper.classList.remove('active');
});

const loginButton = document.querySelector('.login .btn');
const usernameInput = document.querySelector('.login input[name="username"]');
const accountInput = document.querySelector('.login input[name="account"]');
const passwordInput = document.querySelector('.login input[name="password"]');

loginButton.addEventListener('click', (event) => {
  event.preventDefault(); 

window.location.href = 'db.html';
});

