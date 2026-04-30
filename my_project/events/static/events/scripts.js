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
});
