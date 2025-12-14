// Global state
let sessionId = null;
let userApiKey = null;
let welcomeMinimized = false;
// Global variable to store last search results
let lastSearchResults = null;

// ============================================================================
// API KEY HELPERS (Security: localStorage only, no logging)
// ============================================================================

function getUserApiKey() {
  return localStorage.getItem("researchforge_api_key") || "";
}

function setUserApiKey(apiKey) {
  localStorage.setItem("researchforge_api_key", apiKey);
}

function generateSessionId() {
  return "session_" + Math.random().toString(36).substr(2, 16);
}

// ============================================================================
// SCROLL FUNCTIONS
// ============================================================================

function scrollToSearch() {
  document.getElementById("search").scrollIntoView({ behavior: "smooth" });
  setTimeout(() => document.getElementById("searchQuery").focus(), 500);
}

function scrollToChat() {
  document.getElementById("chat").scrollIntoView({ behavior: "smooth" });
  setTimeout(() => document.getElementById("chatInput").focus(), 500);
}

// ============================================================================
// API KEY MANAGEMENT
// ============================================================================

function saveApiKey() {
  const apiKeyInput = document.getElementById("apiKeyInput");
  const apiKey = apiKeyInput.value.trim();

  if (!apiKey) {
    alert("⚠️ Please enter an API key");
    return;
  }

  if (!apiKey.startsWith("AIzaSy")) {
    alert('⚠️ Invalid API key format. Should start with "AIzaSy"');
    return;
  }

  const btn = document.getElementById("saveApiKeyBtn");
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Validating...';

  fetch("/api/set-api-key", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      api_key: apiKey,
      session_id: sessionId || "default",
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "success") {
        userApiKey = apiKey;
        setUserApiKey(apiKey);
        alert("✅ " + data.message);
        document.getElementById("apiKeySection").style.display = "none";
      } else {
        alert("❌ " + data.message);
        btn.disabled = false;
        btn.innerHTML = "Validate & Save";
      }
    })
    .catch((err) => {
      alert("❌ Error: " + err.message);
      btn.disabled = false;
      btn.innerHTML = "Validate & Save";
    });
}

// ============================================================================
// EXAMPLE QUERIES
// ============================================================================

function fillExample(text) {
  document.getElementById("chatInput").value = text;
  document.getElementById("chatInput").focus();
}

function runExample(exampleType) {
  let message = "";

  switch (exampleType) {
    case "find-papers":
      message =
        "Find recent research papers on renewable energy technology and sustainability";
      break;

    case "generate-proposal":
      message = "Generate a research proposal for AI in healthcare";
      break;

    case "build-profiles":
      message =
        "Find 5 papers about machine learning. After you find them, immediately build researcher profiles from ALL the authors in those papers. Show me both the papers and the profiles.";
      break;

    case "find-collaborators":
      message = "Find collaborators for natural language processing research";
      break;

    case "draft-email":
      message =
        "Draft a collaboration email to Dr. Sarah Chen about AI research";
      break;

    case "export-results":
      // Check if there are search results to export
      if (lastSearchResults && lastSearchResults.length > 0) {
        exportToBibTeX();
        return; // Don't send a message, just export
      } else {
        // No results yet, guide user to search first
        showNotification(
          "Please search for papers first, then use the Export button",
          "info"
        );
        message =
          "Search for papers on blockchain applications in healthcare, then I'll show you how to export them";
      }
      break;

    case "query-suggestions":
      message =
        "What are better search keywords I should use for quantum computing applications research?";
      break;

    case "breast-cancer":
      message =
        "Find papers about breast cancer detection using machine learning and medical imaging";
      break;

    case "healthcare-proposal":
      message =
        "Generate a complete research proposal for AI in healthcare focusing on medical imaging for disease detection";
      break;

    default:
      message = exampleType;
  }

  const chatInput = document.getElementById("chatInput");
  if (chatInput) {
    chatInput.value = message;
    sendMessage();
  }
}

// ============================================================================
// WELCOME STATE MANAGEMENT
// ============================================================================

