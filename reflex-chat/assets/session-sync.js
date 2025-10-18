// Session sync helper for Breogan
(function(){
  function isAuthPath(path){
    return path === '/login' || path === '/register';
  }

  // On page load, enforce route guard: if not authenticated and not on /login or /register, redirect to /login
  if(!sessionStorage.getItem('breogan_user') && !isAuthPath(window.location.pathname)){
    window.location.href = '/login';
  }

  // If authenticated and on /login, go to root
  if(sessionStorage.getItem('breogan_user') && window.location.pathname === '/login'){
    window.location.href = '/';
  }

  // Attach login interception if login form exists
  var loginForm = document.getElementById('login-form');
  if(loginForm){
    loginForm.addEventListener('submit', function(e){
      var u = this.querySelector('input[name="username"]').value;
      var p = this.querySelector('input[name="password"]').value;
      // Hardcoded admin/admin
      if(u === 'admin' && p === 'admin'){
        // Persist session
        sessionStorage.setItem('breogan_user', u);
        // Let the form submit to server first, then redirect
        setTimeout(function(){
          window.location.href = '/';
        }, 100);
        return true;
      }else{
        e.preventDefault();
        alert('Credenciales inválidas. Usa admin / admin');
        return false;
      }
    });
  }

  // Attach register interception to store user
  var regForm = document.getElementById('register-form');
  if(regForm){
    regForm.addEventListener('submit', function(e){
      var u = this.querySelector('input[name="username"]').value;
      var p = this.querySelector('input[name="password"]').value;
      if(u && p){
        sessionStorage.setItem('breogan_user', u);
        return true;
      }else{
        e.preventDefault();
        alert('Introduce nombre de usuario y contraseña');
        return false;
      }
    });
  }
})();
