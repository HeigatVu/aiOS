document.getElementById('btn-update').addEventListener('click', async function() {
  var modal = document.getElementById('update-modal');
  var output = document.getElementById('update-output');
  var closeBtn = document.getElementById('btn-close-update');
  
  modal.style.display = 'flex';
  output.textContent = 'Starting system update... Please wait...\n';
  closeBtn.disabled = true;
  
  try {
    var response = await fetch('/api/update', { method: 'POST' });
    if (!response.ok) {
      throw new Error('Server returned ' + response.status);
    }
    var reader = response.body.getReader();
    var decoder = new TextDecoder('utf-8');
    while (true) {
      var { done, value } = await reader.read();
      if (done) break;
      output.textContent += decoder.decode(value, { stream: true });
      output.scrollTop = output.scrollHeight;
    }
    output.textContent += '\n\nUpdate process finished.\n';
  } catch (err) {
    output.textContent += '\nError running update: ' + err.message;
  } finally {
    closeBtn.disabled = false;
  }
});
