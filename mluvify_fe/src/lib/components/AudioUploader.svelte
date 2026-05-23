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
      // Changed to use a variable for cleaner URL management in real apps
      await fetch('http://localhost:8000/semantic', { method: 'POST', body: formData });
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      isUploading = false;
      input.value = '';
    }
  }
</script>

<label class="compact-upload {isUploading ? 'uploading' : ''}">
  <input
    type="file"
    accept="audio/*"
    onchange={handleUpload}
    class="hidden-input"
    disabled={isUploading}
  />

  {#if isUploading}
    <div class="spinner"></div>
    <span class="status truncate">Analyzing {selectedFileName}...</span>
  {:else}
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon">
      <path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
    </svg>
    <span class="status">Upload Audio <span class="meta">(Max 50MB)</span></span>
  {/if}
</label>

<style>
  /* Base styles to maintain functionality */
  .hidden-input {
    display: none;
  }

  /* Compact Container */
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
    max-width: 100%; /* Ensure it fits its parent */
    width: auto; /* Don't take up full width by default */
  }

  /* Hover state */
  .compact-upload:hover:not(.uploading) {
    border-color: #404040;
    background-color: #171717;
  }

  /* Uploading/Disabled State */
  .compact-upload.uploading {
    cursor: not-allowed;
    background-color: rgba(23, 23, 23, 0.5);
    border-style: dashed;
  }

  /* Icon styling */
  .icon {
    color: #a3a3a3;
    flex-shrink: 0;
  }

  /* Text styling */
  .status {
    font-size: 0.8125rem; /* 13px */
    color: #e5e5e5;
    white-space: nowrap;
  }

  /* Secondary text (Max size) */
  .meta {
    color: #737373;
    font-size: 0.75rem;
    margin-left: 0.25rem;
  }

  /* Helper for long filenames during upload */
  .truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100px; /* Adjust as needed for your layout */
  }

  /* Minimal Spinner */
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