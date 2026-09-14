/**
 * M-Control: Controlador de interfaz y utilidades compartidas
 */

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar almacenamiento
    if (window.StorageService) {
        window.StorageService.init();
    }

    // Resaltar link de navegación activo basado en la URL actual
    highlightActiveNav();

    // Aplicar Modo Anónimo si está activado
    applyAnonymousMode();
});

function highlightActiveNav() {
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '' && href === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

function applyAnonymousMode() {
    if (!window.StorageService) return;
    const settings = window.StorageService.getSettings();
    if (settings.modoAnonimo) {
        document.body.classList.add('anonymous-mode');
        const sensitiveElements = document.querySelectorAll('.sensitive-metric');
        sensitiveElements.forEach(el => {
            el.setAttribute('data-original-text', el.innerText);
            el.innerText = '••••';
        });
    }
}

function showToast(message, duration = 3000) {
    let toast = document.getElementById('global-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'global-toast';
        toast.className = 'toast-msg';
        document.body.appendChild(toast);
    }
    toast.innerText = message;
    toast.style.display = 'block';

    setTimeout(() => {
        toast.style.display = 'none';
    }, duration);
}

function formatDateDisplay(isoString) {
    if (!isoString) return 'Sin fecha';
    const d = new Date(isoString);
    return d.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Redireccionar con animación suave
function redirectTo(url) {
    window.location.href = url;
}
