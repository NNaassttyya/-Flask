// Инициализация свайперов
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

const swiper1 = new Swiper(".card-wrapper", {
    scrollbar: {
        el: ".swiper-scrollbar",
        hide: true,
    },
});

// Плавная прокрутка для кнопки "Подробнее"
document.querySelector('.btn-main')?.addEventListener('click', function(e) {
    e.preventDefault();
    document.querySelector('.about-us-screen')?.scrollIntoView({
        behavior: 'smooth'
    });
});

// Обработка формы поддержки
document.addEventListener('DOMContentLoaded', function() {
    const supportForm = document.getElementById('supportForm');
    const successModal = document.getElementById('successModal');
    
    if (supportForm) {
        supportForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(supportForm);
            const submitBtn = supportForm.querySelector('.form-Btn');
            
            // Сохраняем оригинальный текст кнопки
            const originalBtnText = submitBtn.textContent;
            submitBtn.textContent = 'Отправка...';
            submitBtn.disabled = true;
            
            try {
                const response = await fetch(supportForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Показываем модальное окно успеха
                    if (successModal) {
                        successModal.style.display = 'flex';
                    }
                    // Очищаем форму
                    supportForm.reset();
                } else {
                    alert('Ошибка при отправке: ' + (data.error || 'Попробуйте позже'));
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при отправке формы');
            } finally {
                // Восстанавливаем кнопку
                submitBtn.textContent = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }
    
    // Закрытие модального окна
    const modalClose = document.querySelector('.modal-close');
    if (modalClose && successModal) {
        modalClose.addEventListener('click', function() {
            successModal.style.display = 'none';
        });
    }
    
    // Закрытие модального окна при клике вне его
    if (successModal) {
        successModal.addEventListener('click', function(e) {
            if (e.target === successModal) {
                successModal.style.display = 'none';
            }
        });
    }
});