const messagesEl = document.getElementById('messages');
const formEl = document.getElementById('chat-form');
const inputEl = document.getElementById('input');
const sendBtn = document.getElementById('send');

// Use a consistent session ID that persists across page reloads
// This ensures conversations are remembered even after server restarts
let sessionId = localStorage.getItem('financial_session_id');
if (!sessionId) {
    sessionId = 'user_' + Date.now();
    localStorage.setItem('financial_session_id', sessionId);
}

function addMessage(text, role) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function loadExistingConversation() {
  try {
    // Check if there are existing messages for this session
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        message: "Hello, I'm back! Can you remind me what we discussed about my finances?",
        session_id: sessionId
      }),
    });
    if (res.ok) {
      const data = await res.json();
      // If this is a new session, the bot will give a fresh response
      // If it's an existing session, the bot will reference previous conversation
      addMessage(data.reply, 'bot');
    }
  } catch (err) {
    console.error('Error loading conversation:', err);
    // If there's an error, just show the welcome message
    addMessage('Hello! I\'m your AI financial advisor. I can help you with:\n\n• Budgeting and saving strategies\n• Investment basics and portfolio concepts\n• Retirement planning fundamentals\n• Tax planning principles\n• Insurance and risk management\n• Debt management strategies\n\nWhat would you like to learn about today?', 'bot');
  }
}

async function clearConversation() {
  try {
    const res = await fetch(`/chat/${sessionId}`, {
      method: 'DELETE'
    });
    if (res.ok) {
      messagesEl.innerHTML = '';
      addMessage('Financial consultation session cleared. How can I help you with your financial goals today?', 'bot');
    }
  } catch (err) {
    console.error('Error clearing conversation:', err);
  }
}

async function startNewSession() {
  // Generate a new session ID
  sessionId = 'user_' + Date.now();
  localStorage.setItem('financial_session_id', sessionId);
  
  // Clear the display
  messagesEl.innerHTML = '';
  
  // Show welcome message for new session
  addMessage('Hello! I\'m your AI financial advisor. I can help you with:\n\n• Budgeting and saving strategies\n• Investment basics and portfolio concepts\n• Retirement planning fundamentals\n• Tax planning principles\n• Insurance and risk management\n• Debt management strategies\n\nWhat would you like to learn about today?', 'bot');
}

formEl.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = inputEl.value.trim();
  if (!text) return;
  
  addMessage(text, 'user');
  inputEl.value = '';

  sendBtn.disabled = true;
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        message: text,
        session_id: sessionId
      }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    const data = await res.json();
    addMessage(data.reply || '', 'bot');
  } catch (err) {
    addMessage(`Error: ${err.message}`, 'bot');
  } finally {
    sendBtn.disabled = false;
    inputEl.focus();
  }
});

// Add buttons to the header
document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('header');
  
  // Clear current session button
  const clearBtn = document.createElement('button');
  clearBtn.textContent = '🗑️ Clear Chat';
  clearBtn.style.cssText = 'margin-left: auto; padding: 8px 16px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.1); color: white; font-weight: 600; cursor: pointer; backdrop-filter: blur(10px); margin-right: 8px;';
  clearBtn.onmouseover = () => clearBtn.style.background = 'rgba(255,255,255,0.2)';
  clearBtn.onmouseout = () => clearBtn.style.background = 'rgba(255,255,255,0.1)';
  clearBtn.onclick = clearConversation;
  header.appendChild(clearBtn);
  
  // New session button
  const newSessionBtn = document.createElement('button');
  newSessionBtn.textContent = '🆕 New Session';
  newSessionBtn.style.cssText = 'padding: 8px 16px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.1); color: white; font-weight: 600; cursor: pointer; backdrop-filter: blur(10px);';
  newSessionBtn.onmouseover = () => newSessionBtn.style.background = 'rgba(255,255,255,0.2)';
  newSessionBtn.onmouseout = () => newSessionBtn.style.background = 'rgba(255,255,255,0.1)';
  newSessionBtn.onclick = startNewSession;
  header.appendChild(newSessionBtn);
  
  // Load existing conversation or show welcome message
  loadExistingConversation();
});


