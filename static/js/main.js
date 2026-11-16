document.addEventListener('DOMContentLoaded', function() {
    // Авто скрытие всяких алёртов, тут можете придумать что-нибудь своё красивое
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            alert.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // По критериям вроде надо
    const statusSelects = document.querySelectorAll('.status-select');
    statusSelects.forEach(select => {
        select.addEventListener('change', function(e) {
            if (!confirm(`Изменить статус заявки на "${this.options[this.selectedIndex].text}"?`)) {
                e.preventDefault();
                this.value = this.defaultValue;
            }
        });
    });

    // Вроде по критериям надо
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = 'var(--color-danger)';
                    valid = false;
                } else {
                    field.style.borderColor = '';
                }
            });
            if (!valid) {
                e.preventDefault();
                alert('Пожалуйста, заполните все обязательные поля');
            }
        });
    });

    // Для красоты, забейте, не обязательно.
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});