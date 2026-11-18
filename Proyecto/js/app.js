/**
 * M-Control: Controlador de interfaz, guardia de rutas y gestión de sesión
 */

(function enforceRouteGuardImmediately() {
    const rawPath = window.location.pathname.split('/').pop() || 'index.html';
    const currentPath = rawPath === '' ? 'index.html' : rawPath.toLowerCase();
    const publicPages = ['login.html', 'educacion.html'];

    let isAuth = false;
    try {
        const rawSess = localStorage.getItem('mcontrol_session_auth');
        const sess = rawSess ? JSON.parse(rawSess) : null;
        isAuth = !!(sess && sess.userId && sess.alias);
    } catch (e) {
        isAuth = false;
    }

    if (!isAuth && !publicPages.includes(currentPath)) {
        window.location.replace('login.html');
    }
})();

document.addEventListener('DOMContentLoaded', () => {
    if (window.StorageService) {
        window.StorageService.init();
    }

    const currentPath = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
    const isAuth = window.StorageService ? window.StorageService.isAuthenticated() : false;

    // Adaptar barra de navegación según si el visitante tiene sesión o solo está viendo Misión/Visión
    adaptNavbarForAuthState(isAuth, currentPath);

    // Resaltar link de navegación activo basado en la URL actual
    highlightActiveNav();

    // Aplicar Modo Anónimo si está activado
    if (isAuth) {
        applyAnonymousMode();
        initSessionBadgeAndAdminModal();
    }
});

function adaptNavbarForAuthState(isAuth, currentPath) {
    const navList = document.querySelector('.nav-links');
    const brandLink = document.querySelector('.brand');

    if (!isAuth) {
        // Visitante sin cuenta: solo puede ver login.html y educacion.html (Misión, Visión, Objetivos y Proyecto)
        if (brandLink) {
            brandLink.setAttribute('href', 'login.html');
        }
        if (navList) {
            navList.innerHTML = `
                <li><a href="educacion.html" class="nav-link ${currentPath === 'educacion.html' ? 'active' : ''}">🏛️ ¿En qué consiste M-Control? (Misión y Visión)</a></li>
                <li><a href="login.html" class="nav-link nav-btn-action">🔐 Iniciar Sesión</a></li>
            `;
        }
        // Ocultar botones de acción privados en educacion.html si no ha iniciado sesión
        const btnReg = document.querySelector('a[href="registro.html"].btn');
        if (btnReg) {
            btnReg.setAttribute('href', 'login.html');
            btnReg.innerHTML = '🔐 Iniciar Sesión para Acceder al Sistema';
        }
    } else {
        // Usuario autenticado: asegurar texto claro en el menú de Misión/Evidencia
        const eduLink = document.querySelector('a[href="educacion.html"].nav-link');
        if (eduLink) {
            eduLink.innerHTML = '🏛️ Proyecto y Misión';
        }
        // Ocultar enlaces de "Cambiar participante" en index.html si no es admin
        if (!window.StorageService.isAdmin()) {
            const switchLinks = document.querySelectorAll('a[onclick*="openUserSwitcherModal"], a[href="login.html"].btn-secondary');
            switchLinks.forEach(el => {
                el.style.display = 'none';
            });
        }
    }
}

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

function redirectTo(url) {
    window.location.href = url;
}

window.handleLogout = function() {
    if (window.StorageService) {
        window.StorageService.logout();
    }
    window.location.href = 'login.html';
};

// ==========================================================================
// COMPONENTE GLOBAL: BADGE DE SESIÓN Y PANEL EXCLUSIVO DE ADMINISTRADOR
// ==========================================================================

