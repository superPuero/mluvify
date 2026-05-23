  <script lang="ts">
    import AudioRecorder from '$lib/components/AudioRecorder.svelte';
    import AudioUploader from '$lib/components/AudioUploader.svelte';
    import Button from '$lib/components/Button.svelte';
  //   import LiveTranscript from '$lib/components/LiveTranscript.svelte';
  //   import ChatMessage from '$lib/components/ChatMessage.svelte';
  //   import StatsCard from '$lib/components/StatsCard.svelte';

    let messages = $state([])
    let criterias = $state({})
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
            
            <!-- Chat Messages Area -->   
            <div class="chat-messages">
              <!-- Example placeholder for messages -->
              <div class="message system">
                Awaiting audio input to begin analysis...
              </div>
            </div>

            <!-- Input Area (Audio Components) -->
            <div class="chat-input-area">
              <Button label="send"/>
              <AudioRecorder />
              <AudioUploader />
              <!-- <LiveTranscript /> -->
            </div>
          </div>
        </div>

        <!-- Right Column: Evaluation Statistics -->
        <div class="column">
          <div class="panel stats-panel">
            <div class="panel-header">
              <h2>Evaluation Statistics</h2>
            </div>
            
            <div class="stats-content">
              <!-- Placeholder until data arrives -->
              <div class="placeholder-card">
                <p class="placeholder-title">Awaiting Audio</p>
                <p class="placeholder-text">Semantic and acoustic metrics will appear here</p>
              </div>

              <!-- Example of how stats might look once populated:
              <div class="stat-group">
                <h3>Vocal Biomarkers</h3>
                ...
              </div>
              -->
            </div>
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
      /* Widened from 1000px to 1200px to better support a dual-pane layout */
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
      /* Sets a fixed height so the chat can scroll internally */
      height: calc(100vh - 180px);
      min-height: 500px;
    }

    /* Desktop layout - splitting the grid */
    @media (min-width: 768px) {
      .grid-layout {
        /* Gives slightly more room to the chat (60/40 split) */
        grid-template-columns: 3fr 2fr;
      }
    }

    .column {
      display: flex;
      flex-direction: column;
      height: 100%;
    }

    /* Shared Panel Styling */
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

    /* Chat Specific Styling */
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

    .chat-input-area {
      padding: 1.25rem;
      border-top: 1px solid #262626;
      background-color: #121212;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    /* Stats Specific Styling */
    .stats-content {
      flex: 1;
      padding: 1.25rem;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
    }

    /* Placeholder Styling */
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