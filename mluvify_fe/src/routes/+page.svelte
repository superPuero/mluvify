<script lang="ts">
  import AudioRecorder from '$lib/components/AudioRecorder.svelte';
  import AudioUploader from '$lib/components/AudioUploader.svelte';
//   import LiveTranscript from '$lib/components/LiveTranscript.svelte';
</script>

<div class="app-container">
  <div class="content-wrapper">
    <header class="header">
      <h1 class="title">Mluvify</h1>
      <p class="subtitle">
        AI-powered semantic speech analysis for detecting potential psychological and neurological patterns.
      </p>
    </header>

    <main class="grid-layout">
      <!-- Left Column: Inputs -->
      <div class="column">
        <AudioRecorder />
        <AudioUploader />
        <!-- <LiveTranscript /> -->
      </div>

      <!-- Right Column: Analysis -->
      <div class="column">
        <div class="placeholder-card">
          <p class="placeholder-title">Awaiting Audio</p>
          <p class="placeholder-text">Results will appear here</p>
        </div>
      </div>
    </main>
  </div>
</div>

<style>
  /* Global-ish reset for this container */
    :global(body) {
        margin: 0;
        padding: 0;
        background-color: #000000; 
    }

  .app-container {
    min-height: 100vh;
    background-color: #000000;
    color: #e5e5e5;
    font-family: system-ui, -apple-system, sans-serif;
    padding: 2rem;
    box-sizing: border-box;
  }

  .content-wrapper {
    max-width: 1000px;
    margin: 0 auto;
  }

  .header {
    margin-bottom: 3rem;
  }

  .title {
    font-size: 1.875rem;
    font-weight: 500;
    color: #ffffff;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.025em;
  }

  .subtitle {
    color: #737373;
    font-size: 0.875rem;
    max-width: 600px;
    margin: 0;
    line-height: 1.5;
  }

  .grid-layout {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  @media (min-width: 768px) {
    .grid-layout {
      grid-template-columns: 1fr 1fr;
    }
  }

  .column {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .placeholder-card {
    height: 100%;
    min-height: 300px;
    border: 1px dashed #262626;
    background-color: rgba(23, 23, 23, 0.3);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  .placeholder-title {
    font-size: 0.875rem;
    font-weight: 500;
    color: #a3a3a3;
    margin: 0 0 0.25rem 0;
  }

  .placeholder-text {
    font-size: 0.75rem;
    color: #525252;
    margin: 0;
  }
</style>