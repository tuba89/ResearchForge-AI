// ============================================================================
// ERROR MODAL & API KEY MANAGEMENT - Add to app.js
// ============================================================================

// Show beautiful error modal
function showErrorModal(errorData) {
  // Remove existing modal if any
  const existingModal = document.getElementById("errorModal");
  if (existingModal) {
    existingModal.remove();
  }

  const modal = document.createElement("div");
  modal.id = "errorModal";
  modal.className =
    "fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in";
  modal.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
  modal.style.backdropFilter = "blur(4px)";

  const isQuotaError = errorData.error_type === "quota_exhausted";
  const iconColor = isQuotaError ? "text-yellow-500" : "text-red-500";
  const icon = isQuotaError ? "fa-exclamation-triangle" : "fa-times-circle";

  modal.innerHTML = `
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 animate-slide-up" onclick="event.stopPropagation()">
      <div class="text-center mb-6">
        <div class="w-16 h-16 ${
          isQuotaError ? "bg-yellow-100" : "bg-red-100"
        } rounded-full flex items-center justify-center mx-auto mb-4">
          <i class="fas ${icon} text-3xl ${iconColor}"></i>
        </div>
        <h3 class="text-2xl font-bold text-gray-800 mb-2">${
          errorData.title || "Error"
        }</h3>
        <p class="text-gray-600">${errorData.message || "An error occurred"}</p>
      </div>

      ${
        errorData.suggestions && errorData.suggestions.length > 0
          ? `
        <div class="mb-6">
          <h4 class="font-semibold text-gray-700 mb-3">💡 Suggestions:</h4>
          <ul class="space-y-2">
            ${errorData.suggestions
              .map(
                (suggestion) => `
              <li class="flex items-start gap-2 text-sm text-gray-600">
                <span class="text-indigo-500 mt-1">•</span>
                <span>${suggestion}</span>
              </li>
            `
              )
              .join("")}
          </ul>
        </div>
      `
          : ""
      }

      <div class="flex gap-3">
        ${
          errorData.can_retry
            ? `
          <button onclick="closeErrorModal(); retryLastAction();" 
            class="flex-1 px-4 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-semibold transition">
            <i class="fas fa-redo mr-2"></i>Retry
          </button>
        `
            : ""
        }
        ${
          errorData.show_api_key_option
            ? `
          <button onclick="closeErrorModal(); showApiKeyInput();" 
            class="flex-1 px-4 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white rounded-xl font-semibold transition">
            <i class="fas fa-key mr-2"></i>Use My Key
          </button>
        `
            : ""
        }
        <button onclick="closeErrorModal()" 
          class="px-4 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl font-semibold transition">
          Close
        </button>
      </div>
    </div>
  `;

  // Close on backdrop click
  modal.addEventListener("click", closeErrorModal);

  document.body.appendChild(modal);
}

// Show beautiful error modal
function showErrorModal(errorData) {
  // Remove existing modal if any
  const existingModal = document.getElementById("errorModal");
  if (existingModal) {
    existingModal.remove();
  }

  const modal = document.createElement("div");
  modal.id = "errorModal";
  modal.className =
    "fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in";
  modal.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
  modal.style.backdropFilter = "blur(4px)";

  const isQuotaError = errorData.error_type === "quota_exhausted";
  const iconColor = isQuotaError ? "text-yellow-500" : "text-red-500";
  const icon = isQuotaError ? "fa-exclamation-triangle" : "fa-times-circle";

  modal.innerHTML = `
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 animate-slide-up" onclick="event.stopPropagation()">
      <div class="text-center mb-6">
        <div class="w-16 h-16 ${
          isQuotaError ? "bg-yellow-100" : "bg-red-100"
        } rounded-full flex items-center justify-center mx-auto mb-4">
          <i class="fas ${icon} text-3xl ${iconColor}"></i>
        </div>
        <h3 class="text-2xl font-bold text-gray-800 mb-2">${
          errorData.title || "Error"
        }</h3>
        <p class="text-gray-600 mb-4">${
          errorData.message || "An error occurred"
        }</p>
        
        ${
          isQuotaError
            ? `<div class="bg-yellow-50 border-l-4 border-yellow-400 p-3 mb-4 text-left">
               <p class="text-yellow-700 text-sm"><i class="fas fa-lightbulb mr-2"></i>This is a FREE service limitation. Get your own key for unlimited usage.</p>
             </div>`
            : ""
        }
      </div>

      ${
        errorData.suggestions && errorData.suggestions.length > 0
          ? `
        <div class="mb-6">
          <h4 class="font-semibold text-gray-700 mb-3">💡 Quick Fix:</h4>
          <ol class="space-y-2 text-sm text-gray-600">
            ${errorData.suggestions
              .map(
                (suggestion, index) => `
              <li class="flex items-start gap-2">
                <span class="flex-shrink-0 w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-700 font-bold text-xs">${
                  index + 1
                }</span>
                <span>${suggestion}</span>
              </li>
            `
              )
              .join("")}
          </ol>
        </div>
      `
          : ""
      }

      <div class="flex flex-col gap-3">
        ${
          errorData.show_api_key_option
            ? `
          <button onclick="scrollToApiKeySection(); closeErrorModal();" 
            class="w-full px-4 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white rounded-xl font-semibold transition flex items-center justify-center">
            <i class="fas fa-key mr-2"></i>Enter My API Key Now
          </button>
        `
            : ""
        }
        ${
          errorData.can_retry
            ? `
          <button onclick="closeErrorModal(); retryLastAction();" 
            class="w-full px-4 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-semibold transition flex items-center justify-center">
            <i class="fas fa-redo mr-2"></i>Try Again
          </button>
        `
            : ""
        }
        <button onclick="closeErrorModal()" 
          class="w-full px-4 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl font-semibold transition">
          Close
        </button>
      </div>
    </div>
  `;

  // Close on backdrop click
  modal.addEventListener("click", closeErrorModal);

  document.body.appendChild(modal);
}

