<script>
let localStream = null;

document.getElementById('startCam').addEventListener('click', async () => {
  try {
    // Start local camera display
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    document.getElementById('localCam').srcObject = localStream;

    // Start backend AI detection
    fetch('/api/start_live_camera', { method: 'POST' })
      .then(res => {
        if (!res.ok) { // Check for bad responses (like 500)
          throw new Error(`Server responded with status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => console.log("AI Detection:", data))
      .catch(error => { // ADD THIS BLOCK
        console.error('Error starting AI detection:', error);
        alert('Could not start the AI detection on the server. Please check the console.');
      });
  } catch (err) {
    alert('Camera access denied or not available: ' + err.message);
  }
});

document.getElementById('stopCam').addEventListener('click', () => {
  if (localStream) {
    localStream.getTracks().forEach(t => t.stop());
    document.getElementById('localCam').srcObject = null;
    localStream = null;
  }

  // Stop backend AI detection
  fetch('/api/stop_live_camera', { method: 'POST' })
    .then(res => {
        if (!res.ok) {
          throw new Error(`Server responded with status: ${res.status}`);
        }
        return res.json();
    })
    .then(data => console.log("AI Detection:", data))
    .catch(error => { // AND ADD THIS BLOCK
        console.error('Error stopping AI detection:', error);
        alert('Could not stop the AI detection on the server. Please check the console.');
    });
});
</script>