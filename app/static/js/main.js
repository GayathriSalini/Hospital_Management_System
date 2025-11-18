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


/*Doctor Availability */


function showForm(date, time, id, title, nop) {
  document.getElementById('availability-form').style.display = 'block';
  document.body.style.overflowY = 'auto';
  document.getElementById('schedule_date').value = date;        
  document.getElementById('schedule_time').value = time || '';
  document.getElementById('schedule_id').value = id || '';
  document.getElementById('title').value = title || '';
  document.getElementById('nop').value = nop || '';
  document.getElementById('form-title').innerText = id ? 'Update Availability' : 'Add Availability';
}

function hideForm() {
  document.getElementById('availability-form').style.display = 'none';
  document.body.style.overflowY = '';  
  document.getElementById('schedule_id').value = '';
  document.getElementById('schedule_time').value = '';
  document.getElementById('title').value = '';
  document.getElementById('nop').value = '';
}

function markLeave(date, scheduleId) {
  if(confirm('Mark ' + date + ' as Leave?')) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = "{{ url_for('doctor.availability') }}";
    form.style.display = 'none';

    const scheduleInput = document.createElement('input');
    scheduleInput.type = 'hidden';
    scheduleInput.name = 'schedule_id';
    scheduleInput.value = scheduleId || '';

    const dateInput = document.createElement('input');
    dateInput.type = 'hidden';
    dateInput.name = 'schedule_date';
    dateInput.value = date;

    const titleInput = document.createElement('input');
    titleInput.type = 'hidden';
    titleInput.name = 'title';
    titleInput.value = 'On Leave';

    form.appendChild(scheduleInput);
    form.appendChild(dateInput);
    form.appendChild(titleInput);

    document.body.appendChild(form);
    form.submit();
  }
}

function showForm(date, time, schedule_id, title, nop) {
    document.getElementById('availability-form').style.display = 'block';
    document.getElementById('schedule_date').value = date;
    document.getElementById('schedule_time').value = time || '';
    document.getElementById('schedule_id').value = schedule_id || '';
    document.getElementById('title').value = title || '';
    document.getElementById('nop').value = nop || '';
    window.scrollTo(0, document.body.scrollHeight);
  }

  function hideForm() {
    document.getElementById('availability-form').style.display = 'none';
  }


