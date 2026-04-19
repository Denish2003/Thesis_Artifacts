# Data Donation Platform

This repository contains the implementation and thesis materials for a research project on emotionally meaningful human-AI interaction. The main software artifact is a Streamlit-based data donation platform that allows participants to upload conversation logs, review them, redact sensitive content, and optionally donate a cleaned dataset for research. 

## Repository Overview

The project is organized into:

- `main.py`, `_pages/`, and `components/` contain the Streamlit application.

At a high level, the application supports the following workflow:

1. Present study information and informed consent.
2. Accept uploaded conversation data from either ChatGPT exports or the custom browser extension format.
3. Normalize uploaded conversations into a common internal review representation.
4. Let participants search, inspect, exclude, and redact content before sharing.
5. Allow participants to export a cleaned JSON file or donate the cleaned payload.

## Application Structure

### Entry Point

- `main.py`
  - Configures the Streamlit app.
  - Initializes session state.
  - Applies global styling.
  - Renders the sidebar action panel.
  - Routes between the home, consent, instructions, upload, chat list, and chat detail pages.

### Pages

- `_pages/home.py`
  - Landing page and initial call to the consent flow.
- `_pages/consent.py`
  - Participant consent interface.
- `_pages/instructions.py`
  - Workflow instructions and upload guidance.
- `_pages/upload.py`
  - JSON/ZIP upload and schema detection.
- `_pages/chat_list.py`
  - Search, month filtering, chat exclusion, and navigation into detail view.
- `_pages/chat_details.py`
  - Message-level review, PII highlighting, and redaction.
- `_pages/reminder_modal.py`
  - Optional reminder email collection for users waiting on exports.

### Shared Components

- `components/chat_schema.py`
  - Accepts both supported conversation schemas.
  - Normalizes uploaded data into a shared review model.
  - Writes redactions back into the original schema shape.
- `components/state.py`
  - Defines session-state defaults and reset helpers.
- `components/sidebar.py`
  - Renders navigation, cleaned export, and donation actions.
- `components/ui.py`
  - Reusable UI helpers for headers, cards, stats, and notices.
- `components/styles.py`
  - Global CSS for layout and visual design.
- `components/PII.py`
  - Lightweight regex- and rule-based PII detection.
- `components/save_data_to_VM.py`
  - File-based persistence for donated datasets and reminder emails.
- `components/go_to_page.py`
  - Small helper for session-state-based page navigation.
- `components/types.py`
  - Shared type definitions used across the app.

## Supported Input Formats

The platform currently supports two upload formats.

### 1. Legacy ChatGPT Export Format

This is the original `conversations.json` export format used by ChatGPT. Internally, it stores each conversation as a graph-like `mapping` structure with nested message objects.

### 2. Custom Extension Format

This is the simplified format produced by the project’s browser extension:

```json
{
  "conversations": [
    {
      "title": "...",
      "savedAt": "...",
      "url": "...",
      "messages": [
        {
          "role": "user",
          "markdown": "..."
        },
        {
          "role": "assistant",
          "markdown": "..."
        }
      ]
    }
  ]
}
```

The platform preserves the original schema style when exporting cleaned data.

## Running the App

### Prerequisites

- Python 3.11+ recommended
- `pip`

### Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Start the Streamlit App

```bash
streamlit run main.py
```

If you are using the repository’s local virtual environment, you can also run:

```bash
./venv/bin/streamlit run main.py
```

## Data Handling Model

The platform is designed around participant review and control.

- Uploaded files are first processed within the active Streamlit session.
- Participants can inspect conversations before any donation occurs.
- Chats can be excluded from the cleaned export without immediate permanent deletion.
- Messages can be fully redacted or selectively redacted.
- Donated data are stored as timestamped JSON files through a file-based persistence layer.

The current implementation uses lightweight PII detection as an assistive review tool. It should not be interpreted as a guarantee of complete anonymization.

## Storage

The application currently writes data to local directories on the host machine:

- Donated datasets are stored under `~/data_donations`
- Reminder emails are stored under `~/email_reminders`

In the thesis deployment model, this host machine is an Azure Virtual Machine running the Streamlit application.
