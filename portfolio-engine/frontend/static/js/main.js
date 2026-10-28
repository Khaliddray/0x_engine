/**
 * Main Application Script: Theme Toggle, Navigation Drawer & Global Utilities
 */

// Theme Management
(function initTheme() {
  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark = (saved === 'dark' || (!saved && prefersDark) || !saved);
  if (isDark) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  document.addEventListener('DOMContentLoaded', () => {
    if (document.body) {
      document.body.classList.toggle('dark', document.documentElement.classList.contains('dark'));
    }
  });
})();

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  if (document.body) {
    document.body.classList.toggle('dark', isDark);
  }
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

// Navigation Drawer Menu
function openNavigationMenu() {
  const panel = document.getElementById('navigation-panel');
  const btn = document.querySelector('.menu-toggle-btn');
  if (panel) {
    panel.classList.remove('hidden');
    if (btn) btn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }
}

function closeNavigationMenu() {
  const panel = document.getElementById('navigation-panel');
  const btn = document.querySelector('.menu-toggle-btn');
  if (panel) {
    panel.classList.add('hidden');
    if (btn) btn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
}

// Global Keyboard Handler (Escape Key)
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    closeNavigationMenu();
    if (typeof closeProjectModal === 'function') {
      closeProjectModal();
    }
  }
});

// Copy Email Utility
function copyEmailToClipboard(btn) {
  navigator.clipboard.writeText('khalidzak21@gmail.com').then(() => {
    if (btn) {
      const originalText = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(() => {
        btn.textContent = originalText;
      }, 2500);
    }
  });
}

// Smooth Scroll to Top
function scrollToTop(e) {
  if (e) e.preventDefault();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