function initSessionBadgeAndAdminModal() {
    if (!window.StorageService || !window.StorageService.isAuthenticated()) return;
    const navContainer = document.querySelector('.nav-container');
    if (!navContainer) return;

    const user = window.StorageService.getCurrentUser();
    const isAdmin = window.StorageService.isAdmin();

    if (!document.getElementById('btn-user-badge')) {
        const badgeWrapper = document.createElement('div');
        badgeWrapper.className = 'user-nav-container';
        badgeWrapper.style.display = 'flex';
        badgeWrapper.style.alignItems = 'center';
        badgeWrapper.style.gap = '0.5rem';

        badgeWrapper.innerHTML = `
            <span id="btn-user-badge" class="user-nav-badge" style="cursor: default;" title="Sesión activa: ${user.alias}">
                <span class="user-avatar-dot"></span>
                <span id="nav-user-alias">${isAdmin ? '👑' : '👤'} ${user.alias}</span>
            </span>
            ${isAdmin ? `
                <button class="btn btn-secondary btn-sm" style="padding: 0.35rem 0.65rem; font-size: 0.78rem; border-color: var(--accent); color: var(--accent);" onclick="window.openUserSwitcherModal()" title="Panel exclusivo de Administrador para crear usuarios">
                    👑 Crear / Gestionar Usuarios
                </button>
            ` : ''}
            <button class="btn btn-secondary btn-sm" style="padding: 0.35rem 0.65rem; font-size: 0.78rem; color: #f87171; border-color: rgba(239,68,68,0.35);" onclick="window.handleLogout()" title="Cerrar sesión">
                🚪 Salir
            </button>
        `;
        navContainer.appendChild(badgeWrapper);
    }

    // Solo inyectar el modal de gestión de usuarios si el usuario activo es el Administrador
    if (isAdmin && !document.getElementById('user-switcher-modal')) {
        const modalHtml = `
        <div id="user-switcher-modal" class="modal-overlay" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.75); z-index: 1000; align-items: center; justify-content: center; backdrop-filter: blur(4px);">
            <div class="modal-content" style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); max-width: 560px; width: 92%; padding: 1.5rem; box-shadow: var(--shadow); max-height: 90vh; overflow-y: auto;">
                <div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <h3 style="margin: 0; font-size: 1.2rem; color: var(--text-primary);">👑 Panel de Administrador: Gestión de Usuarios</h3>
                        <p style="margin: 0; font-size: 0.8rem; color: var(--text-secondary);">Solo tú como Administrador puedes crear cuentas y asignar contraseñas a los participantes.</p>
                    </div>
                    <button class="modal-close" onclick="window.closeUserSwitcherModal()" style="background: none; border: none; color: var(--text-muted); font-size: 1.5rem; cursor: pointer;">&times;</button>
                </div>

                <h4 style="font-size: 0.85rem; margin-bottom: 0.6rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.5px;">➕ Crear Nuevo Usuario Autorizado</h4>
                <form id="modal-register-form" onsubmit="window.handleModalRegister(event)" style="background: rgba(15, 23, 42, 0.55); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 1rem; margin-bottom: 1.25rem; display: flex; flex-direction: column; gap: 0.75rem;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;">
                        <div>
                            <label style="font-size: 0.75rem; color: var(--text-secondary); display: block; margin-bottom: 3px;">Usuario (Login) *</label>
                            <input type="text" id="modal-new-alias" class="form-control" placeholder="Ej. sujeto4 o carlos24" required style="padding: 0.5rem 0.75rem; font-size: 0.85rem;">
                        </div>
                        <div>
                            <label style="font-size: 0.75rem; color: var(--text-secondary); display: block; margin-bottom: 3px;">Contraseña Asignada *</label>
                            <input type="text" id="modal-new-pin" class="form-control" placeholder="Ej. clave2026" required style="padding: 0.5rem 0.75rem; font-size: 0.85rem;">
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 0.6rem;">
                        <div>
                            <label style="font-size: 0.75rem; color: var(--text-secondary); display: block; margin-bottom: 3px;">Edad *</label>
                            <input type="number" id="modal-new-edad" class="form-control" min="18" max="99" value="23" required style="padding: 0.5rem 0.75rem; font-size: 0.85rem;">
                        </div>
                        <div>
                            <label style="font-size: 0.75rem; color: var(--text-secondary); display: block; margin-bottom: 3px;">Objetivo del Participante</label>
                            <select id="modal-new-objetivo" class="form-control" style="padding: 0.5rem 0.75rem; font-size: 0.85rem;">
                                <option value="autorregulacion">Autorregulación y Bienestar</option>
                                <option value="estres">Observar relación con Estrés</option>
                                <option value="descanso">Proteger Sueño y Energía</option>
                            </select>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-success btn-sm" style="padding: 0.6rem; font-size: 0.88rem; font-weight: 700;">✨ Crear Usuario y Contraseña</button>
                </form>

                <h4 style="font-size: 0.85rem; margin-bottom: 0.6rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;">📋 Cuentas Registradas en el Sistema</h4>
                <div id="modal-users-list" style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.25rem; max-height: 230px; overflow-y: auto;">
                    <!-- Lista de usuarios -->
                </div>

                <div style="display: flex; justify-content: flex-end;">
                    <button type="button" class="btn btn-secondary btn-sm" onclick="window.closeUserSwitcherModal()">Cerrar Panel</button>
                </div>
            </div>
        </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
}

window.openUserSwitcherModal = function() {
    if (!window.StorageService || !window.StorageService.isAdmin()) {
        showToast('Solo el Administrador puede gestionar cuentas de usuarios.');
        return;
    }
    const modal = document.getElementById('user-switcher-modal');
    if (!modal) return;
    renderUserSwitcherList();
    modal.style.display = 'flex';
};

window.closeUserSwitcherModal = function() {
    const modal = document.getElementById('user-switcher-modal');
    if (modal) modal.style.display = 'none';
};

function renderUserSwitcherList() {
    const users = window.StorageService.getUsers();
    const listContainer = document.getElementById('modal-users-list');
    if (!listContainer) return;

    listContainer.innerHTML = '';
    users.forEach(u => {
        const count = window.StorageService.getEvents(u.id).length;
        const isUserAdmin = (u.alias || '').toLowerCase() === 'admin' || u.rol === 'admin';
        const item = document.createElement('div');
        item.className = 'user-card-item';
        item.innerHTML = `
            <div class="user-info-text">
                <span class="user-alias-title">${isUserAdmin ? '👑 ' : '👤 '}<strong>${u.alias}</strong> <span style="font-size: 0.78rem; color: var(--accent); margin-left: 6px;">[Clave: ${u.pin || '1234'}]</span></span>
                <span class="user-subtext">Edad: ${u.edad || 24} años · Eventos registrados: ${count}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
                ${!isUserAdmin ? `<button class="btn btn-secondary btn-sm" style="padding: 0.25rem 0.55rem; font-size: 0.75rem; color: #f87171;" onclick="window.handleAdminDeleteUser(${u.id})">Eliminar</button>` : `<span style="font-size: 0.75rem; color: var(--color-green); font-weight: 700;">Admin</span>`}
            </div>
        `;
        listContainer.appendChild(item);
    });
}

window.handleAdminDeleteUser = async function(userId) {
    if (!confirm('¿Estás seguro de eliminar este usuario y sus registros?')) return;
    await window.StorageService.adminDeleteUser(userId);
    renderUserSwitcherList();
    showToast('Usuario eliminado correctamente.');
};

window.handleModalRegister = async function(e) {
    e.preventDefault();
    const alias = document.getElementById('modal-new-alias').value.trim();
    const edad = document.getElementById('modal-new-edad').value.trim();
    const objetivo = document.getElementById('modal-new-objetivo').value;
    const pin = document.getElementById('modal-new-pin').value.trim();

    try {
        const newUser = await window.StorageService.adminCreateUser(alias, edad, objetivo, pin);
        document.getElementById('modal-new-alias').value = '';
        document.getElementById('modal-new-pin').value = '';
        renderUserSwitcherList();
        showToast(`✅ Usuario "${newUser.alias}" creado con contraseña "${newUser.pin}".`);
    } catch (err) {
        alert(err.message || 'No se pudo crear el usuario.');
    }
};
