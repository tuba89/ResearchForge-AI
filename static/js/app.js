// /**
//  * ResearchForge AI - Frontend JavaScript
//  * Handles UI interactions, API calls, and dynamic content updates
//  */

// let sessionId = null;

// /**
//  * Scroll to search section
//  */
// function scrollToSearch() {
//   document.getElementById("search").scrollIntoView({ behavior: "smooth" });
// }

// /**
//  * Scroll to chat section
//  */
// function scrollToChat() {
//   document.getElementById("chat").scrollIntoView({ behavior: "smooth" });
// }

// /**
//  * Search for research papers
//  */
// async function searchPapers() {
//   const query = document.getElementById("searchQuery").value.trim();
//   const category = document.getElementById("searchCategory").value;

//   if (!query) {
//     showNotification("Please enter a search query", "error");
//     return;
//   }

//   const resultsContainer = document.getElementById("searchResults");
//   const loadingIndicator = document.getElementById("searchLoading");

//   // Show loading state
//   resultsContainer.innerHTML = "";
//   loadingIndicator.classList.remove("hidden");

//   try {
//     const response = await fetch("/api/search", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({
//         query: query,
//         category: category,
//         max_results: 10,
//       }),
//     });

//     const data = await response.json();

//     // Hide loading
//     loadingIndicator.classList.add("hidden");

//     if (data.status === "success") {
//       displaySearchResults(data.papers, query);
//     } else {
//       showNotification("Search failed: " + data.message, "error");
//     }
//   } catch (error) {
//     loadingIndicator.classList.add("hidden");
//     showNotification("Network error: " + error.message, "error");
//   }
// }

// /**
//  * Display search results
//  */
// function displaySearchResults(papers, query) {
//   const resultsContainer = document.getElementById("searchResults");

//   if (papers.length === 0) {
//     resultsContainer.innerHTML = `
//             <div class="text-center py-8 text-gray-500">
//                 <i class="fas fa-search text-4xl mb-4"></i>
//                 <p>No papers found for "${query}"</p>
//                 <p class="text-sm mt-2">Try different keywords or categories</p>
//             </div>
//         `;
//     return;
//   }

//   let html = `
//         <div class="mb-4">
//             <h4 class="text-lg font-semibold text-gray-800">
//                 Found ${papers.length} papers for "${query}"
//             </h4>
//         </div>
//         <div class="space-y-4">
//     `;

//   papers.forEach((paper) => {
//     html += `
//             <div class="paper-card bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md">
//                 <h5 class="text-lg font-bold text-gray-900 mb-2">
//                     ${escapeHtml(paper.title)}
//                 </h5>
//                 <div class="flex items-center space-x-4 text-sm text-gray-600 mb-3">
//                     <span>
//                         <i class="fas fa-calendar-alt mr-1"></i>
//                         ${paper.published}
//                     </span>
//                     <span>
//                         <i class="fas fa-id-badge mr-1"></i>
//                         ${paper.arxiv_id}
//                     </span>
//                 </div>
//                 <p class="text-gray-700 mb-2">
//                     <strong>Authors:</strong> ${paper.authors
//                       .slice(0, 3)
//                       .join(", ")}${paper.authors.length > 3 ? " et al." : ""}
//                 </p>
//                 <p class="text-gray-600 mb-4">
//                     ${escapeHtml(paper.abstract)}...
//                 </p>
//                 <div class="flex space-x-2">
//                     <a href="${paper.web_url}" target="_blank"
//                         class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
//                         <i class="fas fa-external-link-alt mr-2"></i>
//                         View on arXiv
//                     </a>
//                     <a href="${paper.pdf_url}" target="_blank"
//                         class="inline-flex items-center px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition">
//                         <i class="fas fa-file-pdf mr-2"></i>
//                         Download PDF
//                     </a>
//                 </div>
//             </div>
//         `;
//   });

