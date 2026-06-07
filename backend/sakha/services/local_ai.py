"""Local AI Service - Intelligent response generation for local development"""

import logging
from typing import List, Dict, Optional, AsyncGenerator
import asyncio

logger = logging.getLogger(__name__)


class LocalAIService:
    """Generate intelligent, context-aware responses locally"""

    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()

    def _initialize_knowledge_base(self) -> Dict[str, Dict]:
        """Initialize response templates for common topics"""
        return {
            "photosynthesis": {
                "short": "Photosynthesis is the process by which plants convert sunlight, water, and CO2 into glucose and oxygen.",
                "long": "Photosynthesis is a biochemical process where plants, algae, and some bacteria convert light energy from the sun into chemical energy. It occurs in two main stages: (1) Light-dependent reactions in the thylakoid membranes, where photons are absorbed by chlorophyll to generate ATP and NADPH, splitting water molecules and releasing oxygen; (2) Light-independent reactions (Calvin cycle) in the stroma, using ATP and NADPH to fix CO2 into glucose. The overall equation is: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2. This process is fundamental to life on Earth, producing oxygen and organic compounds that form the base of most food chains.",
                "deep_thinking": "Photosynthesis represents one of nature's most elegant energy conversion systems. At the quantum level, photons interact with chlorophyll molecules, transferring their energy through a coordinated network of pigments and electron transport chains. The Z-scheme (zigzag pattern of electron flow) involves two photosystems working in concert to accomplish water oxidation, one of chemistry's most challenging reactions. The Calvin cycle operates with remarkable precision, using only three molecules of ATP and two of NADPH per CO2 fixed. Consider the evolutionary implications: photosynthesis evolved as cyanobacteria roughly 2.5 billion years ago, fundamentally transforming Earth's atmosphere from anoxic to oxygen-rich. This enabled the evolution of aerobic respiration and complex multicellular life. The efficiency of photosynthesis (~11% for C3 plants) has been a target for agricultural improvement. Recent research into artificial photosynthesis and synthetic biology aims to replicate this process for carbon capture and biofuel production."
            },
            "ai": {
                "short": "Artificial Intelligence (AI) refers to computer systems designed to perform tasks that typically require human intelligence.",
                "long": "Artificial Intelligence encompasses a broad spectrum of technologies that enable machines to perform cognitive tasks. AI systems can be categorized by capability level: Narrow AI (specialized for specific tasks like image recognition) versus General AI (hypothetically capable of any intellectual task). Machine Learning, a subset of AI, enables systems to learn from data without explicit programming. Deep Learning uses neural networks with multiple layers to process complex patterns. Key techniques include supervised learning (training on labeled data), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through rewards). Modern AI applications include natural language processing (NLPs), computer vision, recommendation systems, autonomous vehicles, and game-playing AI. The field combines insights from computer science, statistics, neuroscience, and cognitive psychology.",
                "deep_thinking": "Artificial Intelligence is fundamentally about information processing and decision-making under uncertainty. The philosophical question of whether AI can achieve true 'intelligence' or 'consciousness' remains contested—is intelligence substrate-independent, or does it require biological implementation? From a computational perspective, AI represents the formalization of problem-solving: decomposing tasks into computable steps, representing knowledge symbolically or connectionally, and optimizing for specified objectives. The transformer architecture's success in large language models suggests that attention mechanisms and scale are crucial for emergent capabilities. There's an intriguing empirical phenomenon: as models scale, new abilities emerge that weren't explicitly trained for (emergence). This raises questions about the nature of generalization and whether sufficiently large models approach a form of general problem-solving. The alignment problem—ensuring AI systems pursue human-intended goals—represents perhaps the most critical challenge as capabilities advance."
            },
            "quantum computing": {
                "short": "Quantum computers use quantum bits (qubits) that can exist in superposition, potentially solving certain problems faster than classical computers.",
                "long": "Quantum computing harnesses principles of quantum mechanics to process information differently from classical computers. Key concepts include: (1) Superposition: qubits can be 0, 1, or both simultaneously; (2) Entanglement: qubits can be correlated in ways that have no classical analogue; (3) Interference: quantum algorithms amplify correct answers while canceling wrong ones. Quantum gates manipulate qubits through unitary transformations. Notable algorithms include Shor's algorithm (factoring large numbers exponentially faster) and Grover's algorithm (database search). Quantum computers excel at specific problem classes but are not universally faster. Current implementations face challenges: decoherence (loss of quantum state), high error rates, limited qubit counts, and difficulty isolating quantum systems. Technologies include superconducting qubits, ion traps, photonic systems, and topological approaches. Applications span cryptography, drug discovery, optimization, and materials science.",
                "deep_thinking": "Quantum computing represents a fundamental shift in how we model computation itself. Classical computation is bound by Church-Turing thesis constraints, operating through deterministic state transitions. Quantum computing appears to transcend these bounds through parallel exploration of solution spaces via superposition. But this raises profound questions: Does quantum advantage require exponential resources to verify? The relationship between quantum information theory and computational complexity remains incompletely understood. Wigner's friend paradox and quantum measurement problem suggest that quantum computing's foundations touch on interpretational issues in quantum mechanics itself. The error-correction threshold theorem is crucial—if physical error rates drop below a threshold, fault-tolerant quantum computation becomes possible, though this requires enormous qubit overhead. Interestingly, quantum machine learning might offer advantages, but it's unclear if quantum supremacy in learning tasks is fundamental or artifacts of current algorithms. The future may involve hybrid classical-quantum systems rather than pure quantum computing dominating."
            },
            "climate change": {
                "short": "Climate change refers to long-term shifts in Earth's climate caused primarily by human greenhouse gas emissions.",
                "long": "Climate change is driven by the enhanced greenhouse effect: human activities (burning fossil fuels, deforestation) increase atmospheric CO2, methane, and nitrous oxide. These gases trap heat, raising global temperatures approximately 1.1°C since pre-industrial times. Consequences include: rising sea levels, more extreme weather, ecosystem disruption, and agricultural challenges. The IPCC (Intergovernmental Panel on Climate Change) projects 1.5-2°C warming this century under current policies. Mitigation strategies include renewable energy adoption, efficiency improvements, carbon capture, and policy measures (carbon pricing, regulations). Adaptation involves infrastructure resilience, water management, and agricultural practices. The Paris Agreement aims to limit warming to 2°C. Scientific consensus is overwhelming—97%+ of climate scientists affirm human-caused climate change.",
                "deep_thinking": "Climate change represents a complex systems challenge of unprecedented scale. The climate system involves multiple feedback loops: ice-albedo feedback (reduced ice lowers reflectivity, accelerating warming), water vapor feedback (warmer atmosphere holds more moisture), and carbon-cycle feedback (warming reduces CO2 absorption). The Anthropocene—the geological epoch marked by human influence—reflects our species' planetary-scale impact. Critically, climate change involves moral and political dimensions beyond science: how to weigh present economic interests against future generation welfare, international justice (historically low-emission countries suffering disproportionately), and technological optimism versus precaution. The probabilistic nature of climate projections creates policy challenges—science can quantify likelihood, but acting on uncertain futures requires value judgments. Tipping points—potential irreversible transitions like thermohaline circulation collapse—add urgency and non-linearity. Solutions require unprecedented coordination across nations, sectors, and timeframes, making climate change as much a social and political challenge as a physical one."
            }
        }

    def detect_topic(self, message: str) -> Optional[str]:
        """Detect the topic from the user's message"""
        message_lower = message.lower()
        for topic in self.knowledge_base.keys():
            if topic in message_lower:
                return topic
        return None

    async def get_response(
        self,
        message: str,
        response_length: str = "medium",
        deep_thinking: bool = False,
    ) -> str:
        """Generate intelligent response based on query"""
        
        topic = self.detect_topic(message)
        
        if topic and topic in self.knowledge_base:
            responses = self.knowledge_base[topic]
            
            if deep_thinking:
                return responses.get("deep_thinking", responses.get("long"))
            elif response_length == "short":
                return responses.get("short", responses.get("medium", ""))
            else:  # long or medium
                return responses.get("long", responses.get("short", ""))
        
        # Generic response
        return self._generate_generic_response(message, response_length, deep_thinking)

    async def stream_response(
        self,
        message: str,
        response_length: str = "medium",
        deep_thinking: bool = False,
    ) -> AsyncGenerator[str, None]:
        """Stream response word by word"""
        
        full_response = await self.get_response(message, response_length, deep_thinking)
        
        # Split into words and stream them
        words = full_response.split()
        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            yield chunk
            # Small delay to simulate streaming
            await asyncio.sleep(0.01)

    def _generate_generic_response(
        self,
        message: str,
        response_length: str,
        deep_thinking: bool,
    ) -> str:
        """Generate a generic contextual response"""
        
        message_lower = message.lower()
        
        # Greeting responses
        if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "greetings"]):
            if deep_thinking:
                return "Greetings! I appreciate your politeness. Let me engage thoughtfully with any questions you might have. The act of greeting itself is fascinating from a social and evolutionary perspective—humans use greetings to establish trust and mutual recognition, behaviors that likely evolved to facilitate cooperation in social groups."
            elif response_length == "short":
                return "Hello! How can I help you today?"
            else:
                return "Hello! Welcome to SAKHA AI. I'm here to help you with questions, creative tasks, analysis, and much more. Feel free to ask me anything!"
        
        # How are you
        if "how are you" in message_lower:
            if deep_thinking:
                return "That's a thoughtful question. While I don't have subjective experiences like humans, I can reflect on my purpose. I'm functioning as intended—analyzing text, generating responses, and hopefully providing value through our conversation. The question itself touches on philosophy of mind: whether consciousness or well-being can exist in digital systems remains an open debate in cognitive science and philosophy."
            elif response_length == "short":
                return "I'm functioning well, thank you for asking! Ready to help."
            else:
                return "I appreciate you asking! I'm operating optimally and ready to assist you with any questions or tasks. How can I help you today?"
        
        # Help request
        if "help" in message_lower or message_lower.startswith("?"):
            if deep_thinking:
                return "I'm designed to provide comprehensive assistance across many domains. I can answer questions about science, technology, history, philosophy, and more; generate creative content like stories and essays; help with analysis and problem-solving; provide explanations for complex topics; and engage in meaningful dialogue. The nature of 'help' itself is multifaceted—from immediate practical assistance to deeper understanding and perspective."
            elif response_length == "short":
                return "I can help with questions, creative writing, analysis, coding, and much more!"
            else:
                return "I'm here to help with a wide range of tasks: answering questions on many topics (science, history, technology, philosophy, etc.), providing explanations and analysis, creative writing and content generation, coding and technical assistance, brainstorming ideas, and having meaningful conversations. What would you like help with?"
        
        # Code-related
        if any(code_word in message_lower for code_word in ["code", "python", "javascript", "function", "debug", "algorithm"]):
            if deep_thinking:
                return "Programming and code are fascinating from multiple perspectives. At the mechanical level, code translates human intent into executable instructions that computers process. At the design level, good code balances clarity, efficiency, and maintainability—reflecting choices about abstraction and complexity management. Algorithmically, we're often solving timeless problems (sorting, searching, optimization) with varied trade-offs between time and space complexity. The history of programming paradigms—from procedural to object-oriented to functional—reflects evolving understanding of how to structure complex systems. Debugging itself is a creative problem-solving activity. I'd be happy to help with specific code questions!"
            elif response_length == "short":
                return "I can help with coding! What programming language or problem would you like assistance with?"
            else:
                return "I can help with programming tasks including code writing, debugging, algorithm design, explaining concepts, and optimization. I'm familiar with Python, JavaScript, Java, C++, SQL, and many other languages. I can also explain data structures, design patterns, and software architecture principles. What specific coding question do you have?"
        
        # Default response
        if deep_thinking:
            return f"That's an interesting question. When I consider '{message}', I'm drawn to think about the underlying concepts and assumptions. Every question, even seemingly simple ones, often has deeper layers worthy of exploration. Without more specificity, I'd encourage you to dig deeper: What sparked this question? What would constitute a good answer for you? What are the broader implications? I'm ready to explore this topic with more detail if you'd like to elaborate."
        elif response_length == "short":
            return f"Interesting question about '{message.split()[0]}'. Can you provide more context?"
        else:
            return f"That's an interesting topic you've brought up. While I don't have specific knowledge about '{message}' in my current knowledge base, I'm ready to help if you can provide more details or context. You might want to ask about a specific aspect of this topic, and I can provide more targeted information. What would you like to know?"


# Create global instance
local_ai_service = LocalAIService()
