const STORAGE_KEY = "savedConversations";

const saveButton = document.getElementById("saveButton");
const downloadButton = document.getElementById("downloadButton");
const countLabel = document.getElementById("countLabel");
const statusLabel = document.getElementById("status");

function setStatus(message, kind = "info") {
  statusLabel.textContent = message;
  statusLabel.dataset.kind = kind;
}

function createDataUrl(payload) {
  const json = JSON.stringify(payload, null, 2);
  return `data:application/json;charset=utf-8,${encodeURIComponent(json)}`;
}

async function getSavedConversations() {
  const result = await chrome.storage.local.get(STORAGE_KEY);
  return Array.isArray(result[STORAGE_KEY]) ? result[STORAGE_KEY] : [];
}

async function refreshCount() {
  const conversations = await getSavedConversations();
  countLabel.textContent = `Saved conversations: ${conversations.length}`;
  return conversations;
}

async function getActiveChatGptTab() {
  const tabs = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  const [tab] = tabs;
  if (!tab?.id || !tab.url) {
    throw new Error("No active tab found.");
  }

  const isChatGpt =
    tab.url.startsWith("https://chatgpt.com/") ||
    tab.url.startsWith("https://chat.openai.com/");

  if (!isChatGpt) {
    throw new Error("Open a ChatGPT conversation tab first.");
  }

  return tab;
}

async function saveCurrentConversation() {
  const tab = await getActiveChatGptTab();
  let response;

  try {
    response = await chrome.tabs.sendMessage(tab.id, {
      type: "SCRAPE_AND_SAVE_CONVERSATION"
    });
  } catch (error) {
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ["content.js"]
    });

    response = await chrome.tabs.sendMessage(tab.id, {
      type: "SCRAPE_AND_SAVE_CONVERSATION"
    });
  }

  if (!response?.ok) {
    throw new Error(response?.error || "Failed to save conversation.");
  }

  await refreshCount();
  setStatus(`Saved "${response.conversationTitle}".`, "success");
}

async function downloadSavedConversations() {
  const conversations = await getSavedConversations();
  if (!conversations.length) {
    setStatus("No saved conversations to download.", "info");
    return;
  }

  const response = await chrome.runtime.sendMessage({
    type: "DOWNLOAD_CONVERSATIONS",
    dataUrl: createDataUrl({ conversations })
  });

  if (!response?.ok) {
    throw new Error(response?.error || "Download failed.");
  }

  await chrome.storage.local.remove(STORAGE_KEY);
  await refreshCount();
  setStatus(`Downloaded ${conversations.length} conversation(s).`, "success");
}

saveButton.addEventListener("click", async () => {
  try {
    setStatus("Saving conversation...");
    await saveCurrentConversation();
  } catch (error) {
    setStatus(error?.message || "Unable to save conversation.", "error");
  }
});

downloadButton.addEventListener("click", async () => {
  try {
    setStatus("Preparing download...");
    await downloadSavedConversations();
  } catch (error) {
    setStatus(error?.message || "Unable to download conversations.", "error");
  }
});

refreshCount().catch(() => {
  setStatus("Unable to read saved conversations.", "error");
});
