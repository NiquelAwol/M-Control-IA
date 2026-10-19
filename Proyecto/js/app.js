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

    // Inicializar widget multi-usuario global en la barra de navegación
    initUserSwitcher();
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

// ==========================================================================
// COMPONENTE GLOBAL: SWITCHER DE PARTICIPANTES / MULTI-USUARIO
// ==========================================================================

function initUserSwitcher() {
    if (!window.StorageService) return;
    const navContainer = document.querySelector('.nav-container');
    if (!navContainer) return;

    // Verificar si ya existe el widget
    if (!document.getElementById('btn-user-badge')) {
        const user = window.StorageService.getCurrentUser();
        const userEvents = window.StorageService.getEvents(user.id);

        const badgeWrapper = document.createElement('div');
        badgeWrapper.className = 'user-nav-container';
        badgeWrapper.style.display = 'flex';
        badgeWrapper.style.alignItems = 'center';
        badgeWrapper.style.gap = '0.5rem';

        badgeWrapper.innerHTML = `
            <button id="btn-user-badge" class="user-nav-badge" onclick="window.openUserSwitcherModal()" title="Participante activo: ${user.alias}">
                <span class="user-avatar-dot"></span>
                <span id="nav-user-alias">👤 ${user.alias} (${userEvents.length} ev)</span>
                <span style="font-size: 0.65rem; opacity: 0.8;">▼</span>
            </button>
            <a href="login.html" class="nav-link" style="font-size: 0.82rem; padding: 0.3rem 0.5rem; color: var(--text-muted);" title="Pantalla de inicio de sesión">⚙️</a>
        `;
        navContainer.appendChild(badgeWrapper);
    }

    // Inyectar el modal de selección de usuario si no está en el DOM
    if (!document.getElementById('user-switcher-modal')) {
        const modalHtml = `
        <div id="user-switcher-modal" class="modal-overlay" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 1000; align-items: center; justify-content: center; backdrop-filter: blur(4px);">
            <div class="modal-content" style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); max-width: 520px; width: 92%; padding: 1.5rem; box-shadow: var(--shadow); max-height: 90vh; overflow-y: auto;">
                <div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
                    <div>
                        <h3 style="margin: 0; font-size: 1.2rem; color: var(--text-primary);">👤 Perfiles de Participantes</h3>
                        <p style="margin: 0; font-size: 0.8rem; color: var(--text-secondary);">Selecciona tu alias o crea uno nuevo para tu sesión privada.</p>
                    </div>
                    <button class="modal-close" onclick="window.closeUserSwitcherModal()" style="background: none; border: none; color: var(--text-muted); font-size: 1.5rem; cursor: pointer;">&times;</button>
                </div>

                <div id="modal-current-user-banner" style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: var(--radius-sm); padding: 0.75rem 1rem; margin-bottom: 1.25rem; font-size: 0.88rem;">
                    <!-- Se llena dinámicamente -->
                </div>

                <h4 style="font-size: 0.9rem; margin-bottom: 0.6rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;">Participantes Registrados</h4>
                <div id="modal-users-list" style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.5rem; max-height: 220px; overflow-y: auto;">
                    <!-- Lista de participantes -->
                </div>

                <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 1.25rem 0;">

                <h4 style="font-size: 0.9rem; margin-bottom: 0.75rem; color: var(--text-primary);">➕ Registrar Nuevo Participante</h4>
                <form id="modal-register-form" onsubmit="window.handleModalRegister(event)" style="display: flex; flex-direction: column; gap: 0.75rem;">
                    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 0.5rem;">
                        <input type="text" id="modal-new-alias" class="form-control" placeholder="Alias (ej. Participante 4)" required style="padding: 0.5rem 0.75rem; font-size: 0.85rem;">
                        <input type="number" id="modal-new-edad" class="form-control" placeholder="Edad (ej. 23)" min="18" max="99" value="23" required style="padding: 0.5rem 0.75rem; font-size: 0.85rem;">
                    </div>
                    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 0.5rem;">
                        <select id="modal-new-objetivo" class="form-control" style="padding: 0.5rem 0.75rem; font-size: 0.85rem;">
                            <option value="autorregulacion">Autorregulación y Bienestar</option>
                            <option value="estres">Observar relación con Estrés</option>
                            <option value="descanso">Proteger Sueño y Energía</option>
                        </select>
                        <input type="password" id="modal-new-pin" class="form-control" placeholder="PIN (1234)" value="1234" maxlength="6" style="padding: 0.5rem 0.75rem; font-size: 0.85rem;">
                    </div>
                    <button type="submit" class="btn btn-success btn-sm" style="padding: 0.6rem; font-size: 0.88rem; font-weight: 600;">+ Crear Perfil y Cambiar a Él</button>
                </form>

                <div style="margin-top: 1.25rem; display: flex; justify-content: space-between; align-items: center;">
                    <a href="login.html" class="btn btn-secondary btn-sm" style="font-size: 0.82rem;">Ir a Pantalla de Login ➔</a>
                    <button type="button" class="btn btn-secondary btn-sm" onclick="window.closeUserSwitcherModal()">Cerrar</button>
                </div>
            </div>
        </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
}

window.openUserSwitcherModal = function() {
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
    const currentUser = window.StorageService.getCurrentUser();
    const users = window.StorageService.getUsers();
    const currentBanner = document.getElementById('modal-current-user-banner');
    const listContainer = document.getElementById('modal-users-list');

    if (currentBanner) {
        const count = window.StorageService.getEvents(currentUser.id).length;
        currentBanner.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: var(--color-green); font-weight: 700;">● ACTIVO AHORA:</span> 
                    <strong>${currentUser.alias}</strong> 
                    <span style="color: var(--text-secondary); font-size: 0.8rem;">(Edad: ${currentUser.edad || 24} años)</span>
                </div>
                <span class="user-chip-count">${count} evento(s)</span>
            </div>
        `;
    }

    if (listContainer) {
        listContainer.innerHTML = '';
        users.forEach(u => {
            const count = window.StorageService.getEvents(u.id).length;
            const isActive = u.id === currentUser.id;
            const item = document.createElement('div');
            item.className = `user-card-item ${isActive ? 'active' : ''}`;
            item.innerHTML = `
                <div class="user-info-text">
                    <span class="user-alias-title">${isActive ? '✓ ' : ''}${u.alias}</span>
                    <span class="user-subtext">Edad: ${u.edad || 24} · Objetivo: ${u.objetivo || 'Autorregulación'}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span class="user-chip-count">${count} reg.</span>
                    ${!isActive ? `<button class="btn btn-secondary btn-sm" style="padding: 0.25rem 0.6rem; font-size: 0.78rem;" onclick="window.switchParticipant(${u.id})">Entrar</button>` : `<span style="font-size: 0.75rem; color: var(--color-green); font-weight: 700;">En uso</span>`}
                </div>
            `;
            listContainer.appendChild(item);
        });
    }
}

window.switchParticipant = function(userId) {
    window.StorageService.setCurrentUser(userId);
    const user = window.StorageService.getCurrentUser();
    showToast(`Sesión cambiada a: ${user.alias}`);
    window.closeUserSwitcherModal();
    setTimeout(() => {
        window.location.reload();
    }, 350);
};

window.handleModalRegister = function(e) {
    e.preventDefault();
    const alias = document.getElementById('modal-new-alias').value.trim();
    const edad = document.getElementById('modal-new-edad').value.trim();
    const objetivo = document.getElementById('modal-new-objetivo').value;
    const pin = document.getElementById('modal-new-pin').value.trim();

    if (!alias) {
        alert('Por favor introduce un alias para el participante.');
        return;
    }

    const newUser = window.StorageService.registerUser(alias, edad, objetivo, pin);
    showToast(`Participante "${newUser.alias}" creado exitosamente.`);
    window.closeUserSwitcherModal();
    setTimeout(() => {
        window.location.reload();
    }, 400);
};
