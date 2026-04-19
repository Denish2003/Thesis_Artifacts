(function initConversationSaver() {
  const STORAGE_KEY = "savedConversations";

  function normalizeWhitespace(text) {
    return text
      .replace(/\u00a0/g, " ")
      .replace(/\r\n/g, "\n")
      .replace(/\n{3,}/g, "\n\n")
      .trim();
  }

  function indentLines(text, prefix) {
    return text
      .split("\n")
      .map((line) => (line ? `${prefix}${line}` : prefix.trimEnd()))
      .join("\n");
  }

  function escapeInlineCode(text) {
    return text.replace(/`/g, "\\`");
  }

  function escapeMarkdownLinkText(text) {
    return text.replace(/\[/g, "\\[").replace(/\]/g, "\\]");
  }

  function convertChildrenToMarkdown(node, context = {}) {
    return Array.from(node.childNodes)
      .map((child) => convertNodeToMarkdown(child, context))
      .join("");
  }

  function convertListItemToMarkdown(node, context, index) {
    const listType = context.listType || "ul";
    const depth = context.depth || 0;
    const indent = "  ".repeat(depth);
    const marker = listType === "ol" ? `${index + 1}. ` : "- ";
    const parts = [];

    Array.from(node.childNodes).forEach((child) => {
      if (child.nodeType === Node.ELEMENT_NODE) {
        const tagName = child.tagName.toLowerCase();
        if (tagName === "ul" || tagName === "ol") {
          const nested = convertNodeToMarkdown(child, {
            depth: depth + 1,
            listType: tagName
          }).trimEnd();
          if (nested) {
            parts.push(`\n${nested}`);
          }
          return;
        }
      }

      parts.push(convertNodeToMarkdown(child, context));
    });

    const content = parts.join("").trim();
    if (!content) {
      return "";
    }

    const lines = content.split("\n");
    const firstLine = `${indent}${marker}${lines[0]}`;
    const rest = lines
      .slice(1)
      .map((line) => `${indent}  ${line}`)
      .join("\n");

    return rest ? `${firstLine}\n${rest}\n` : `${firstLine}\n`;
  }

  function convertNodeToMarkdown(node, context = {}) {
    if (!node) {
      return "";
    }

    if (node.nodeType === Node.TEXT_NODE) {
      return (node.textContent || "").replace(/\u00a0/g, " ");
    }

    if (node.nodeType !== Node.ELEMENT_NODE) {
      return "";
    }

    const element = node;
    const tagName = element.tagName.toLowerCase();

    if (tagName === "pre") {
      const languageSource =
        element.querySelector("code")?.className ||
        element.getAttribute("data-language") ||
        "";
      const languageMatch = languageSource.match(/language-([a-z0-9+-]+)/i);
      const language = languageMatch?.[1] || "";
      const codeText = element.innerText.replace(/\n+$/, "");
      return `\n\`\`\`${language}\n${codeText}\n\`\`\`\n`;
    }

    if (tagName === "code" && element.closest("pre")) {
      return "";
    }

    if (tagName === "code") {
      return `\`${escapeInlineCode(element.textContent || "")}\``;
    }

    if (tagName === "br") {
      return "\n";
    }

    if (tagName === "hr") {
      return "\n---\n";
    }

    if (tagName === "strong" || tagName === "b") {
      return `**${convertChildrenToMarkdown(element, context)}**`;
    }

    if (tagName === "em" || tagName === "i") {
      return `*${convertChildrenToMarkdown(element, context)}*`;
    }

    if (tagName === "del" || tagName === "s") {
      return `~~${convertChildrenToMarkdown(element, context)}~~`;
    }

    if (tagName === "a") {
      const label = escapeMarkdownLinkText(
        normalizeWhitespace(convertChildrenToMarkdown(element, context)) || element.href || ""
      );
      const href = element.href || "";
      return href ? `[${label}](${href})` : label;
    }

    if (tagName === "img") {
      const alt = escapeMarkdownLinkText(element.getAttribute("alt") || "image");
      const src = element.getAttribute("src") || "";
      return src ? `![${alt}](${src})` : alt;
    }

    if (tagName === "li") {
      return convertListItemToMarkdown(element, context, context.itemIndex || 0);
    }

    if (tagName === "ul" || tagName === "ol") {
      const items = Array.from(element.children)
        .filter((child) => child.tagName.toLowerCase() === "li")
        .map((child, index) =>
          convertNodeToMarkdown(child, {
            ...context,
            listType: tagName,
            itemIndex: index
          })
        )
        .join("");
      return `${items}\n`;
    }

    let text = convertChildrenToMarkdown(element, context);

    if (tagName === "p") {
      text += "\n\n";
    } else if (/^h[1-6]$/.test(tagName)) {
      const level = Number(tagName[1]);
      text = `${"#".repeat(level)} ${normalizeWhitespace(text)}\n\n`;
    } else if (tagName === "blockquote") {
      text = `${indentLines(normalizeWhitespace(text), "> ")}\n\n`;
    } else if (tagName === "table") {
      text = `${element.innerText.trim()}\n\n`;
    } else if (tagName === "thead" || tagName === "tbody" || tagName === "tr") {
      return text;
    } else if (tagName === "th" || tagName === "td") {
      return normalizeWhitespace(text);
    } else if (tagName === "div" || tagName === "section" || tagName === "article") {
      const hasBlockChildren = Array.from(element.children).some((child) =>
        ["P", "PRE", "UL", "OL", "BLOCKQUOTE", "H1", "H2", "H3", "H4", "H5", "H6", "TABLE"].includes(child.tagName)
      );
      if (hasBlockChildren) {
        text += "\n";
      }
    } else if (tagName === "span") {
      return text;
    } else if (tagName === "sup" || tagName === "sub") {
      return text;
    } else if (/^h[1-6]$/.test(tagName)) {
      text = `${normalizeWhitespace(text)}\n\n`;
    }

    return text;
  }

  function findConversationTitle() {
    const titleCandidates = [
      document.querySelector("nav a[aria-current='page']"),
      document.querySelector("header h1"),
      document.querySelector("main h1"),
      document.querySelector("h1")
    ];

    for (const candidate of titleCandidates) {
      const text = normalizeWhitespace(candidate?.textContent || "");
      if (text) {
        return text;
      }
    }

    return document.title
      .replace(/\s*[-|]\s*ChatGPT.*$/i, "")
      .replace(/\s*[-|]\s*OpenAI.*$/i, "")
      .trim() || "Untitled Conversation";
  }

  function detectRole(messageNode) {
    const explicitRole =
      messageNode.getAttribute("data-message-author-role") ||
      messageNode.dataset?.messageAuthorRole ||
      "";

    if (explicitRole === "user" || explicitRole === "assistant") {
      return explicitRole;
    }

    const labelText = (
      messageNode.getAttribute("aria-label") ||
      messageNode.textContent ||
      ""
    ).slice(0, 200);

    if (/^you said/i.test(labelText) || /\buser\b/i.test(labelText)) {
      return "user";
    }

    return "assistant";
  }

  function findMessageTextNode(messageNode) {
    const selectors = [
      "[data-message-content]",
      "[data-testid='conversation-turn-content']",
      ".markdown",
      ".prose",
      "[class*='markdown']"
    ];

    for (const selector of selectors) {
      const match = messageNode.querySelector(selector);
      if (match) {
        return match;
      }
    }

    return messageNode;
  }

  function getMessageNodes() {
    const selectors = [
      "[data-message-author-role]",
      "article[data-testid*='conversation-turn']",
      "main article"
    ];

    for (const selector of selectors) {
      const nodes = Array.from(document.querySelectorAll(selector));
      if (nodes.length) {
        return nodes.filter((node) => {
          const text = normalizeWhitespace(node.innerText || "");
          return Boolean(text);
        });
      }
    }

    return [];
  }

  function scrapeConversation() {
    const title = findConversationTitle();
    const rawNodes = getMessageNodes();

    const messages = rawNodes
      .map((node) => {
        const role = detectRole(node);
        const textNode = findMessageTextNode(node);
        const markdown = normalizeWhitespace(convertNodeToMarkdown(textNode));
        if (!markdown) {
          return null;
        }

        return { role, markdown };
      })
      .filter(Boolean);

    if (!messages.length) {
      throw new Error("No conversation messages found on the page.");
    }

    return {
      title,
      savedAt: new Date().toISOString(),
      url: window.location.href,
      messages
    };
  }

  async function getSavedConversations() {
    const result = await chrome.storage.local.get(STORAGE_KEY);
    return Array.isArray(result[STORAGE_KEY]) ? result[STORAGE_KEY] : [];
  }

  function buildConversationSignature(conversation) {
    return JSON.stringify({
      title: conversation.title,
      url: conversation.url,
      messages: conversation.messages
    });
  }

  function findExistingConversationIndex(savedConversations, conversation) {
    const signature = buildConversationSignature(conversation);

    return savedConversations.findIndex((savedConversation) => {
      if (savedConversation.url && conversation.url && savedConversation.url === conversation.url) {
        return true;
      }

      return buildConversationSignature(savedConversation) === signature;
    });
  }

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message?.type !== "SCRAPE_AND_SAVE_CONVERSATION") {
      return false;
    }

    (async () => {
      try {
        const conversation = scrapeConversation();
        const savedConversations = await getSavedConversations();
        const existingIndex = findExistingConversationIndex(savedConversations, conversation);

        if (existingIndex >= 0) {
          savedConversations[existingIndex] = {
            ...savedConversations[existingIndex],
            ...conversation
          };
        } else {
          savedConversations.push(conversation);
        }

        await chrome.storage.local.set({ [STORAGE_KEY]: savedConversations });
        sendResponse({
          ok: true,
          conversationTitle: conversation.title,
          count: savedConversations.length,
          wasDuplicate: existingIndex >= 0
        });
      } catch (error) {
        sendResponse({
          ok: false,
          error: error?.message || "Failed to save conversation."
        });
      }
    })();

    return true;
  });
})();
