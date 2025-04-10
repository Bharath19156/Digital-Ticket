$(document).ready(function () {
    console.log("Script loaded successfully"); // Debugging log

    $('#passTypeSelect').change(function () {
        var selectedOption = $(this).val();
        console.log("Selected Option:", selectedOption); // Debugging log

        // Hide all forms first
        $('#studentBusForm, #studentMetroForm, #generalBusForm, #generalMetroForm').slideUp();

        // Show the selected form
        if (selectedOption === 'student_bus') {
            $('#studentBusForm').slideDown();
        } else if (selectedOption === 'student_metro') {
            $('#studentMetroForm').slideDown();
        } else if (selectedOption === 'general_bus') {
            $('#generalBusForm').slideDown();
        } else if (selectedOption === 'general_metro') {
            $('#generalMetroForm').slideDown();
        }
    });
});





document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');  // should be 'form', not 'forms'
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            if (form.id === "generalBusPassForm") {
                alert('Bus Pass form submitted');
            } 
            if (form.id === "generalMetroPassForm") {
                alert('Metro Pass form submitted');
            }
            if (form.id === "studentBusPassForm") {
                alert('Bus Pass form submitted');
            }
            if (form.id === "studentMetroPassForm") {
                alert('Metro Pass form submitted');
            }

            form.submit();  // NOTE: submitting the form after preventing it above

            setTimeout(function() {
                window.location.reload();  // Correct function syntax
            }, 500);
        });
    });
});


function showPopup(status, itemId, name, validity, userType, remarks) {
    const statusText = document.getElementById('statusText');
    const qrImage = document.getElementById('qrImage');
    const userName = document.getElementById('userName');
    const userValidity = document.getElementById('userValidity');
    const userTypeSpan = document.getElementById('userType');
    const userRemarks = document.getElementById('userRemarks');
    const remarksRow = document.getElementById('remarksRow');
    const validityRow = document.getElementById('validityRow');
  
    // Reset fields
    qrImage.src = ""; // Clear QR image
    qrImage.style.display = 'none';
    qrImage.alt = ""; // Hide alt text too
  
    validityRow.style.display = 'none';
    remarksRow.style.display = 'none';
  
    userName.textContent = name || 'N/A';
    userTypeSpan.textContent = userType || 'N/A';
  
    status = status.toLowerCase().trim();
    remarks = remarks?.trim();
  
    if (status === 'approved') {
      statusText.textContent = 'Your application has been approved ✅';
  
      if (!remarks) {
        userValidity.textContent = validity || 'N/A';
        validityRow.style.display = 'block';
  
        fetch('/print_id', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: itemId })
        })
          .then(res => res.json())
          .then(data => {
            if (data.qr_url) {
              qrImage.src = data.qr_url;
              qrImage.alt = 'QR Code';
              qrImage.style.display = 'block';
            }
          })
          .catch(err => {
            console.error("QR fetch error:", err);
          });
      } else {
        userRemarks.textContent = remarks;
        remarksRow.style.display = 'block';
      }
  
    } else if (status === 'rejected') {
      statusText.textContent = 'Your application has been rejected ❌';
  
      // Only show name, user type, and remarks
      remarksRow.style.display = 'block';
      userRemarks.textContent = remarks || 'No remarks provided';
  
      // Hide QR image and validity explicitly
      qrImage.src = "";
      qrImage.style.display = 'none';
      qrImage.alt = "";
  
      validityRow.style.display = 'none';
  
    } else if (status === 'pending') {
      statusText.textContent = 'Your application is still pending ⏳';
  
    } else {
      statusText.textContent = 'Status unknown.';
    }
  
    const statusModal = new bootstrap.Modal(document.getElementById('statusModal'));
    statusModal.show();
}
  
  





