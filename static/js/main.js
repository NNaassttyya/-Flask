// Инициализация Swiper
const swiper = new Swiper(".swiper", {
    loop: true,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
});
// Обработчики для категорий
const categories = document.querySelectorAll('.categories-cnt');
categories.forEach(category => {
    category.addEventListener('click', () => {
        category.classList.toggle('active');
    });
});

// Функции управления модальными окнами
function showRegisterForm() {
    document.getElementById('sign-up').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
}

function closeAllModals() {
    document.getElementById('sign-up').style.display = 'none';
    document.getElementById('register-form').style.display = 'none';
}

function switchToLogin() {
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('sign-up').style.display = 'block';
}

// Основные функции авторизации
function showLoginForm() {
    if (isLoggedIn()) {
        window.location.href = "profile.html";
        return;
    }
    document.getElementById('sign-up').style.display = 'block';
}

function isLoggedIn() {
    return localStorage.getItem('isLoggedIn') === 'true';
}

function changeToProfileButton() {
    const authButton = document.getElementById('auth-button');
    authButton.textContent = 'Профиль';
    authButton.classList.remove('entrance');
    authButton.classList.add('profile-button');
    authButton.onclick = function() {
        window.location.href = "profile.html";
    };
}

function logout() {
    localStorage.removeItem('isLoggedIn');
    const authButton = document.getElementById('auth-button');
    authButton.textContent = 'Войти';
    authButton.classList.remove('profile-button');
    authButton.classList.add('entrance');
    authButton.onclick = function() {
        showLoginForm();
    };
}

// Обработчик успешной регистрации
function registerUser() {
    // Здесь должна быть ваша логика регистрации
    localStorage.setItem('isLoggedIn', 'true');
    changeToProfileButton();
    alert('Регистрация прошла успешно!');
    closeAllModals();
}

// Обработчик входа
function handleLogin() {
    // Здесь должна быть ваша логика входа
    localStorage.setItem('isLoggedIn', 'true');
    changeToProfileButton();
    closeAllModals();
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    if (isLoggedIn()) {
        changeToProfileButton();
    }
    
    // Назначаем обработчик для кнопки входа
    const signUpBtn = document.querySelector('.signUpBtn');
    if (signUpBtn) {
        signUpBtn.addEventListener('click', handleLogin);
    }
    
    // Инициализация кнопки входа в шапке
    const authButton = document.getElementById('auth-button');
    if (authButton) {
        authButton.onclick = function() {
            if (isLoggedIn()) {
                window.location.href = "profile.html";
            } else {
                showLoginForm();
            }
        };
    }
});


  if (window.location.pathname.includes("panorama-page.html")) {
    setTimeout(function() {
      showPopup();
    }, 3000);
  }

  function showPopup() {
    const popup = document.getElementById('companionPopup');
    if (popup) {
      document.body.classList.add('popup-open');
      popup.style.display = 'flex';
    }
  }

  function closePopup() {
    const popup = document.getElementById('companionPopup');
    if (popup) {
      document.body.classList.remove('popup-open');
      popup.style.display = 'none';
    }
  }

  function findCompanion() {
    window.location.href = "find-companion.html";
    closePopup();
  }

  document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById('companionPopup');
    if (popup) {
      popup.addEventListener('click', function(e) {
        if (e.target === this) {
          closePopup();
        }
      });
    }
  });

