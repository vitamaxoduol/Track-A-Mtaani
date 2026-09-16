"use strict";

// All project facts and citations come from the backend's reviewed records.
// Session identifiers and chat history stay in page memory only.
const form = document.querySelector("#chat-form");
const question = document.querySelector("#question");
const conversation = document.querySelector("#conversation");
const status = document.querySelector("#status");
const sendButton = document.querySelector("#send");
const retryButton = document.querySelector("#retry");
let sessionId = null;
let language = "en";
const t = (text) => language === "sw" ? (SW_UI[text] || text) : text;
// Cache only static interface text; never rewrite conversation history or evidence.
const staticText = [];
const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
while (walker.nextNode()) {
  const node = walker.currentNode;
  if (Object.hasOwn(SW_UI, node.textContent)) staticText.push([node, node.textContent]);
}
function updateLanguage(value) {
  language = value;
  document.documentElement.lang = value;
  for (const [node, original] of staticText) node.textContent = t(original);
  question.placeholder = t("Ask about projects in your area…");
  sendButton.setAttribute("aria-label", t("Send question"));
  document.querySelectorAll("[data-language]").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.language === value)));
}
let busy = false;
let retryAction = null;

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

function sourceLink(label, href) {
  const link = element("a", "source-link", label);
  try {
    const url = new URL(href);
    if (url.protocol !== "https:" || !url.hostname.endsWith(".go.ke") || url.username || url.password) throw new Error("Invalid source");
    link.href = url.href;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.setAttribute("aria-label", `${label} (opens official document in a new tab)`);
  } catch {
    return element("span", "project-meta", t("Source link unavailable. Please check the coverage information."));
  }
  return link;
}

function projectCard(project) {
  const card = element("article", "project-card");
  card.append(element("span", "project-category", project.spending_unit));
  card.append(element("h2", "", project.name));
  for (const observation of project.observations) {
    const amount = element("p", "project-amount");
    amount.append(element("strong", "", observation.formatted_amount), element("span", "amount-kind", t("Allocated")));
    card.append(amount, element("p", "project-meta", language === "sw" ? `Wadi ya ${project.ward} · Mwaka wa fedha ${observation.financial_year} · Bajeti iliyoidhinishwa` : `${project.ward} Ward · FY ${observation.financial_year} · Approved budget`));
    const citation = observation.citation;
    const source = element("div", "citation");
    source.append(element("span", "eyebrow", t("Official source")));
    source.append(sourceLink(`${citation.document_title} ↗`, citation.page_url));
    source.append(element("span", "source-page", language === "sw" ? `PDF ukurasa ${citation.pdf_page} · Ukurasa uliochapishwa ${citation.printed_page}` : `PDF page ${citation.pdf_page} · Printed page ${citation.printed_page}`));
    source.append(element("span", "source-page", t("Record reviewed: ") + citation.reviewed_date));
    card.append(source);
    const details = element("details");
    details.append(element("summary", "", t("View details & evidence")));
    details.append(element("p", "", t("Department: ") + project.department));
    details.append(element("p", "", t("Source column: ") + citation.amount_heading));
    const excerpt = element("blockquote", "evidence-excerpt", citation.excerpt);
    details.append(excerpt, element("p", "", t("Relevant source cells, with whitespace normalized. Open the source to inspect the complete row.")));
    card.append(details);
  }
  const explain = element("button", "choice", t("Explain this project"));
  explain.type = "button";
  explain.addEventListener("click", () => sendMessage({action: "explain", project_id: project.id}, t("Explain this project")));
  card.append(explain);
  return card;
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, { ...options, signal: AbortSignal.timeout(20000), cache: "no-store" });
  if (!response.ok) {
    let message = "We couldn't load a response. Your question has been kept; please try again.";
    if (response.status === 429) message = "The demo is busy. Please retry in one minute.";
    else if (response.status === 422 || response.status === 413) message = "Please enter a question of 1–1000 characters.";
    throw new Error(t(message));
  }
  return response.json();
}

function renderCoverage(coverage) {
  const container = document.querySelector("#coverage-sources");
  container.replaceChildren();
  for (const source of coverage.sources) {
    const row = element("p");
    row.append(sourceLink(source.title, source.url));
    row.append(element("span", "source-page", t(source.used_for_answers ? "Used for project answers" : "Registered only; not yet used for answers")));
    container.append(row);
  }
}

function setBusy(value) {
  busy = value;
  sendButton.disabled = value;
  document.querySelectorAll("[data-language]").forEach(button => { button.disabled = value; });
  question.readOnly = value;
  form.setAttribute("aria-busy", String(value));
  conversation.querySelectorAll("button").forEach((button) => { button.disabled = value || button.dataset.expired === "true"; });
}