//   html += "</div>";
//   resultsContainer.innerHTML = html;
// }

// /**
//  * Send chat message to AI agent
//  */
// async function sendMessage() {
//   const input = document.getElementById("chatInput");
//   const message = input.value.trim();

//   if (!message) return;

//   // Add user message to chat
//   addChatMessage(message, "user");
//   input.value = "";

//   // Show typing indicator
//   const typingId = addTypingIndicator();

//   try {
//     const response = await fetch("/api/chat", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({
//         message: message,
//         session_id: sessionId,
//       }),
//     });

//     const data = await response.json();

//     // Remove typing indicator
//     removeTypingIndicator(typingId);

//     if (data.status === "success") {
//       sessionId = data.session_id;
//       addChatMessage(data.response, "assistant");
//     } else {
//       addChatMessage("Sorry, I encountered an error: " + data.message, "error");
//     }
//   } catch (error) {
//     removeTypingIndicator(typingId);
//     addChatMessage("Network error: " + error.message, "error");
//   }
// }

// /**
//  * Add message to chat
//  */
// function addChatMessage(text, role) {
//   const chatMessages = document.getElementById("chatMessages");

//   // Remove empty state
//   if (chatMessages.querySelector(".text-center")) {
//     chatMessages.innerHTML = "";
//   }

//   const messageDiv = document.createElement("div");
//   messageDiv.className = `mb-4 animate-fade-in ${
//     role === "user" ? "text-right" : "text-left"
//   }`;

//   let bgColor, textColor, icon;
//   if (role === "user") {
//     bgColor = "bg-blue-600";
//     textColor = "text-white";
//     icon = "fa-user";
//   } else if (role === "assistant") {
//     bgColor = "bg-gray-200";
//     textColor = "text-gray-800";
//     icon = "fa-robot";
//   } else {
//     bgColor = "bg-red-100";
//     textColor = "text-red-800";
//     icon = "fa-exclamation-triangle";
//   }

//   messageDiv.innerHTML = `
//         <div class="inline-block ${bgColor} ${textColor} px-4 py-3 rounded-lg max-w-2xl">
//             <div class="flex items-start space-x-2">
//                 <i class="fas ${icon} mt-1"></i>
//                 <div class="whitespace-pre-wrap">${escapeHtml(text)}</div>
//             </div>
//         </div>
//     `;

//   chatMessages.appendChild(messageDiv);
//   chatMessages.scrollTop = chatMessages.scrollHeight;
// }

// /**
//  * Add typing indicator
//  */
// function addTypingIndicator() {
//   const chatMessages = document.getElementById("chatMessages");
//   const typingDiv = document.createElement("div");
//   const id = "typing-" + Date.now();
//   typingDiv.id = id;
//   typingDiv.className = "mb-4 text-left";
//   typingDiv.innerHTML = `
//         <div class="inline-block bg-gray-200 text-gray-800 px-4 py-3 rounded-lg">
//             <div class="flex items-center space-x-2">
//                 <i class="fas fa-robot"></i>
//                 <div class="flex space-x-1">
//                     <div class="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style="animation-delay: 0s"></div>
//                     <div class="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
//                     <div class="w-2 h-2 bg-gray-600 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
//                 </div>
//             </div>
//         </div>
//     `;
//   chatMessages.appendChild(typingDiv);
//   chatMessages.scrollTop = chatMessages.scrollHeight;
//   return id;
// }

// /**
//  * Remove typing indicator
//  */
// function removeTypingIndicator(id) {
//   const element = document.getElementById(id);
//   if (element) {
//     element.remove();
//   }
// }