function hideWelcomeState() {
  const welcomeState = document.getElementById("welcomeState");
  if (welcomeState) {
    welcomeState.innerHTML = `
      <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-4 mb-4 border border-indigo-200">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm font-semibold text-slate-700">
            <i class="fas fa-lightbulb text-yellow-500 mr-2"></i>Try more examples:
          </span>
          <button onclick="location.reload()" class="text-xs text-slate-500 hover:text-slate-700">
            <i class="fas fa-redo mr-1"></i>Reset
          </button>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
          <button onclick="runExample('breast-cancer')"
            class="px-3 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-xs font-medium transition shadow-sm hover:shadow-md flex items-center justify-center gap-1">
            <i class="fas fa-search text-xs"></i>
            <span>Papers</span>
          </button>
          
          <button onclick="runExample('healthcare-proposal')"
            class="px-3 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-lg text-xs font-medium transition shadow-sm hover:shadow-md flex items-center justify-center gap-1">
            <i class="fas fa-file-alt text-xs"></i>
            <span>Proposal</span>
          </button>
          
          <button onclick="runExample('build-profiles')"
            class="px-3 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-xs font-medium transition shadow-sm hover:shadow-md flex items-center justify-center gap-1">
            <i class="fas fa-user-plus text-xs"></i>
            <span>Profiles</span>
          </button>
          
          <button onclick="runExample('find-collaborators')"
            class="px-3 py-2 bg-rose-500 hover:bg-rose-600 text-white rounded-lg text-xs font-medium transition shadow-sm hover:shadow-md flex items-center justify-center gap-1">
            <i class="fas fa-users text-xs"></i>
            <span>Match</span>
          </button>
          
          <button onclick="runExample('draft-email')"
            class="px-3 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg text-xs font-medium transition shadow-sm hover:shadow-md flex items-center justify-center gap-1">
            <i class="fas fa-envelope text-xs"></i>
            <span>Email</span>
          </button>
          
          <button onclick="runExample('export-results')"
            class="px-3 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg text-xs font-medium transition shadow-sm hover:shadow-md flex items-center justify-center gap-1">
            <i class="fas fa-download text-xs"></i>
            <span>Export</span>
          </button>
          
          <button onclick="runExample('query-suggestions')"
            class="px-3 py-2 bg-violet-500 hover:bg-violet-600 text-white rounded-lg text-xs font-medium transition shadow-sm hover:shadow-md flex items-center justify-center gap-1">
            <i class="fas fa-lightbulb text-xs"></i>
            <span>Suggest</span>
          </button>
        </div>
      </div>
    `;
  }
}

