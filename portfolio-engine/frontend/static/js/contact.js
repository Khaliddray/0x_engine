/**
 * Contact Script: Form Submission via /api/contact with Validation & Feedback
 */

async function handleContactSubmit(event) {
  event.preventDefault();

  const form = event.target;
  const submitBtn = form.querySelector('button[type="submit"]');
  const alertContainer = document.getElementById('contact-alert-container');

  const payload = {
    name: form.name.value.trim(),
    email: form.email.value.trim(),
    subject: form.subject.value.trim(),
    message: form.message.value.trim(),
  };

  if (!payload.name || !payload.email || !payload.subject || !payload.message) {
    showAlert(alertContainer, 'Please fill in all required fields.', 'alert-info');
    return;
  }

  // Set loading state
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'DISPATCHING INQUIRY...';
  }

  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error(`Inquiry submission failed (HTTP ${res.status})`);
    }

    const data = await res.json();
    showAlert(
      alertContainer,
      data.message || 'Your inquiry has been received! Yahaya Khalid will follow up shortly.',
      'alert-success'
    );
    form.reset();
  } catch (err) {
    // Fallback to mailto if API fails
    window.location.href = `mailto:khalidzak21@gmail.com?subject=${encodeURIComponent(
      payload.subject || 'Engineering Inquiry'
    )}&body=${encodeURIComponent(
      `From: ${payload.name} (${payload.email})\n\n${payload.message}`
    )}`;
    showAlert(
      alertContainer,
      'Opened your default email client to send your message directly.',
      'alert-info'
    );
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'TRANSMIT MESSAGE →';
    }
  }
}

function showAlert(container, message, typeClass) {
  if (!container) return;
  container.className = `alert-box ${typeClass}`;
  container.textContent = message;
  container.classList.remove('hidden');
}
