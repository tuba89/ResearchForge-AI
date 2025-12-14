// ============================================================================
// RESEARCHFORGE AI - Enhanced Frontend JavaScript
// Agent Status Tracking & Workflow Visualization
// ============================================================================

// Agent status polling
let statusPollInterval = null;

function startAgentStatusPolling() {
  // Poll every 2 seconds
  statusPollInterval = setInterval(updateAgentStatus, 2000);
}

function stopAgentStatusPolling() {
  if (statusPollInterval) {
    clearInterval(statusPollInterval);
    statusPollInterval = null;
  }
}

async function updateAgentStatus() {
  try {
    const response = await fetch("/api/agent-status");
    const data = await response.json();

    if (data.status === "success" && data.agents) {
      // Update each agent's status indicator
      for (const [agentName, status] of Object.entries(data.agents)) {
        const statusElement = document.getElementById(
          `status-${agentName.toLowerCase()}`
        );
        if (statusElement) {
          // Remove all status classes
          statusElement.classList.remove("ready", "active", "processing");
          // Add current status class
          statusElement.classList.add(status);
        }
      }
    }
  } catch (error) {
    console.error("Agent status update error:", error);
    // Silently fail - don't disturb user experience
  }
}

// Workflow step highlighting
function highlightWorkflowStep(stepName) {
  // Remove active class from all steps
  document.querySelectorAll(".workflow-step").forEach((step) => {
    step.classList.remove("active");
  });

  // Add active class to current step
  const currentStep = document.querySelector(`[data-step="${stepName}"]`);
  if (currentStep) {
    currentStep.classList.add("active");
  }
}

// Enhanced message display with agent attribution
function addMessageWithAgent(role, content, metadata = {}) {
  addMessage(role, content, false);

  // If agent name is provided, highlight it in the dashboard
  if (metadata.agentName) {
    const agentCard = document.querySelector(
      `#status-${metadata.agentName.toLowerCase()}`
    );
    if (agentCard) {
      agentCard.classList.add("active");
      setTimeout(() => {
        agentCard.classList.remove("active");
        agentCard.classList.add("ready");
      }, 3000);
    }
  }

  // If workflow step is provided, highlight it
  if (metadata.workflowStep) {
    highlightWorkflowStep(metadata.workflowStep);
  }
}

// Initialize agent status polling on page load
document.addEventListener("DOMContentLoaded", () => {
  // Start agent status polling
  startAgentStatusPolling();

  // Log that we're running with 8-agent system
  console.log("🤖 8-Agent System Active");
  console.log("📊 Agent Status Polling: Started");
});

// Cleanup on page unload
window.addEventListener("beforeunload", () => {
  stopAgentStatusPolling();
});