function clearChat() {
  const chatMessages = document.getElementById("chatMessages");
  chatMessages.innerHTML = `
    <div id="welcomeState" class="text-center py-12">
      <div class="w-20 h-20 bg-indigo-50 rounded-full flex items-center justify-center mx-auto mb-5">
        <span class="text-3xl">⚛️</span>
      </div>

      <h4 class="text-2xl font-bold text-slate-800 mb-2">How can I help your research?</h4>
      <p class="text-slate-500 mb-6 max-w-md mx-auto text-sm">
        I can find papers, analyze trends, generate proposals, and draft collaboration emails.
      </p>

      <div class="space-y-2 max-w-2xl mx-auto">
        <!-- Example 1: Find Papers -->
        <button onclick="runExample('breast-cancer')"
          class="w-full p-3 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl hover:border-indigo-400 hover:shadow-lg transition-all duration-300 text-left group">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
              <i class="fas fa-search text-white text-sm"></i>
            </div>
            <div class="flex-1 min-w-0">
              <h5 class="text-sm font-bold text-slate-800 group-hover:text-indigo-600 transition-colors">
                🔬 Find Research Papers
              </h5>
              <p class="text-slate-600 text-xs truncate">
                Breast cancer detection using ML & medical imaging
              </p>
            </div>
            <i class="fas fa-arrow-right text-slate-400 group-hover:text-indigo-600 group-hover:translate-x-1 transition-all flex-shrink-0"></i>
          </div>
        </button>

        <!-- Example 2: Generate Proposal -->
        <button onclick="runExample('healthcare-proposal')"
          class="w-full p-3 bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-xl hover:border-purple-400 hover:shadow-lg transition-all duration-300 text-left group">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-purple-500 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
              <i class="fas fa-file-alt text-white text-sm"></i>
            </div>
            <div class="flex-1 min-w-0">
              <h5 class="text-sm font-bold text-slate-800 group-hover:text-purple-600 transition-colors">
                📝 Generate Research Proposal
              </h5>
              <p class="text-slate-600 text-xs truncate">
                AI applications in healthcare proposal
              </p>
            </div>
            <i class="fas fa-arrow-right text-slate-400 group-hover:text-purple-600 group-hover:translate-x-1 transition-all flex-shrink-0"></i>
          </div>
        </button>

        <!-- Example 3: Build Profiles -->
        <button onclick="runExample('build-profiles')"
          class="w-full p-3 bg-gradient-to-r from-amber-50 to-yellow-50 border border-amber-200 rounded-xl hover:border-amber-400 hover:shadow-lg transition-all duration-300 text-left group">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-amber-500 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
              <i class="fas fa-user-plus text-white text-sm"></i>
            </div>
            <div class="flex-1 min-w-0">
              <h5 class="text-sm font-bold text-slate-800 group-hover:text-amber-600 transition-colors">
                👤 Build Researcher Profiles
              </h5>
              <p class="text-slate-600 text-xs truncate">
                Extract researchers from quantum computing papers
              </p>
            </div>
            <i class="fas fa-arrow-right text-slate-400 group-hover:text-amber-600 group-hover:translate-x-1 transition-all flex-shrink-0"></i>
          </div>
        </button>

        <!-- Example 4: Find Collaborators -->
        <button onclick="runExample('find-collaborators')"
          class="w-full p-3 bg-gradient-to-r from-rose-50 to-red-50 border border-rose-200 rounded-xl hover:border-rose-400 hover:shadow-lg transition-all duration-300 text-left group">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-rose-500 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
              <i class="fas fa-users text-white text-sm"></i>
            </div>
            <div class="flex-1 min-w-0">
              <h5 class="text-sm font-bold text-slate-800 group-hover:text-rose-600 transition-colors">
                💞 Find Collaborators
              </h5>
              <p class="text-slate-600 text-xs truncate">
                Match me with AI ethics researchers
              </p>
            </div>
            <i class="fas fa-arrow-right text-slate-400 group-hover:text-rose-600 group-hover:translate-x-1 transition-all flex-shrink-0"></i>
          </div>
        </button>

        <!-- Example 5: Draft Email -->
        <button onclick="runExample('draft-email')"
          class="w-full p-3 bg-gradient-to-r from-cyan-50 to-sky-50 border border-cyan-200 rounded-xl hover:border-cyan-400 hover:shadow-lg transition-all duration-300 text-left group">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-cyan-500 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
              <i class="fas fa-envelope text-white text-sm"></i>
            </div>
            <div class="flex-1 min-w-0">
              <h5 class="text-sm font-bold text-slate-800 group-hover:text-cyan-600 transition-colors">
                ✉️ Draft Collaboration Email
              </h5>
              <p class="text-slate-600 text-xs truncate">
                Professional outreach to Dr. Garcia
              </p>
            </div>
            <i class="fas fa-arrow-right text-slate-400 group-hover:text-cyan-600 group-hover:translate-x-1 transition-all flex-shrink-0"></i>
          </div>
        </button>

        <!-- Example 6: Export -->
        <button onclick="runExample('export-results')"
          class="w-full p-3 bg-gradient-to-r from-emerald-50 to-green-50 border border-emerald-200 rounded-xl hover:border-emerald-400 hover:shadow-lg transition-all duration-300 text-left group">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-emerald-500 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
              <i class="fas fa-download text-white text-sm"></i>
            </div>
            <div class="flex-1 min-w-0">
              <h5 class="text-sm font-bold text-slate-800 group-hover:text-emerald-600 transition-colors">
                📊 Export Search Results
              </h5>
              <p class="text-slate-600 text-xs truncate">
                Download as JSON, CSV, or BibTeX
              </p>
            </div>
            <i class="fas fa-arrow-right text-slate-400 group-hover:text-emerald-600 group-hover:translate-x-1 transition-all flex-shrink-0"></i>
          </div>
        </button>

        <!-- Example 7: Query Suggestions -->
        <button onclick="runExample('query-suggestions')"
          class="w-full p-3 bg-gradient-to-r from-violet-50 to-purple-50 border border-violet-200 rounded-xl hover:border-violet-400 hover:shadow-lg transition-all duration-300 text-left group">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-violet-500 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
              <i class="fas fa-lightbulb text-white text-sm"></i>
            </div>
            <div class="flex-1 min-w-0">
              <h5 class="text-sm font-bold text-slate-800 group-hover:text-violet-600 transition-colors">
                💡 Get Query Suggestions
              </h5>
              <p class="text-slate-600 text-xs truncate">
                Improve your search with AI suggestions
              </p>
            </div>
            <i class="fas fa-arrow-right text-slate-400 group-hover:text-violet-600 group-hover:translate-x-1 transition-all flex-shrink-0"></i>
          </div>
        </button>
      </div>
    </div>
  `;

  sessionId = null;
  welcomeMinimized = false;
}

