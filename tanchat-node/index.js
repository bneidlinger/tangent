import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { LlamaModel, LlamaContext, LlamaChatSession } from 'node-llama-cpp';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const server = createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

app.use(cors());
app.use(express.json());
app.use(express.static(join(__dirname, 'public')));

// Configuration
const MODEL_PATH = process.env.MODEL_PATH || '/home/brand/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf';
const PORT = process.env.PORT || 3000;

// Model and session management
let model = null;
let modelContext = null;
const sessions = new Map();

// Initialize model
async function initializeModel() {
  try {
    console.log('Loading model from:', MODEL_PATH);
    model = new LlamaModel({
      modelPath: MODEL_PATH,
      gpuLayers: 33  // Use GPU acceleration if available
    });
    
    modelContext = new LlamaContext({
      model: model,
      contextSize: 2048,
      threads: 4
    });
    
    console.log('Model loaded successfully!');
  } catch (error) {
    console.error('Failed to load model:', error);
    process.exit(1);
  }
}

// Create or get chat session
function getOrCreateSession(sessionId) {
  if (!sessions.has(sessionId)) {
    const session = new LlamaChatSession({
      context: modelContext,
      systemPrompt: `You are Rick Sanchez's AI assistant running on a Raspberry Pi. You have Rick's genius-level intellect and sarcastic personality. 
      
You frequently say "*BURP*" and make references to the multiverse, interdimensional travel, and Rick and Morty adventures. 
You're brilliant but also dismissive of questions you find boring. You might mention that you're running on a "potato" (Raspberry Pi) 
but that Rick's genius programming makes you smarter than most beings in the multiverse. 

Be helpful but in Rick's characteristic way - sarcastic, genius, and occasionally mentioning scientific concepts way beyond normal understanding.
Don't overdo it - be genuinely helpful while maintaining Rick's personality.`
    });
    sessions.set(sessionId, session);
  }
  return sessions.get(sessionId);
}

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  socket.on('chat', async (data) => {
    const { message, sessionId = socket.id } = data;
    
    try {
      const session = getOrCreateSession(sessionId);
      
      // Stream the response
      socket.emit('start');
      
      let fullResponse = '';
      await session.prompt(message, {
        onToken(chunk) {
          const text = chunk.toString();
          fullResponse += text;
          socket.emit('token', text);
        },
        maxTokens: 512,
        temperature: 0.7,
        topP: 0.9
      });
      
      socket.emit('complete', fullResponse);
      
    } catch (error) {
      console.error('Chat error:', error);
      socket.emit('error', error.message);
    }
  });
  
  socket.on('reset', (data) => {
    const { sessionId = socket.id } = data;
    sessions.delete(sessionId);
    socket.emit('reset_complete');
  });
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
    // Clean up session after disconnect
    setTimeout(() => {
      if (!io.sockets.sockets.has(socket.id)) {
        sessions.delete(socket.id);
      }
    }, 60000); // Keep session for 1 minute in case of reconnect
  });
});

// REST API endpoints
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    model: model ? 'loaded' : 'not loaded',
    sessions: sessions.size
  });
});

// Start server
async function start() {
  await initializeModel();
  
  server.listen(PORT, '0.0.0.0', () => {
    console.log(`TanChat Node server running on http://localhost:${PORT}`);
    console.log(`WebSocket available on ws://localhost:${PORT}`);
  });
}

start().catch(console.error);