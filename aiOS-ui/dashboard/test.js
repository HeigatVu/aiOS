// ── Starfield ──
(function(){
  var c = document.getElementById('stars');
  for (var i = 0; i < 80; i++) {
    var s = document.createElement('div');
    s.className = 'star';
    var size = Math.random() * 2 + 1;
    s.style.cssText =
      'left:' + (Math.random()*100) + '%;' +
      'top:' + (Math.random()*100) + '%;' +
      'width:' + size + 'px;' +
      'height:' + size + 'px;' +
      '--dur:' + (Math.random()*3+2) + 's;' +
      '--delay:' + (Math.random()*3) + 's;';
    c.appendChild(s);
  }
})();

// ── Quick Access links ──
(function(){
  var host = window.location.hostname || '127.0.0.1';
  var am = document.getElementById('lnk-agentmemory');
  if (am) am.href = 'http://' + host + ':3113';
  var fb = document.getElementById('lnk-files');
  if (fb) fb.href = 'http://' + host + ':8787/files';
})();

// ── Health check ──
async function checkHealth() {
  var dot = document.getElementById('status-dot');
  var txt = document.getElementById('status-text');
  try {
    var r = await fetch('/health');
    var d = await r.json();
    if (d.subserver && d.subserver.healthy) {
      dot.classList.remove('dead');
      txt.textContent = 'subserver ok (pid ' + d.subserver.pid + ') | :' + d.subserver.port;
    } else {
      dot.classList.add('dead');
      txt.textContent = 'subserver not ready';
    }
  } catch(e) {
    dot.classList.add('dead');
    txt.textContent = 'health check error';
  }
}
checkHealth();
setInterval(checkHealth, 10000);

// ── Update System ──
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
    var data = await response.json();
    output.textContent += '\n=== STDOUT ===\n' + (data.stdout || '(no output)') + '\n';
    if (data.stderr) {
      output.textContent += '\n=== STDERR ===\n' + data.stderr + '\n';
    }
    output.textContent += '\nFinished with code ' + data.returncode + '.';
  } catch (err) {
    output.textContent += '\nError running update: ' + err.message;
  } finally {
    closeBtn.disabled = false;
  }
});

function closeUpdateModal() {
  document.getElementById('update-modal').style.display = 'none';
}

function closeModalOutside(event) {
  var closeBtn = document.getElementById('btn-close-update');
  if (!closeBtn.disabled && event.target === document.getElementById('update-modal')) {
    closeUpdateModal();
  }
}
