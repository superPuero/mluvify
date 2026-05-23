<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    label,
    meta = '',
    loadingText = 'Processing...',
    isLoading = false,
    disabled = false,
    type = 'button',
    icon,
    onclick
  }: {
    label: string;
    meta?: string;
    loadingText?: string;
    isLoading?: boolean;
    disabled?: boolean;
    type?: 'button' | 'submit' | 'reset';
    icon?: Snippet;
    onclick?: (e: MouseEvent) => void;
  } = $props();
</script>

<button
  {type}
  class="compact-button {isLoading ? 'loading' : ''}"
  disabled={isLoading || disabled}
  {onclick}
>
  {#if isLoading}
    <div class="spinner"></div>
    <span class="status truncate">{loadingText}</span>
  {:else}
    <!-- Render the custom icon snippet if provided -->
    {#if icon}
      {@render icon()}
    {/if}
    
    <span class="status">
      {label}
      {#if meta}
        <span class="meta">{meta}</span>
      {/if}
    </span>
  {/if}
</button>

<style>
  /* Reset default button styles */
  button {
    appearance: none;
    font-family: inherit;
    margin: 0;
  }

  /* Compact Container (matches your upload label) */
  .compact-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 0.5rem 0.75rem;
    background-color: #111;
    border: 1px solid #262626;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
    width: auto;
  }

  /* Hover state */
  .compact-button:hover:not(.loading):not(:disabled) {
    border-color: #404040;
    background-color: #171717;
  }

  /* Loading & Disabled States */
  .compact-button:disabled {
    cursor: not-allowed;
    background-color: rgba(23, 23, 23, 0.5);
  }

  .compact-button.loading {
    border-style: dashed;
  }

  /* Target SVGs passed via the icon snippet */
  :global(.compact-button > svg) {
    color: #a3a3a3;
    flex-shrink: 0;
    width: 16px;
    height: 16px;
  }

  /* Text styling */
  .status {
    font-size: 0.8125rem; /* 13px */
    color: #e5e5e5;
    white-space: nowrap;
  }

  /* Secondary text */
  .meta {
    color: #737373;
    font-size: 0.75rem;
    margin-left: 0.25rem;
  }

  /* Helper for long text */
  .truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 120px;
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