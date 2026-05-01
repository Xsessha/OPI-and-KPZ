document.addEventListener('DOMContentLoaded', function () {
  const wishlistTextarea = document.querySelector('#id_wish_text');
  document.querySelectorAll('.suggestion-chip').forEach((chip) => {
    chip.addEventListener('click', function () {
      if (!wishlistTextarea) return;
      wishlistTextarea.value = this.dataset.suggestion;
      wishlistTextarea.focus();
    });
  });

  document.querySelectorAll('form[data-loading]').forEach((form) => {
    form.addEventListener('submit', function () {
      const submitButton = form.querySelector('[type="submit"]');
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = 'Saving...';
      }
    });
  });

  // Auto-refresh page on home/dashboard to show updated participant counts
  if (document.querySelector('.event-grid') || document.querySelector('.empty-state')) {
    let refreshInterval;
    const startAutoRefresh = () => {
      clearInterval(refreshInterval);
      refreshInterval = setInterval(() => {
        location.reload();
      }, 3000); // Refresh every 3 seconds
    };

    // Handle visibility change - refresh when returning to tab
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        clearInterval(refreshInterval);
      } else {
        location.reload();
      }
    });

    startAutoRefresh();
  }
});