// /**
//  * Show notification
//  */
// function showNotification(message, type = "info") {
//   const notification = document.createElement("div");
//   notification.className = `fixed top-4 right-4 px-6 py-4 rounded-lg shadow-lg z-50 animate-slide-up ${
//     type === "error" ? "bg-red-500" : "bg-blue-500"
//   } text-white`;
//   notification.innerHTML = `
//         <div class="flex items-center space-x-2">
//             <i class="fas ${
//               type === "error" ? "fa-exclamation-circle" : "fa-info-circle"
//             }"></i>
//             <span>${escapeHtml(message)}</span>
//         </div>
//     `;
//   document.body.appendChild(notification);

//   setTimeout(() => {
//     notification.remove();
//   }, 5000);
// }

// /**
//  * Escape HTML to prevent XSS
//  */
// function escapeHtml(text) {
//   const div = document.createElement("div");
//   div.textContent = text;
//   return div.innerHTML;
// }

// /**
//  * Initialize app
//  */
// document.addEventListener("DOMContentLoaded", () => {
//   console.log("ResearchForge AI initialized");

//   // Add enter key listener for search
//   document.getElementById("searchQuery").addEventListener("keypress", (e) => {
//     if (e.key === "Enter") {
//       searchPapers();
//     }
//   });
// });
/**
 * ResearchForge AI - Enhanced Frontend JavaScript
 *
 */

let sessionId = null;

// Scroll functions
function scrollToSearch() {
  document.getElementById("search").scrollIntoView({ behavior: "smooth" });
  setTimeout(() => document.getElementById("searchQuery").focus(), 500);
}

function scrollToChat() {
  document.getElementById("chat").scrollIntoView({ behavior: "smooth" });
  setTimeout(() => document.getElementById("chatInput").focus(), 500);
}

// Fill example queries
function fillExample(text) {
  document.getElementById("chatInput").value = text;
  document.getElementById("chatInput").focus();
}

// Clear chat
function clearChat() {
  const chatMessages = document.getElementById("chatMessages");
  chatMessages.innerHTML = `
        <div class="text-center text-gray-400 mt-40">
            <div class="text-8xl mb-6 animate-pulse-slow">⚛️</div>
            <h4 class="text-2xl font-bold text-gray-700 mb-3">Ready to assist your research</h4>
            <p class="text-lg mb-6">Start a conversation with the AI assistant</p>
            <div class="flex flex-wrap justify-center gap-3">
                <button onclick="fillExample('Find papers about quantum computing')"
                    class="bg-white px-4 py-2 rounded-lg text-sm text-gray-700 hover:bg-purple-50 hover:text-purple-600 transition shadow">
                    🔍 Find papers
                </button>
                <button onclick="fillExample('Generate a research proposal')"
                    class="bg-white px-4 py-2 rounded-lg text-sm text-gray-700 hover:bg-purple-50 hover:text-purple-600 transition shadow">
                    📝 Generate proposal
                </button>
                <button onclick="fillExample('Draft a collaboration email')"
                    class="bg-white px-4 py-2 rounded-lg text-sm text-gray-700 hover:bg-purple-50 hover:text-purple-600 transition shadow">
                    ✉️ Draft email
                </button>
            </div>
        </div>
    `;
  sessionId = null;
}

