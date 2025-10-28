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



/*SEARCH ADMIN DOCTOR/PATIENT*/
function updateLabels() {
  let type = document.getElementById('search_type').value;
  let input = document.getElementById('query_input');
  if (type === 'patient') {
    input.placeholder = "Patient name, ID or contact";
  } else {
    input.placeholder = "Doctor name, email, NIC or specialization";
  }
}

window.onload = updateLabels;
document.getElementById('search_type').addEventListener('change', updateLabels);