// ============================================================================
// MARKDOWN FORMATTER
// ============================================================================

function formatMarkdown(text) {
  let html = text;

  // 1. Markdown links [text](url)
  html = html.replace(
    /\[([^\]]+)\]\(([^\)]+)\)/g,
    '<a href="$2" target="_blank" class="text-blue-600 hover:text-purple-600 underline font-medium">$1 <i class="fas fa-external-link-alt text-xs"></i></a>'
  );

  // 2. Raw URLs (arXiv and others)
  html = html.replace(
    /(href="|src=")?(https?:\/\/[^\s"<>]+)/g,
    function (match, prefix, url) {
      if (prefix) return match;

      if (url.includes("arxiv.org/pdf/")) {
        return `<a href="${url}" target="_blank" class="inline-flex items-center gap-1 text-blue-600 hover:text-purple-600 underline font-medium"><i class="fas fa-file-pdf text-red-500"></i> View PDF <i class="fas fa-external-link-alt text-xs"></i></a>`;
      }
      return `<a href="${url}" target="_blank" class="text-blue-600 hover:text-purple-600 underline font-medium">${url} <i class="fas fa-external-link-alt text-xs ml-1"></i></a>`;
    }
  );

  // Headers
  html = html.replace(
    /^### (.*$)/gim,
    '<h3 class="text-xl font-bold text-indigo-700 mt-5 mb-3 border-l-4 border-indigo-500 pl-3">$1</h3>'
  );
  html = html.replace(
    /^## (.*$)/gim,
    '<h2 class="text-2xl font-bold text-purple-700 mt-6 mb-4 border-l-4 border-purple-500 pl-3">$1</h2>'
  );
  html = html.replace(
    /^# (.*$)/gim,
    '<h1 class="text-3xl font-bold text-slate-900 mt-8 mb-5 pb-2 border-b-2 border-slate-200">$1</h1>'
  );

  // Bold
  html = html.replace(
    /\*\*(.*?)\*\*/g,
    '<strong class="font-bold text-slate-900">$1</strong>'
  );

  // Italic
  html = html.replace(
    /\*(.*?)\*/g,
    '<em class="italic text-slate-700">$1</em>'
  );

  // Code blocks
  html = html.replace(
    /```(.*?)```/gs,
    '<pre class="bg-slate-800 text-green-400 p-4 rounded-xl my-4 overflow-x-auto"><code>$1</code></pre>'
  );

  // Inline code
  html = html.replace(
    /`(.*?)`/g,
    '<code class="bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded font-mono text-sm">$1</code>'
  );

  // Lists
  html = html.replace(
    /^\* (.*$)/gim,
    '<li class="ml-6 mb-2 pl-2 flex items-start gap-2"><span class="text-indigo-500 font-bold mt-1">•</span><span class="flex-1">$1</span></li>'
  );
  html = html.replace(
    /^- (.*$)/gim,
    '<li class="ml-6 mb-2 pl-2 flex items-start gap-2"><span class="text-purple-500 font-bold mt-1">•</span><span class="flex-1">$1</span></li>'
  );

  // Numbered lists
  html = html.replace(
    /^(\d+)\. (.*$)/gim,
    '<li class="ml-6 mb-3 pl-2 flex items-start gap-3"><span class="flex-shrink-0 w-6 h-6 bg-indigo-500 text-white rounded-full flex items-center justify-center text-xs font-bold">$1</span><span class="flex-1 pt-0.5">$2</span></li>'
  );

  // Wrap lists
  html = html.replace(
    /(<li class="ml-6[^>]*>.*?<\/li>\s*)+/g,
    '<ul class="space-y-1 my-4">$&</ul>'
  );

  // Line breaks
  html = html.replace(
    /\n\n/g,
    '</p><p class="mb-4 leading-relaxed text-slate-700">'
  );
  html = html.replace(/\n/g, "<br>");

  // Wrap in paragraph
  html =
    '<div class="prose prose-slate max-w-none"><p class="mb-4 leading-relaxed text-slate-700">' +
    html +
    "</p></div>";

  return html;
}

// ============================================================================
// CHAT FUNCTIONS
// ============================================================================

function addMessage(role, content, isRaw = false) {
  const chatMessages = document.getElementById("chatMessages");

  if (!welcomeMinimized) {
    const welcomeState = document.getElementById("welcomeState");
    if (welcomeState && welcomeState.querySelector(".text-2xl")) {
      hideWelcomeState();
      welcomeMinimized = true;
    }
  }

  const messageDiv = document.createElement("div");
  messageDiv.className = "message mb-4 max-w-4xl";

  if (role === "user") {
    messageDiv.classList.add("ml-auto");
    messageDiv.innerHTML = `
      <div class="message-user rounded-2xl px-6 py-4 shadow-lg" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <div class="flex items-start gap-3">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 rounded-full bg-white bg-opacity-20 flex items-center justify-center">
              <i class="fas fa-user text-sm"></i>
            </div>
          </div>
          <div class="flex-1">
            <div class="font-semibold mb-1 text-sm opacity-90">You</div>
            <div class="leading-relaxed">${escapeHtml(content)}</div>
          </div>
        </div>
      </div>
    `;
  } else if (role === "typing") {
    messageDiv.innerHTML = `
      <div class="message-ai rounded-2xl px-6 py-4 shadow-md bg-white border border-gray-200">
        <div class="flex items-start gap-3">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 flex items-center justify-center text-white text-sm">
              ⚛️
            </div>
          </div>
          <div class="flex-1">
            <div class="font-semibold mb-2 text-sm text-gray-700">ResearchForge AI</div>
            <div class="flex gap-1">
              <div class="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style="animation-delay: 0s"></div>
              <div class="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              <div class="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            </div>
          </div>
        </div>
      </div>
    `;
  } else {
    messageDiv.innerHTML = `
      <div class="message-ai rounded-2xl px-6 py-4 shadow-md bg-white border border-gray-200">
        <div class="flex items-start gap-3">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 flex items-center justify-center text-white text-sm">
              ⚛️
            </div>
          </div>
          <div class="flex-1">
            <div class="font-semibold mb-2 text-sm text-gray-700">ResearchForge AI</div>
            <div class="markdown-content text-gray-700">
              ${isRaw ? escapeHtml(content) : formatMarkdown(content)}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

async function sendMessage() {
  const input = document.getElementById("chatInput");
  const message = input.value.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";
  addMessage("typing", "");

  try {
    // const userApiKey = getUserApiKey();
    const apiKey = getUserApiKey();

    if (!window.sessionId) {
      window.sessionId = generateSessionId();
    }

    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message,
        session_id: window.sessionId,
        api_key: apiKey || undefined,
      }),
    });

    const data = await response.json();
    const chatMessages = document.getElementById("chatMessages");
    const typingIndicator = chatMessages.querySelector(".animate-bounce");
    if (typingIndicator) {
      typingIndicator.closest(".message").remove();
    }

    if (data.status === "success") {
      addMessage("assistant", data.response);
    } else if (data.error_type === "quota_exhausted") {
      addMessage(
        "assistant",
        `⚠️ **API Quota Exceeded**\n\n${data.message}\n\n**Solution:**\n1. Get a FREE API key from [Google AI Studio](https://aistudio.google.com/apikey)\n2. Paste it in the 'Your Google API Key' field above\n3. Click 'Save Key'`,
        false
      );
    } else if (data.error_type === "no_api_key") {
      addMessage(
        "assistant",
        `⚠️ **No API Key Available**\n\nPlease provide your Gemini API key above.`,
        false
      );
    } else {
      addMessage(
        "assistant",
        `**Error:** ${data.message || "Unknown error occurred"}`,
        false
      );
    }
  } catch (error) {
    const chatMessages = document.getElementById("chatMessages");
    const typingIndicator = chatMessages.querySelector(".animate-bounce");
    // if (typingIndicator) {
    //   typingIndicator.closest(".message").remove();
    // }
    if (typingIndicator && typingIndicator.closest(".message")) {
      typingIndicator.closest(".message").remove();
    }
    addMessage("assistant", `**Network Error:** ${error.message}`, false);
    console.error("Chat error:", error);
  }
}

// ============================================================================
// SEARCH FUNCTIONS
// ============================================================================

async function searchPapers() {
  const query = document.getElementById("searchQuery").value.trim();
  const category = document.getElementById("searchCategory").value;

  if (!query) {
    showNotification("Please enter a search query", "error");
    return;
  }

  const loadingDiv = document.getElementById("searchLoading");
  const resultsDiv = document.getElementById("searchResults");

  loadingDiv.classList.remove("hidden");
  resultsDiv.innerHTML = "";

  try {
    const userApiKey = getUserApiKey();

    const response = await fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: query,
        category: category,
        max_results: 10,
        api_key: userApiKey || undefined,
      }),
    });

    const data = await response.json();
    loadingDiv.classList.add("hidden");

    if (!response.ok) {
      if (data.error_type === "quota_exhausted") {
        showNotification(
          "API quota exceeded. Please use your own API key.",
          "error"
        );
        return;
      }
      throw new Error(data.message || "Search failed");
    }

    if (data.status === "success" && data.papers && data.papers.length > 0) {
      lastSearchResults = data.papers; //  to store results
      // Complete success display
      let html = `
        <div class="mb-6 text-center">
          <h3 class="text-2xl font-bold text-slate-800 mb-2">
            Found ${data.papers.length} Papers
          </h3>
          <p class="text-slate-600">Category: ${
            category === "all" ? "All Categories" : category
          }</p>
        </div>
      `;

      data.papers.forEach((paper, index) => {
        html += `
          <div class="paper-card bg-white rounded-2xl border border-gray-200 p-6 mb-4 hover:shadow-xl transition-all duration-300">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold text-lg">
                ${index + 1}
              </div>
              <div class="flex-1">
                <h4 class="text-lg font-bold text-slate-800 mb-2">
                  ${escapeHtml(paper.title)}
                </h4>
                <div class="text-sm text-slate-600 mb-3">
                  <span class="font-semibold">Authors:</span> ${escapeHtml(
                    paper.authors.slice(0, 3).join(", ")
                  )}${paper.authors.length > 3 ? ", et al." : ""}
                </div>
                <p class="text-slate-700 mb-4 leading-relaxed">
                  ${escapeHtml(paper.abstract)}
                </p>
                <div class="flex flex-wrap gap-3 items-center">
                  <span class="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
                    📅 ${paper.published}
                  </span>
                  <span class="text-xs bg-purple-100 text-purple-700 px-3 py-1 rounded-full">
                    🆔 ${paper.arxiv_id}
                  </span>
                  <a href="${
                    paper.pdf_url
                  }" target="_blank" class="text-xs bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full font-medium transition flex items-center gap-2">
                    <i class="fas fa-file-pdf"></i> View PDF
                  </a>
                </div>
              </div>
            </div>
          </div>
        `;
      });

      resultsDiv.innerHTML = html;

      // Show export button and update count
      const exportButtonContainer = document.getElementById(
        "exportButtonContainer"
      );
      const exportCount = document.getElementById("exportCount");
      if (exportButtonContainer && exportCount) {
        exportButtonContainer.classList.remove("hidden");
        exportCount.textContent = `${data.papers.length} papers`;
      }

      // Save search to history
      saveSearchToHistory(query, category, data.papers);
    } else {
      resultsDiv.innerHTML = `
        <div class="text-center py-12 bg-gray-50 rounded-2xl">
          <i class="fas fa-search text-6xl text-gray-300 mb-4"></i>
          <h4 class="text-xl font-bold text-gray-700 mb-2">No papers found</h4>
          <p class="text-gray-600">Try a different search query or category</p>
        </div>
      `;
    }
  } catch (error) {
    loadingDiv.classList.add("hidden");

    if (error.message.includes("429") || error.message.includes("quota")) {
      resultsDiv.innerHTML = `
        <div class="text-center py-12 bg-red-50 rounded-2xl border border-red-200">
          <i class="fas fa-exclamation-triangle text-6xl text-red-400 mb-4"></i>
          <h4 class="text-xl font-bold text-red-700 mb-2">API Quota Exceeded</h4>
          <p class="text-red-600">Please use your own API key above.</p>
        </div>
      `;
    } else {
      resultsDiv.innerHTML = `
        <div class="text-center py-12 bg-red-50 rounded-2xl border border-red-200">
          <i class="fas fa-exclamation-triangle text-6xl text-red-400 mb-4"></i>
          <h4 class="text-xl font-bold text-red-700 mb-2">Search Error</h4>
          <p class="text-red-600">${error.message}</p>
        </div>
      `;
    }
    console.error("Search error:", error);
  }
}