// Simple markdown formatting (lightweight, no external library needed)
function formatMarkdown(text) {
  let html = text;

  // Headers
  html = html.replace(
    /^### (.*$)/gim,
    '<h3 class="text-xl font-semibold text-gray-800 mt-4 mb-2">$1</h3>'
  );
  html = html.replace(
    /^## (.*$)/gim,
    '<h2 class="text-2xl font-bold text-gray-800 mt-6 mb-3">$1</h2>'
  );
  html = html.replace(
    /^# (.*$)/gim,
    '<h1 class="text-3xl font-bold text-gray-900 mt-8 mb-4">$1</h1>'
  );

  // Bold
  html = html.replace(
    /\*\*(.*?)\*\*/g,
    '<strong class="font-semibold text-gray-900">$1</strong>'
  );

  // Italic
  html = html.replace(/\*(.*?)\*/g, '<em class="italic text-gray-700">$1</em>');

  // Code blocks
  html = html.replace(
    /```(.*?)```/gs,
    '<pre class="bg-gray-800 text-gray-100 p-4 rounded-lg my-3 overflow-x-auto"><code>$1</code></pre>'
  );

  // Inline code
  html = html.replace(
    /`(.*?)`/g,
    '<code class="bg-gray-100 text-red-600 px-2 py-1 rounded text-sm">$1</code>'
  );

  // Unordered lists
  html = html.replace(/^\* (.*$)/gim, '<li class="ml-6 mb-2">• $1</li>');
  html = html.replace(/^- (.*$)/gim, '<li class="ml-6 mb-2">• $1</li>');

  // Numbered lists
  html = html.replace(
    /^\d+\. (.*$)/gim,
    '<li class="ml-6 mb-2 list-decimal">$1</li>'
  );

  // Links
  html = html.replace(
    /\[(.*?)\]\((.*?)\)/g,
    '<a href="$2" target="_blank" class="text-blue-600 hover:text-purple-600 underline">$1</a>'
  );

  // Line breaks
  html = html.replace(
    /\n\n/g,
    '</p><p class="mb-3 leading-relaxed text-gray-700">'
  );
  html = html.replace(/\n/g, "<br>");

  // Wrap in paragraph
  html = '<p class="mb-3 leading-relaxed text-gray-700">' + html + "</p>";

  return html;
}

