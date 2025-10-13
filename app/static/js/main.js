document.addEventListener('DOMContentLoaded', function () {
  const flashMessages = document.querySelectorAll('.alert-dismissible');
  const tabButtons = document.querySelectorAll('#loginTab button[data-bs-toggle="tab"]');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabPanes.forEach((pane) => {
    if (!pane.classList.contains('show', 'active')) {
      const alert = pane.querySelector('.alert-dismissible');
      if (alert) alert.style.display = 'none';
    }
  });

  
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      tabPanes.forEach(pane => {
        const alert = pane.querySelector('.alert-dismissible');
        if (alert) {
          if (pane.classList.contains('show', 'active')) {
            alert.style.display = 'block';
          } else {
            alert.style.display = 'none';
          }
        }
      });
    });
  });
});