// Export to BibTeX
async function exportToBibTeX() {
  if (!lastSearchResults || lastSearchResults.length === 0) {
    showNotification(
      "No papers to export. Please search for papers first.",
      "error"
    );
    return;
  }

  try {
    showNotification("Generating BibTeX file...", "info");

    const response = await fetch("/api/export-bibtex", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        papers: lastSearchResults,
      }),
    });

    const data = await response.json();

    if (data.status === "success") {
      // Create downloadable file
      const blob = new Blob([data.bibtex_content], { type: "text/plain" });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = data.filename || "references.bib";
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      showNotification(
        `✅ Exported ${data.entry_count} papers to ${data.filename}`,
        "success"
      );
    } else {
      showNotification(`Export failed: ${data.message}`, "error");
    }
  } catch (error) {
    console.error("Export error:", error);
    showNotification("Failed to export papers", "error");
  }
}

// ============================================================================
// SEARCH HISTORY FUNCTIONS
// ============================================================================

// Load search history on page load
async function loadSearchHistory() {
  try {
    const sessionId = window.sessionId || generateSessionId();

    const response = await fetch(`/api/search-history?session_id=${sessionId}`);
    const data = await response.json();

    if (data.status === "success" && data.history && data.history.length > 0) {
      displaySearchHistory(data.history);
    }
  } catch (error) {
    console.error("Failed to load search history:", error);
  }
}