async function sendMessage(payload, displayText) {
  if (busy) return;
  setBusy(true);
  retryButton.hidden = true;
  status.textContent = t("Checking available records…");
  retryAction = () => sendMessage(payload, displayText);
  try {
    const result = await fetchJson("/api/v1/chat", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ language, ...payload, session_id: sessionId }),
    });
    sessionId = result.session_id;
    updateLanguage(result.language);
    document.querySelector("#welcome").hidden = true;
    conversation.hidden = false;
    // Old action controls must not target a newer conversation search.
    conversation.querySelectorAll("button").forEach((button) => { button.dataset.expired = "true"; });
    const userMessage = element("div", "message message-user");
    userMessage.append(element("p", "", displayText));
    conversation.append(userMessage);
    const reply = element("div", "message message-assistant");
    reply.append(element("span", "assistant-label", "Track-A-Mtaani"));
    if (result.review_notice) reply.append(element("p", "coverage-reminder", result.review_notice));
    if (result.verification) reply.dataset.verdict = result.verification.verdict;
    reply.append(element("p", result.verification ? "verification-message" : "", result.message));
    for (const source of result.explanation_sources) {
      reply.append(sourceLink(`${source.title} · PDF ${source.pdf_page}`, `${source.url}#page=${source.pdf_page}`));
    }
    result.projects.forEach((project) => reply.append(projectCard(project)));
    if (result.disclaimer) reply.append(element("p", "trust-note", result.disclaimer));
    if (result.projects.length) reply.append(element("p", "coverage-reminder", t(result.coverage.statement)));
    if (result.review_context) reply.append(element("p", "coverage-reminder", result.review_context));
    if (result.next_steps) reply.append(element("p", "trust-note next-steps", result.next_steps));
    if (result.choices.length) {
      const choices = element("div", "choices");
      result.choices.forEach((choice) => {
        const button = element("button", "choice", choice);
        button.type = "button";
        button.addEventListener("click", () => sendMessage({ message: choice }, choice));
        choices.append(button);
      });
      reply.append(choices);
    }
    if (result.has_more) {
      const more = element("button", "choice", t("Show more projects ↓"));
      more.type = "button";
      more.addEventListener("click", () => sendMessage({ action: "more" }, t("Show more projects")));
      reply.append(more);
    }
    if (result.kind === "coverage") {
      for (const source of result.coverage.sources) reply.append(sourceLink(source.title, source.url));
    }
    conversation.append(reply);
    renderCoverage(result.coverage);
    if (result.kind !== "expired") question.value = "";
    question.style.height = "auto";
    status.textContent = result.projects.length ? (language === "sw" ? `Jibu liko tayari. Kadi ${result.projects.length} za miradi zina viungo vya vyanzo.` : `Response ready. ${result.projects.length} project cards with source links are available.`) : result.message;
    reply.scrollIntoView({ behavior: "instant", block: "start" });
    retryAction = null;
  } catch (error) {
    status.textContent = error.name === "TimeoutError" ? t("The request took too long. Your question has been kept; please try again.") : error.message === "Failed to fetch" ? t("Unable to reach the application. Check your connection and try again.") : error.message;
    retryButton.hidden = false;
  } finally {
    setBusy(false);
    question.focus({ preventScroll: true });
  }
}

retryButton.addEventListener("click", () => { if (!busy && retryAction) retryAction(); });

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => {
    if (busy) return;
    question.value = language === "sw" ? ({"What projects are planned in Wamagana?": "Ni miradi gani imepangwa Wamagana?", "Explain allocation": "Eleza mgao wa bajeti", "Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved allocation KSh 3,000,000": "Hakiki Kianjogu Karaihu katika Wamagana mwaka wa fedha 2026/2027 iliyoidhinishwa mgao KSh 3,000,000"}[button.dataset.prompt] || button.dataset.prompt) : button.dataset.prompt;
    question.focus();
    question.dispatchEvent(new Event("input"));
  });
});

question.addEventListener("input", () => {
  question.style.height = "auto";
  question.style.height = `${Math.min(question.scrollHeight, 140)}px`;
});
question.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    if (!busy) form.requestSubmit();
  }
});
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = question.value.trim();
  if (!text) {
    status.textContent = t("Type a question or choose a suggested question.");
    question.focus();
    return;
  }
  sendMessage({ message: text }, text);
});

async function loadCoverage() {
  try {
    renderCoverage(await fetchJson("/api/v1/coverage"));
    if (!busy && retryAction === loadCoverage) {
      status.textContent = "";
      retryButton.hidden = true;
      retryAction = null;
    }
  } catch {
    if (!busy && !retryAction) {
      status.textContent = t("Coverage could not be loaded. Check that the application is running and try again.");
      retryAction = loadCoverage;
      retryButton.hidden = false;
    }
  }
}
loadCoverage();

document.querySelectorAll("[data-language]").forEach(button => {
  button.addEventListener("click", () => sendMessage({action: "language", language: button.dataset.language}, button.dataset.language.toUpperCase()));
});
