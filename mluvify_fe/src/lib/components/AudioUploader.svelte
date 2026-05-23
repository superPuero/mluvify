<script lang="ts">
  let { session } = $props<{ session: any }>();

  const uploader = {
    handleFile(event: Event) {
      const input = event.target as HTMLInputElement;
      if (!input.files?.length) return;

      const file = input.files[0];
      session.setAudio(file, file.name);

      input.value = ''; 
    }
  };
</script>

<label class="compact-upload {session.status.isProcessing ? 'uploading' : ''}">
  <input
    type="file"
    accept="audio/*"
    onchange={uploader.handleFile}
    class="hidden-input"
    disabled={session.status.isProcessing}
  />

  {#if session.status.isProcessing}
    <div class="spinner"></div>
    <span class="status truncate">Analyzing {session.audio.name}...</span>
  {:else if session.audio.name && !session.status.isRecording}
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" class="icon">
      <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
    </svg>
    <span class="status truncate">Ready: {session.audio.name}</span>
  {:else}
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon">
      <path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
    </svg>
    <span class="status">Upload Audio <span class="meta">(Max 50MB)</span></span>
  {/if}
</label>

<style>
  .hidden-input {
    display: none;
  }

  .compact-upload {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0.75rem;
    background-color: #111;
    border: 1px solid #262626;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
    max-width: 100%;
    width: auto;
  }

  .compact-upload:hover:not(.uploading) {
    border-color: #404040;
    background-color: #171717;
  }

  .compact-upload.uploading {
    cursor: not-allowed;
    background-color: rgba(23, 23, 23, 0.5);
    border-style: dashed;
  }

  .icon {
    color: #a3a3a3;
    flex-shrink: 0;
  }

  .status {
    font-size: 0.8125rem;
    color: #e5e5e5;
    white-space: nowrap;
  }

  .meta {
    color: #737373;
    font-size: 0.75rem;
    margin-left: 0.25rem;
  }

  .truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100px;
  }

  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(163, 163, 163, 0.2);
    border-top-color: #a3a3a3;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    flex-shrink: 0;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>