// Add message to chat with markdown support
function addMessage(role, content, isRaw = false) {
  const chatMessages = document.getElementById("chatMessages");

  // Remove welcome message if exists
  const welcomeMsg = chatMessages.querySelector(".text-center.text-gray-400");
  if (welcomeMsg) {
    welcomeMsg.remove();
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
                        <div class="leading-relaxed">${escapeHtml(
                          content
                        )}</div>
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
                            ${
                              isRaw
                                ? escapeHtml(content)
                                : formatMarkdown(content)
                            }
                        </div>
                    </div>
                </div>
            </div>
        `;
  }

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Escape HTML
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

// Send chat message
async function sendMessage() {
  const input = document.getElementById("chatInput");
  const message = input.value.trim();

  if (!message) return;

  // Add user message
  addMessage("user", message);
  input.value = "";

  // Show typing indicator
  addMessage("typing", "");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
        session_id: sessionId,
      }),
    });

    const data = await response.json();

    // Remove typing indicator
    const chatMessages = document.getElementById("chatMessages");
    const typingIndicator = chatMessages.querySelector(".animate-bounce");
    if (typingIndicator) {
      typingIndicator.closest(".message").remove();
    }

    if (data.status === "success") {
      sessionId = data.session_id;
      // Add AI response with markdown formatting
      addMessage("assistant", data.response);
    } else {
      addMessage(
        "assistant",
        `**Error:** ${data.message || "Unknown error occurred"}`,
        false
      );
    }
  } catch (error) {
    // Remove typing indicator
    const chatMessages = document.getElementById("chatMessages");
    const typingIndicator = chatMessages.querySelector(".animate-bounce");
    if (typingIndicator) {
      typingIndicator.closest(".message").remove();
    }

    // Show error
    addMessage(
      "assistant",
      `**Error:** Unable to connect to the AI assistant. Please try again.\n\n*${error.message}*`,
      false
    );
    console.error("Chat error:", error);
  }
}

// Search papers
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
    const response = await fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: query,
        category: category,
        max_results: 10,
      }),
    });

    const data = await response.json();
    loadingDiv.classList.add("hidden");

    if (data.status === "success" && data.papers && data.papers.length > 0) {
      resultsDiv.innerHTML = `
                <div class="mb-6">
                    <div class="flex items-center justify-between mb-4">
                        <h4 class="text-xl font-bold text-gray-800">
                            <i class="fas fa-check-circle text-green-500 mr-2"></i>
                            Found ${data.papers.length} papers
                        </h4>
                        <span class="text-sm text-gray-600">
                            <i class="fas fa-clock mr-1"></i>
                            Just now
                        </span>
                    </div>
                    <div class="space-y-4">
                        ${data.papers
                          .map(
                            (paper, index) => `
                            <div class="paper-card bg-white border border-gray-200 rounded-xl p-6 hover:border-purple-300 hover:shadow-lg transition-all">
                                <div class="flex gap-4">
                                    <div class="flex-shrink-0 w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold text-lg shadow-lg">
                                        ${index + 1}
                                    </div>
                                    <div class="flex-1">
                                        <h5 class="font-bold text-lg text-gray-800 mb-2 leading-tight">
                                            ${escapeHtml(paper.title)}
                                        </h5>
                                        <div class="flex flex-wrap items-center gap-3 mb-3 text-sm text-gray-600">
                                            <span>
                                                <i class="fas fa-user mr-1"></i>
                                                ${escapeHtml(
                                                  paper.authors
                                                    .slice(0, 3)
                                                    .join(", ")
                                                )}
                                                ${
                                                  paper.authors.length > 3
                                                    ? ` +${
                                                        paper.authors.length - 3
                                                      } more`
                                                    : ""
                                                }
                                            </span>
                                            <span>
                                                <i class="fas fa-calendar mr-1"></i>
                                                ${paper.published || "N/A"}
                                            </span>
                                            <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full font-medium text-xs">
                                                ${paper.arxiv_id}
                                            </span>
                                        </div>
                                        ${
                                          paper.abstract
                                            ? `
                                            <p class="text-gray-600 text-sm mb-3 leading-relaxed line-clamp-3">
                                                ${escapeHtml(
                                                  paper.abstract.substring(
                                                    0,
                                                    300
                                                  )
                                                )}...
                                            </p>
                                        `
                                            : ""
                                        }
                                        <div class="flex gap-2">
                                            <a href="${
                                              paper.pdf_url || paper.web_url
                                            }" target="_blank"
                                                class="inline-flex items-center px-4 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-lg hover:from-red-600 hover:to-pink-600 transition shadow-md hover:shadow-lg text-sm font-medium">
                                                <i class="fas fa-file-pdf mr-2"></i>
                                                View PDF
                                            </a>
                                            <a href="${
                                              paper.web_url ||
                                              "https://arxiv.org/abs/" +
                                                paper.arxiv_id
                                            }" target="_blank"
                                                class="inline-flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition text-sm font-medium">
                                                <i class="fas fa-external-link-alt mr-2"></i>
                                                arXiv Page
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `
                          )
                          .join("")}
                    </div>
                </div>
            `;
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
    resultsDiv.innerHTML = `
            <div class="text-center py-12 bg-red-50 rounded-2xl border border-red-200">
                <i class="fas fa-exclamation-triangle text-6xl text-red-400 mb-4"></i>
                <h4 class="text-xl font-bold text-red-700 mb-2">Search Error</h4>
                <p class="text-red-600">${error.message}</p>
            </div>
        `;
    console.error("Search error:", error);
  }
}

// Show notification
function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `fixed top-4 right-4 px-6 py-4 rounded-lg shadow-lg z-50 animate-slide-up ${
    type === "error" ? "bg-red-500" : "bg-blue-500"
  } text-white`;
  notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas ${
              type === "error" ? "fa-exclamation-circle" : "fa-info-circle"
            }"></i>
            <span>${escapeHtml(message)}</span>
        </div>
    `;
  document.body.appendChild(notification);

  setTimeout(() => {
    notification.remove();
  }, 5000);
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ ResearchForge AI initialized");

  // Add enter key listener for chat
  document.getElementById("chatInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Add enter key listener for search
  document.getElementById("searchQuery").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      searchPapers();
    }
  });

  // Smooth scroll
  document.documentElement.style.scrollBehavior = "smooth";
});
