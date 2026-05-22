<script lang="ts">
  let isRecording = $state(false);
  let recordingTime = $state(0);
  
  let mediaRecorder: MediaRecorder;
  let audioChunks: Blob[] = [];
  let interval: ReturnType<typeof setInterval>;

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');

      await fetch('http://localhost:8000/analyze', { method: 'POST', body: formData });
      audioChunks = [];
      stream.getTracks().forEach(track => track.stop());
    };

    mediaRecorder.start(1000);
    isRecording = true;
    recordingTime = 0;

    interval = setInterval(() => {
      recordingTime++;
    }, 1000);
  }

  function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") mediaRecorder.stop();
    clearInterval(interval);
    isRecording = false;
  }

  function formatTime(seconds: number) {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }
</script>

<div class="card">
  <div class="info">
    <h2 class="title">
      Live Recording
      {#if isRecording}
        <span class="pulse-dot"></span>
      {/if}
    </h2>
    <p class="subtitle">Capture speech via microphone</p>
  </div>

  <div class="controls">
    <div class="timer {isRecording ? 'recording' : ''}">
      {formatTime(recordingTime)}
    </div>

    {#if !isRecording}
      <button class="btn btn-start" onclick={startRecording} aria-label="Start Recording">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8"/>
        </svg>
      </button>
    {:else}
      <button class="btn btn-stop" onclick={stopRecording} aria-label="Stop Recording">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
          <rect x="5" y="5" width="14" height="14" rx="2" />
        </svg>
      </button>
    {/if}
  </div>
</div>

<style>
  .card {
    background-color: #111111;
    border: 1px solid #262626;
    border-radius: 12px;
    padding: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .info {
    display: flex;
    flex-direction: column;
  }

  .title {
    font-size: 0.875rem;
    font-weight: 500;
    color: #e5e5e5;
    margin: 0 0 0.25rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .pulse-dot {
    width: 6px;
    height: 6px;
    background-color: #ef4444;
    border-radius: 50%;
    animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  .subtitle {
    font-size: 0.75rem;
    color: #737373;
    margin: 0;
  }

  .controls {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .timer {
    font-family: monospace;
    font-size: 0.875rem;
    color: #737373;
    width: 2.5rem;
    text-align: right;
  }

  .timer.recording {
    color: #f87171;
  }

  .btn {
    all: unset;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .btn-start {
    background-color: #262626;
    color: #d4d4d4;
  }

  .btn-start:hover {
    background-color: #404040;
  }

  .btn-stop {
    background-color: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }

  .btn-stop:hover {
    background-color: rgba(239, 68, 68, 0.2);
  }
</style>