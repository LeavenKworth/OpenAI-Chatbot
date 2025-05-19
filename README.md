OpenAI Chatbot — SE4458 Assigment

https://drive.google.com/file/d/1px_oojjrkhWLbwT2DCNMnTl0dpQODx3C/view?usp=sharing


## 🧠 AI Agent (Python)

The AI agent is implemented in Python using  OpenAI's API. It parses incoming chat messages, extracts intent and parameters using LangChain-like tools, and routes requests to the appropriate backend services (Midterm APIs).

- Uses OpenAI
- Parses chat intent and parameters
- Handles business logic interaction

---

## 🔄 API Gateway (C# .NET + Ocelot)

All frontend requests go through the .NET-based API Gateway, following the Ocelot pattern:

- Central entry point for all API traffic
- Routes chat messages to Python AI agent or midterm APIs

---

## 💻 Frontend (React)

A responsive chat UI built with React.js:

- Sends all user messages through the API Gateway
- Displays AI-generated replies and intermediate outputs

---

## ❌ Firebase?

Firebase Realtime Database or Firestore **was not used**.

---

## ⚙️ How It Works

![sequence](https://github.com/user-attachments/assets/4a560b4f-0736-4b0d-838a-34ffdbab289f)


1. User Interaction:
   - The user sends a message through the React-based chat UI.
2. API Gateway (C# .NET):
   - The message is received by the API Gateway, which routes it to the backend services.
3. AI Agent (Python):
   - The message is forwarded to the AI Agent for processing.
4. AI Agent:
   - Parses the intent via LLM (OpenAI)
   - Calls appropriate Midterm API(s) via api-gateway
   - Forms a response
5. Natural Language Conversion
   - The AI Agent converts the raw API response into a natural language reply (e.g., user-friendly explanation or summary).
6. Final Response Delivery
   - The AI Agent sends the human-readable message to the API Gateway,
   which then forwards it to the React UI.
7. UI Update
   - The chat interface updates with the final message, completing the interaction.

---

## 🧪 Tools & Technologies

| Layer          | Stack / Tool                      |
|----------------|-----------------------------------|
| Frontend       | React.js                          |
| API Gateway    | .NET C# (Ocelot-style architecture)|
| AI Agent       | Python (LangChain / OpenAI)       |

---

## Challenges I Faced
1. Integrating Python AI Agent with C# .NET Gateway:
- It was challenging to properly route HTTP requests from the .NET gateway to the Python AI Agent.
2.Following the API Gateway pattern using .NET:
- Most online examples for API Gateway were in Node.js, so adapting the Acelot-style architecture into .NET required additional research. I struggled with implementing clean routing logic and managing endpoints across services.
3. LLM API Integration (OpenAI):
- Connecting to the OpenAI API and parsing the model’s response into actionable intents was not straightforward. I had to experiment with different prompt designs and output formats to make it usable in my application logic.
4. Cross-Origin and Dev Environment Setup:
- Setting up three separate services (React, .NET, Python) and making them communicate on local development servers with proper ports and CORS headers was one of the trickiest parts of the project.
5. No Firebase / Real-time Handling

---

