<script lang="ts">
  let isUploading = $state(false);
  let selectedFileName = $state<string | null>(null);

  async function handleUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];
    selectedFileName = file.name;
    isUploading = true;

    const formData = new FormData();
    formData.append('file', file);

    try {
      await fetch('http://localhost:8000/analyze', { method: 'POST', body: formData });
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      isUploading = false;
      input.value = '';
    }
  }
</script>

<div class="card">
  <div class="info">
    <h2 class="title">Upload Audio</h2>
    <p class="subtitle">Analyze an existing recording (WAV, MP3, M4A)</p>
  </div>

  <label class="dropzone {isUploading ? 'uploading' : ''}">
    <input
      type="file"
      accept="audio/*"
      onchange={handleUpload}
      class="hidden-input" 
      disabled={isUploading}
    />

    {#if isUploading}
      <div class="spinner"></div>
      <span class="dropzone-title uploading-text">Uploading & Analyzing...</span>
      <span class="dropzone-subtitle file-name">{selectedFileName}</span>
    {:else}
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="upload-icon">
        <path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
      <span class="dropzone-title">Click to upload or drag and drop</span>
      <span class="dropzone-subtitle">Maximum file size: 50MB</span>
    {/if}
  </label>
</div>

<style>
  .card {
    background-color: #111111;
    border: 1px solid #262626;
    border-radius: 12px;
    padding: 1.25rem;
  }

  .info {
    margin-bottom: 1rem;
  }

  .title {
    font-size: 0.875rem;
    font-weight: 500;
    color: #e5e5e5;
    margin: 0 0 0.25rem 0;
  }

  .subtitle {
    font-size: 0.75rem;
    color: #737373;
    margin: 0;
  }

  .dropzone {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 1rem;
    border: 1px dashed #404040;
    border-radius: 8px;
    background-color: rgba(23, 23, 23, 0.5);
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
  }

  .dropzone:hover:not(.uploading) {
    border-color: #3b82f6;
    background-color: rgba(59, 130, 246, 0.05);
  }

  .dropzone.uploading {
    cursor: not-allowed;
    border-style: solid;
    border-color: rgba(59, 130, 246, 0.3);
  }

  .hidden-input {
    display: none;
  }

  .upload-icon {
    color: #737373;
    margin-bottom: 0.75rem;
  }

  .dropzone-title {
    font-size: 0.875rem;
    font-weight: 500;
    color: #d4d4d4;
    margin-bottom: 0.25rem;
  }

  .dropzone-subtitle {
    font-size: 0.75rem;
    color: #737373;
  }

  .uploading-text {
    color: #60a5fa;
  }
  
  .file-name {
    max-width: 200px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .spinner {
    width: 24px;
    height: 24px;
    border: 2px solid rgba(59, 130, 246, 0.2);
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 0.75rem;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>