// Display search history in UI
function displaySearchHistory(history) {
  const historyContainer = document.getElementById("searchHistoryContainer");
  if (!historyContainer) return;

  let html =
    '<div class="mb-4"><h3 class="text-lg font-bold text-slate-800 mb-3 flex items-center gap-2"><i class="fas fa-history text-indigo-600"></i> Recent Searches</h3>';

  history.slice(0, 10).forEach((entry, index) => {
    html += `
      <div class="bg-gradient-to-r from-slate-50 to-indigo-50 rounded-lg p-3 mb-2 cursor-pointer hover:from-indigo-50 hover:to-purple-50 hover:shadow-md transition-all duration-200 border border-slate-200"
           onclick="reloadSearch('${escapeHtml(entry.query)}', '${
      entry.category
    }')">
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="font-medium text-sm text-slate-800">${escapeHtml(
              entry.query
            )}</div>
            <div class="text-xs text-slate-500 mt-1">
              <i class="far fa-clock mr-1"></i>${entry.timestamp} • 
              <i class="fas fa-file-alt mr-1"></i>${entry.result_count} papers
            </div>
          </div>
          <div class="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full font-medium ml-2">
            ${entry.category === "all" ? "All" : entry.category}
          </div>
        </div>
      </div>
    `;
  });

  html += `
    <button onclick="clearSearchHistory()" 
            class="text-sm text-red-500 hover:text-red-700 mt-3 flex items-center gap-1 transition">
      <i class="fas fa-trash-alt"></i> Clear History
    </button>
  </div>`;

  historyContainer.innerHTML = html;
}

