async function configureSidePanelBehavior() {
  if (!chrome.sidePanel?.setPanelBehavior) {
    return;
  }

  try {
    await chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
  } catch (error) {
    console.error("Failed to configure side panel behavior.", error);
  }
}

chrome.runtime.onInstalled.addListener(() => {
  void configureSidePanelBehavior();
});

chrome.runtime.onStartup.addListener(() => {
  void configureSidePanelBehavior();
});

void configureSidePanelBehavior();

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type === "DOWNLOAD_CONVERSATIONS") {
    const dataUrl = message.dataUrl;
    if (!dataUrl) {
      sendResponse({ ok: false, error: "Missing data URL." });
      return false;
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const filename = `chatgpt-saved-conversations-${timestamp}.json`;

    chrome.downloads.download(
      {
        url: dataUrl,
        filename,
        saveAs: true
      },
      (downloadId) => {
        if (chrome.runtime.lastError) {
          sendResponse({
            ok: false,
            error: chrome.runtime.lastError.message
          });
          return;
        }

        sendResponse({ ok: true, downloadId });
      }
    );

    return true;
  }

  if (message?.type === "GET_SAVED_CONVERSATION_COUNT") {
    chrome.storage.local.get("savedConversations", (result) => {
      if (chrome.runtime.lastError) {
        sendResponse({ ok: false, error: chrome.runtime.lastError.message });
        return;
      }

      const conversations = Array.isArray(result.savedConversations)
        ? result.savedConversations
        : [];
      sendResponse({ ok: true, count: conversations.length });
    });

    return true;
  }

  return false;
});
