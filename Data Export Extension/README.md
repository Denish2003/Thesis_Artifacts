# Data Export Extension

A Google Chrome extension built with Manifest V3 that lets you save conversations from the ChatGPT web app, keep them locally in browser storage, and export them as JSON.

The extension uses a side panel UI, scrapes the currently open ChatGPT conversation from the page DOM, reconstructs message content as Markdown, prevents duplicate saves, and downloads the accumulated data as a JSON file.

## Features

- Save the currently open ChatGPT conversation from `chatgpt.com` or `chat.openai.com`
- Extract the conversation title and all messages in order
- Store messages as reconstructed Markdown to better preserve formatting
- Handle code blocks, inline code, headings, lists, blockquotes, links, and line breaks
- Prevent duplicate saves by matching on conversation URL and content signature
- Export all saved conversations as a single JSON file
- Clear saved conversations from local storage after download
- Use a persistent Chrome side panel instead of a popup

## How It Works

The extension is organized into three main parts:

- `content.js`
  Scrapes the ChatGPT conversation page DOM, identifies message roles, converts rendered HTML into Markdown, and writes deduplicated conversation objects into `chrome.storage.local`.

- `sidepanel.html`, `sidepanel.css`, `sidepanel.js`
  Provide the user-facing interface for saving the current conversation and downloading the saved conversation set.

- `background.js`
  Configures side panel behavior and handles privileged browser operations such as file downloads.

## Project Structure

```text
.
├── background.js
├── content.js
├── icons/
│   ├── icon-16.png
│   ├── icon-32.png
│   ├── icon-48.png
│   ├── icon-128.png
│   ├── icon-source.png
│   └── icon.svg
├── manifest.json
├── README.md
├── sidepanel.css
├── sidepanel.html
└── sidepanel.js
```

Note:
Legacy `popup.*` files are still present in the repository from an earlier iteration, but the active extension UI is the side panel declared in `manifest.json`.

## Installation

### Load as an unpacked extension

1. Clone or download this repository.
2. Open Chrome and go to `chrome://extensions`.
3. Enable `Developer mode`.
4. Click `Load unpacked`.
5. Select the project folder.

After loading, Chrome will add the extension and its icon to the toolbar.

## Usage

1. Open a conversation on:
   - `https://chatgpt.com`
   - `https://chat.openai.com`
2. Click the extension icon to open the side panel.
3. Click `Save Current Conversation`.
4. Repeat this for any other conversations you want to collect.
5. Click `Download Saved Conversations` when you want to export them.

The exported file is downloaded as JSON in the format:

```json
{
  "conversations": [
    {
      "title": "Example conversation",
      "savedAt": "2026-04-19T12:00:00.000Z",
      "url": "https://chatgpt.com/c/...",
      "messages": [
        {
          "role": "user",
          "markdown": "Hello"
        },
        {
          "role": "assistant",
          "markdown": "Hi there"
        }
      ]
    }
  ]
}
```

## Permissions

The extension uses the following Chrome permissions:

- `storage`
  Stores saved conversations in `chrome.storage.local`

- `downloads`
  Triggers JSON file downloads

- `tabs`
  Accesses the active tab to verify that it is a ChatGPT page

- `scripting`
  Injects the content script into the current tab if needed

- `sidePanel`
  Enables the Chrome side panel interface

Host permissions are limited to:

- `https://chatgpt.com/*`
- `https://chat.openai.com/*`

## Architecture Summary

### 1. Side Panel Layer

The side panel is the extension’s control surface. It allows the user to initiate a save or export action, shows a running count of saved conversations, and reports success or error states.

### 2. Content Script Layer

The content script runs inside the ChatGPT page and has direct access to the rendered DOM. It:

- locates the conversation title
- finds conversation turn elements
- determines the role for each message
- reconstructs message content as Markdown
- deduplicates conversations before storing them

### 3. Background Service Worker Layer

The service worker receives export requests and uses the Chrome Downloads API to generate the output file. It also configures the extension action so that clicking the toolbar icon opens the side panel.

## Duplicate Prevention

To avoid storing the same conversation more than once, the extension:

1. checks whether a saved conversation already has the same URL
2. falls back to comparing a serialized signature of:
   - title
   - URL
   - message list

If a duplicate is found, the saved entry is updated instead of appending a new copy.

## Markdown Reconstruction

ChatGPT renders responses as HTML in the browser. This extension converts that rendered structure back into Markdown-like text so the export is more useful for archival, analysis, or regeneration workflows.

It currently handles:

- fenced code blocks
- inline code
- bold and italics
- headings
- ordered and unordered lists
- blockquotes
- links
- images
- line breaks

Important:
Because the extension works from the rendered DOM, the exported Markdown is reconstructed rather than guaranteed to be byte-for-byte identical to the model’s original internal source formatting.

## Privacy

This project is fully client-side:

- no backend server is used
- no data is transmitted to external services by the extension
- conversations remain in local browser storage until exported or cleared