// Reload a previous search
function reloadSearch(query, category) {
  // Set the search query and category
  const searchQueryInput = document.getElementById("searchQuery");
  const searchCategorySelect = document.getElementById("searchCategory");

  if (searchQueryInput) {
    searchQueryInput.value = query;
  }

  if (searchCategorySelect) {
    searchCategorySelect.value = category;
  }

  // Trigger the search
  searchPapers();

  // Scroll to search section
  document.getElementById("search")?.scrollIntoView({ behavior: "smooth" });
}

// Save search to history
async function saveSearchToHistory(query, category, papers) {
  try {
    const sessionId = window.sessionId || generateSessionId();

    await fetch("/api/search-history", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: sessionId,
        query: query,
        category: category,
        result_count: papers.length,
        papers: papers,
      }),
    });

    // Reload history display
    loadSearchHistory();
  } catch (error) {
    console.error("Failed to save search:", error);
  }
}

// Clear search history
async function clearSearchHistory() {
  if (!confirm("Clear all search history?")) return;

  try {
    const sessionId = window.sessionId || generateSessionId();

    const response = await fetch(
      `/api/search-history?session_id=${sessionId}`,
      {
        method: "DELETE",
      }
    );

    const data = await response.json();

    if (data.status === "success") {
      const historyContainer = document.getElementById(
        "searchHistoryContainer"
      );
      if (historyContainer) {
        historyContainer.innerHTML = "";
      }
      showNotification("Search history cleared", "success");
    }
  } catch (error) {
    console.error("Failed to clear history:", error);
    showNotification("Failed to clear history", "error");
  }
}

// ============================================================================
// NOTIFICATION SYSTEM
// ============================================================================

function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `fixed top-4 right-4 px-6 py-4 rounded-lg shadow-lg z-50 animate-slide-in ${
    type === "success"
      ? "bg-green-500"
      : type === "error"
      ? "bg-red-500"
      : "bg-blue-500"
  } text-white`;
  notification.textContent = message;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.classList.add("animate-slide-out");
    setTimeout(() => {
      if (document.body.contains(notification)) {
        document.body.removeChild(notification);
      }
    }, 300);
  }, 3000);
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ ResearchForge AI initialized");

  // Load saved API key
  const savedKey = getUserApiKey();
  if (savedKey) {
    window.userApiKey = savedKey;
    console.log("🔑 Loaded saved API key from localStorage");
  }

  // Generate session ID
  if (!window.sessionId) {
    window.sessionId = generateSessionId();
  }

  // Load search history
  loadSearchHistory();

  // Chat input enter key
  document.getElementById("chatInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Search input enter key
  document.getElementById("searchQuery").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      searchPapers();
    }
  });

  // Smooth scroll
  document.documentElement.style.scrollBehavior = "smooth";
});

console.log("✅ ResearchForge AI app.js loaded");