// Scroll to API key section
function scrollToApiKeySection() {
  const apiKeySection = document.getElementById("apiKeySection");
  if (apiKeySection) {
    apiKeySection.scrollIntoView({ behavior: "smooth" });

    // Highlight the section
    apiKeySection.classList.add("ring-4", "ring-yellow-400", "ring-opacity-50");

    // Focus on the input field
    const keyInput = document.getElementById("userApiKeyInput");
    if (keyInput) {
      keyInput.focus();
    }

    // Remove highlight after 3 seconds
    setTimeout(() => {
      apiKeySection.classList.remove(
        "ring-4",
        "ring-yellow-400",
        "ring-opacity-50"
      );
    }, 3000);
  }
}
// Close error modal
function closeErrorModal() {
  const modal = document.getElementById("errorModal");
  if (modal) {
    modal.classList.add("animate-fade-out");
    setTimeout(() => modal.remove(), 200);
  }
}

// Show API key input section
function showApiKeyInput() {
  const apiKeySection = document.getElementById("apiKeySection");
  if (apiKeySection) {
    apiKeySection.scrollIntoView({ behavior: "smooth" });
    apiKeySection.classList.add("ring-4", "ring-indigo-300");
    setTimeout(() => {
      apiKeySection.classList.remove("ring-4", "ring-indigo-300");
    }, 2000);
  }
}

// Save user API key to sessionStorage
// function saveUserApiKey() {
//   const input = document.getElementById("userApiKeyInput");
//   const key = input.value.trim();

//   if (!key) {
//     showNotification("Please enter an API key", "error");
//     return;
//   }

//   // Basic validation (Google API keys start with "AIza")
//   if (!key.startsWith("AIza")) {
//     showNotification(
//       "Invalid API key format. Google API keys start with 'AIza'",
//       "error"
//     );
//     return;
//   }

//   sessionStorage.setItem("user_api_key", key);
//   showNotification("API key saved for this session! 🎉", "success");
//   input.value = "";

//   // Hide the input section
//   const apiKeySection = document.getElementById("apiKeySection");
//   if (apiKeySection) {
//     apiKeySection.style.display = "none";
//   }
// }

// Save user API key
function saveUserApiKey() {
  const input = document.getElementById("userApiKeyInput");
  const key = input.value.trim();

  if (!key) {
    showNotification("Please enter an API key", "error");
    return;
  }

  // Better validation
  if (!key.startsWith("AIza")) {
    showNotification(
      "Invalid API key format. Google API keys start with 'AIza'",
      "error"
    );
    return;
  }

  if (key.length < 30) {
    showNotification(
      "Key seems too short. A valid Google API key is usually 40+ characters.",
      "error"
    );
    return;
  }

  // Save to sessionStorage
  sessionStorage.setItem("user_api_key", key);

  // Also save to window for immediate use
  window.userApiKey = key;

  showNotification(
    "✅ API key saved! It will be used for your next request.",
    "success"
  );

  // Optional: Clear the input field
  input.value = "";

  // Optional: Hide the API key input section if you want
  // document.getElementById("apiKeySection").style.display = "none";
}

// Load API key on page load
document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ ResearchForge AI initialized");

  // Load saved API key
  const savedKey = sessionStorage.getItem("user_api_key");
  if (savedKey) {
    const keyInput = document.getElementById("userApiKeyInput");
    if (keyInput) {
      keyInput.value = savedKey;
      window.userApiKey = savedKey;
      console.log(`🔑 Loaded saved API key: ${savedKey.substring(0, 10)}...`);
    }
  }

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

// Debug: Check what API key is being sent
function debugApiKeyStatus() {
  const savedKey = sessionStorage.getItem("user_api_key");
  const inputKey = document.getElementById("userApiKeyInput")?.value.trim();

  console.log("=== API KEY DEBUG ===");
  console.log(
    "Session Storage Key:",
    savedKey ? savedKey.substring(0, 15) + "..." : "None"
  );
  console.log("Input Field Key:", inputKey || "Empty");
  console.log(
    "Will be sent:",
    savedKey || inputKey || "DEFAULT (quota exhausted)"
  );
  console.log("====================");

  // Call this before sending a message
  debugApiKeyStatus();
}

// Get user API key from sessionStorage
function getUserApiKey() {
  return sessionStorage.getItem("user_api_key");
}

// Clear user API key
function clearUserApiKey() {
  sessionStorage.removeItem("user_api_key");
  showNotification("API key cleared", "info");

  // Show the input section again
  const apiKeySection = document.getElementById("apiKeySection");
  if (apiKeySection) {
    apiKeySection.style.display = "block";
  }
}

// Retry last action (placeholder - to be implemented based on context)
let lastAction = null;
function retryLastAction() {
  if (lastAction) {
    lastAction();
  } else {
    showNotification("Please try your request again", "info");
  }
}
