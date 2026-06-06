// ===== Sidebar Toggle (Mobile) =====
(function () {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.getElementById('hamburger');
    const sidebarClose = document.getElementById('sidebarClose');

    if (hamburger && sidebar) {
        hamburger.addEventListener('click', function () {
            sidebar.classList.toggle('open');
        });
    }

    if (sidebarClose && sidebar) {
        sidebarClose.addEventListener('click', function () {
            sidebar.classList.remove('open');
        });
    }

    // Close sidebar on nav click (mobile)
    if (sidebar) {
        sidebar.querySelectorAll('.nav-item').forEach(function (item) {
            item.addEventListener('click', function () {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('open');
                }
            });
        });
    }
})();

// ===== Flash Message Dismiss =====
(function () {
    document.querySelectorAll('.flash-close').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const flash = this.closest('.flash');
            if (flash) {
                flash.style.transition = 'opacity 0.3s ease';
                flash.style.opacity = '0';
                setTimeout(function () { flash.remove(); }, 300);
            }
        });
    });

    // Auto-dismiss after 5 seconds
    document.querySelectorAll('.flash').forEach(function (flash) {
        setTimeout(function () {
            if (flash && flash.parentNode) {
                flash.style.transition = 'opacity 0.5s ease';
                flash.style.opacity = '0';
                setTimeout(function () { flash.remove(); }, 500);
            }
        }, 5000);
    });
})();

// ===== AJAX Task Completion Toggle =====
(function () {
    document.querySelectorAll('.toggle-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            var btn = this.querySelector('.check-btn');
            var card = this.closest('.task-card');
            var formData = new FormData(this);

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.success) {
                    if (data.is_complete) {
                        btn.classList.add('checked');
                        btn.textContent = '\u2713';
                        card.classList.add('completed');
                        card.querySelector('.task-title').classList.add('struck');
                    } else {
                        btn.classList.remove('checked');
                        btn.textContent = '\u25CB';
                        card.classList.remove('completed');
                        card.querySelector('.task-title').classList.remove('struck');
                    }
                }
            })
            .catch(function () {
                // Fallback: submit normally
                var hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'fallback';
                hiddenInput.value = '1';
                form.appendChild(hiddenInput);
                form.submit();
            });
        });
    });
})();

// ===== Due Date Highlighting =====
(function () {
    document.querySelectorAll('.due-date.overdue').forEach(function (el) {
        el.title = 'This task is overdue!';
    });
})();
