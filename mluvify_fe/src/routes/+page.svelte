<script lang="ts">
  import AudioRecorder from '$lib/components/AudioRecorder.svelte';
  import AudioUploader from '$lib/components/AudioUploader.svelte';
  import Button from '$lib/components/Button.svelte';

  interface CriteriaContextData {
    criterias: Record<string, number[]>;
    all_messages: string[],
  }

  // Define the entire session as a single deeply reactive state object
  const session = $state({
    messages: [] as string[],
    criterias: {} as Record<string, number[]>,
    audio: { blob: null as Blob | null, name: null as string | null },
    status: { isRecording: false, isProcessing: false },

    setAudio(blob: Blob, name: string) {
      session.audio.blob = blob;
      session.audio.name = name;
    },

    clearAudio() {
      session.audio.blob = null;
      session.audio.name = null;
    },

    async send() {
      if (!session.audio.blob) return;
      session.status.isProcessing = true;

      const formData = new FormData();
      formData.append('file', session.audio.blob, session.audio.name || 'audio.webm');

      try {
        const response = await fetch('http://localhost:8000/analyze/semantic', { 
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error(`Server responded with status: ${response.status}`);
        }

        const data: CriteriaContextData = await response.json();
        console.log("Data from backend:", data); // Check the array length here!

        // Directly update the reactive object
        session.messages = data.all_messages;
        session.criterias = data.criterias;

        session.clearAudio();
      } catch (error) {
        console.error("Upload failed:", error);
      } finally {
        session.status.isProcessing = false;
      }
    }
  });
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
      <!-- Left Column: LLM Chat -->
      <div class="column">
        <div class="panel chat-panel">
          <div class="panel-header">
            <h2>Live Session</h2>
          </div>
          
          <div class="chat-messages">
            {#if session.messages.length === 0}
              <div class="message system">
                Awaiting audio input to begin analysis...
              </div>
            {:else}
              <!-- Use index (i) to determine if message is user (even) or bot (odd) -->
              {#each session.messages as message, i}
                <div class="message-wrapper {i % 2 === 0 ? 'user' : 'bot'}">
                  <div class="message-bubble">
                    {message}
                  </div>
                </div>
              {/each}
            {/if}
          </div>

          <div class="chat-input-area">
            <Button 
              label={session.status.isProcessing ? "Processing..." : "Send Audio"} 
              onclick={() => session.send()} 
              disabled={!session.audio.blob || session.status.isProcessing} 
            />
            <AudioRecorder {session} />
            <AudioUploader {session} />
          </div>
        </div>
      </div>

      <div class="column">
        <div class="panel stats-panel">
          <div class="panel-header">
            <h2>Evaluation Statistics</h2>
          </div>
          
          <div class="stats-content">
            <!-- Check if there is any criteria data yet -->
            {#if Object.keys(session.criterias).length === 0}
              <div class="placeholder-card">
                <p class="placeholder-title">Awaiting Audio</p>
                <p class="placeholder-text">Semantic and acoustic metrics will appear here</p>
              </div>
            {:else}
              <div class="criteria-list">
                <!-- Loop through the dictionary keys and values -->
                {#each Object.entries(session.criterias) as [name, values]}
                  <!-- Grab the most recent value from the array, fallback to 0 -->
                  {@const latestValue = values[values.length - 1] || 0}
                  
                  <div class="criteria-item">
                    <div class="criteria-header">
                      <span class="criteria-name">{name.replace(/_/g, ' ')}</span>
                      <!-- Display the raw number formatted to 2 decimal places in a badge -->
                      <span class="criteria-value">{latestValue.toFixed(2)}</span> 
                    </div>
                    
                    <!-- The visual bar (0 to 1 mapped to 0% to 100%) -->
                    <div class="progress-track">
                      <div 
                        class="progress-fill" 
                        style="width: {latestValue * 100}%"
                      ></div>
                    </div>
                  </div>
                {/each}
              </div>
            {/if}
          </div>
        </div>
      </div>  
    </main>
  </div>
</div>

<style>
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
    max-width: 1200px;
    margin: 0 auto;
  }

  .header {
    margin-bottom: 2rem;
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
    height: calc(100vh - 180px);
    min-height: 500px;
  }

  @media (min-width: 768px) {
    .grid-layout {
      grid-template-columns: 3fr 2fr;
    }
  }

  .column {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .panel {
    background-color: #0a0a0a;
    border: 1px solid #262626;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }

  .panel-header {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid #262626;
    background-color: #121212;
  }

  .panel-header h2 {
    margin: 0;
    font-size: 1rem;
    font-weight: 500;
    color: #d4d4d4;
  }

  .chat-messages {
    flex: 1;
    padding: 1.25rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .message.system {
    align-self: center;
    color: #737373;
    font-size: 0.875rem;
    margin-top: auto;
    margin-bottom: auto;
  }

  /* --- CHAT STYLES --- */
  .message-wrapper {
    display: flex;
    width: 100%;
  }

  .message-wrapper.user {
    justify-content: flex-end;
  }

  .message-wrapper.bot {
    justify-content: flex-start;
  }

  .message-bubble {
    max-width: 80%;
    padding: 0.75rem 1rem;
    border-radius: 12px;
    font-size: 0.95rem;
    line-height: 1.5;
    word-break: break-word;
  }

  .message-wrapper.user .message-bubble {
    background-color: #2563eb; 
    color: #ffffff;
    border-bottom-right-radius: 4px; 
  }

  .message-wrapper.bot .message-bubble {
    background-color: #262626; 
    color: #e5e5e5;
    border-bottom-left-radius: 4px; 
  }

  .chat-input-area {
    padding: 1.25rem;
    border-top: 1px solid #262626;
    background-color: #121212;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .stats-content {
    flex: 1;
    padding: 1.25rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }

  .placeholder-card {
    height: 100%;
    min-height: 300px;
    border: 1px dashed #262626;
    background-color: rgba(23, 23, 23, 0.3);
    border-radius: 8px;
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

  /* --- NEW CRITERIA LIST STYLES --- */
  .criteria-list {
    display: flex;
    flex-direction: column;
    gap: 1.25rem; /* Spacious gap between criteria items */
  }

  .criteria-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem; /* Gap between header and progress bar */
  }

  .criteria-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .criteria-name {
    font-size: 0.875rem;
    font-weight: 500;
    color: #d4d4d4;
    text-transform: capitalize;
  }

  .criteria-value {
    font-size: 0.75rem;
    font-weight: 600;
    color: #ffffff;
    background-color: #262626; /* Dark pill badge */
    padding: 0.125rem 0.5rem;
    border-radius: 9999px; /* Fully rounded edges */
    font-variant-numeric: tabular-nums; /* Keeps width consistent as numbers change */
    border: 1px solid #333;
  }

  .progress-track {
    width: 100%;
    height: 6px;
    background-color: #1f1f1f; /* Deeper background for the track */
    border-radius: 9999px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    /* Sleek gradient from blue to purple matching the dark theme */
    background: linear-gradient(90deg, #3b82f6, #8b5cf6); 
    border-radius: 9999px;
    /* Smooth transition when values change */
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }
</style>