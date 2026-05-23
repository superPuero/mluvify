<script lang="ts">
  import AudioRecorder from '$lib/components/AudioRecorder.svelte';
  import AudioUploader from '$lib/components/AudioUploader.svelte';
  import Button from '$lib/components/Button.svelte';

  interface CriteriaContextData {
    criterias: Record<string, number[]>;
    all_messages: string[],
  }

  class SessionData {
    messages = $state<string[]>([]);
    criterias = $state<Record<string, number[]>>({});
    
    audio = $state<{ blob: Blob | null, name: string | null }>({ blob: null, name: null });
    status = $state<{ isRecording: boolean, isProcessing: boolean }>({ isRecording: false, isProcessing: false });

    setAudio(blob: Blob, name: string) {
      this.audio.blob = blob;
      this.audio.name = name;
    }

    clearAudio() {
      this.audio.blob = null;
      this.audio.name = null;
    }

    async send() {
      if (!this.audio.blob) return;
      this.status.isProcessing = true;

      const formData = new FormData();
      formData.append('file', this.audio.blob, this.audio.name || 'audio.webm');

      try {
        const response = await fetch('http://localhost:8000/analyze/semantic', { 
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error(`Server responded with status: ${response.status}`);
        }

        const data: CriteriaContextData = await response.json();

        this.messages = data.all_messages;
        this.criterias = data.criterias;

        this.clearAudio();
      } catch (error) {
        console.error("Upload failed:", error);
      } finally {
        this.status.isProcessing = false;
      }
    }
  }

  const session = new SessionData();
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
            <div class="placeholder-card">
              <p class="placeholder-title">Awaiting Audio</p>
              <p class="placeholder-text">Semantic and acoustic metrics will appear here</p>
            </div>
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

  /* --- NEW CHAT STYLES --- */
  .message-wrapper {
    display: flex;
    width: 100%;
  }

  .message-wrapper.user {
    justify-content: flex-end; /* Push user message to the right */
  }

  .message-wrapper.bot {
    justify-content: flex-start; /* Push bot message to the left */
  }

  .message-bubble {
    max-width: 80%;
    padding: 0.75rem 1rem;
    border-radius: 12px;
    font-size: 0.95rem;
    line-height: 1.5;
    word-break: break-word;
  }

  /* User Bubble Styling */
  .message-wrapper.user .message-bubble {
    background-color: #2563eb; /* Blue */
    color: #ffffff;
    border-bottom-right-radius: 4px; /* Flattens the bottom-right corner slightly */
  }

  /* Bot Bubble Styling */
  .message-wrapper.bot .message-bubble {
    background-color: #262626; /* Dark gray */
    color: #e5e5e5;
    border-bottom-left-radius: 4px; /* Flattens the bottom-left corner slightly */
  }
  /* ----------------------- */

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
</style>