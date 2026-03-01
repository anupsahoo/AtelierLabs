# AtelierLabs

What if you could have a conversation with your own thinking process? What if every decision you make could be enhanced by an intelligent system that thinks alongside you, challenges your assumptions, and helps you see what you might have missed?

Welcome to AtelierLabs - where we've built 35+ autonomous thinking agents that don't just process data, they actually think. Each agent is like having a brilliant colleague who specializes in one specific type of reasoning, available 24/7 to help you make better decisions.

## The Story Behind This Lab

Picture this: You're about to launch a new product. Traditional software would give you analytics and reports. But what if instead, you could consult with an "Assumption Breaker" that identifies the hidden beliefs driving your strategy? Or a "Second Order Thinking" agent that predicts the ripple effects of your decisions three moves ahead?

This isn't science fiction. This is what happens when you stop building software and start designing intelligence.

## Repository Structure

Each agent is a complete, independent project with enterprise-grade scaffolding:

```
AtelierLabs/
  assumption_breaker/          # First principles thinking agent
    core/                      # Internal cognitive framework
    src/assumption_breaker/    # Agent implementation
    tests/                     # Test suite
    pyproject.toml            # Dependencies & config
    Dockerfile                # Container support
    Makefile                  # Development commands
    README.md                 # Agent documentation
  
  second_order_thinking/       # Consequence prediction agent
  bias_detector/              # Cognitive bias detection
  devils_advocate/            # Logical opposition
  clarity_refiner/            # Concept clarification
  mental_model_injector/      # Mental model application
  tradeoff_analyzer/          # Tradeoff analysis
  
  # Life Engineering Agents
  weekly_direction/           # Weekly focus planning
  energy_audit/              # Energy and time analysis
  decision_weight/            # Weighted decision making
  fear_decomposer/            # Fear analysis
  discipline_reminder/        # Habit tracking
  long_term_identity/         # Identity alignment
  
  # Strategic Thinking Agents
  business_stress_tester/     # Business idea validation
  competitive_positioning/    # Competitive analysis
  narrative_framer/           # Story construction
  audience_persona/           # Persona creation
  leverage_finder/            # Leverage point identification
  anti_fragility/             # Anti-fragility analysis
  
  # Communication Intelligence Agents
  ego_filter/                 # Tone softening
  power_rewriter/             # Authority enhancement
  simplifier/                 # Complexity reduction
  influence_pattern/          # Persuasion optimization
  hook_generator/             # Opening line creation
  
  # AI Future Agents
  ai_readiness_assessor/      # AI readiness evaluation
  copilot_discipline/         # AI usage analysis
  skill_gap_predictor/        # Future skill prediction
  automation_finder/          # Automation opportunities
  ethical_risk_scanner/       # AI ethics assessment
  cognitive_load_reducer/     # Mental workload optimization
  
  # Beyond Software Agents
  digital_dharma/             # Value vs noise analysis
  silence_agent/              # Strategic quitting
  attention_protector/        # Attention management
  long_horizon/               # Future projection
  legacy_simulator/           # Legacy impact analysis
  
  # Production Governance Agent
  autonomy_gatekeeper/        # AI governance agent (full production setup)
```

## How These Agents Actually Work

Here's what makes these agents different from anything you've seen before. Each one is built like a complete startup - independent, self-sufficient, and ready to solve real problems.

**Think Like a Human, Deploy Like Software**: Every agent carries its own "brain" - a complete cognitive framework with memory, reasoning capabilities, and mental models. It's like each agent graduated from its own AI university and now works as an independent consultant.

**No Dependencies, No Drama**: Remember the frustration of software that breaks when one library updates? These agents don't have that problem. Each one is completely self-contained with its own tools, tests, and deployment setup.

**See the Thinking Process**: Unlike black-box AI that gives you answers without explanation, these agents show their work. You can see exactly how they arrived at their conclusions, what mental models they used, and how confident they are in their reasoning.

**Ready for Real Business**: Each agent comes with everything you need for production - Docker containers, command-line interfaces, and enterprise-grade configuration. You could deploy any of these agents tomorrow.

---

## Cognitive Agent Framework (CAF)

The **Cognitive Agent Framework** is the foundation for all thinking agents. It provides:

- **Base Agent Architecture**: Unified processing pipeline with memory integration
- **Mental Models Library**: First principles, second-order thinking, systems thinking, and more
- **Multi-Modal Reasoning**: Logical, analogical, causal, and probabilistic reasoning
- **Agent Memory System**: Short-term, long-term, and episodic memory capabilities
- **Communication Protocol**: Structured messaging and inter-agent collaboration
- **Orchestration Engine**: Multi-agent workflows and coordination

### Framework Usage

```python
from framework import CognitiveAgent, MentalModelsLibrary

class MyAgent(CognitiveAgent):
    def __init__(self):
        super().__init__(
            name="My Agent",
            category="cognitive",
            mental_models=[MentalModelsLibrary.FIRST_PRINCIPLES],
            description="Description of what this agent does"
        )
    
    async def process_input(self, input_data, context=None):
        # Agent-specific processing logic
        return AgentResult(...)
```

---

## Available Agents

### 🧠 Cognitive Agents (Thinking Upgrade)

| Agent | Mental Models | Purpose |
|-------|---------------|---------|
| **Assumption Breaker** | First Principles, Inversion | Identify hidden assumptions and challenge conventional wisdom |
| **Second Order Thinking** | Second-Order, Systems, Probabilistic | Predict downstream consequences and ripple effects |
| **Bias Detector** | Critical Thinking, Probabilistic | Detect cognitive biases in text and decisions |
| **Devil's Advocate** | Logical Reasoning, Inversion | Provide logical opposition to test arguments |
| **Clarity Refiner** | First Principles, Systems Thinking | Make vague ideas sharp and structured |
| **Mental Model Injector** | Multiple Models | Apply specific mental models to problems |
| **Tradeoff Analyzer** | Opportunity Cost, Systems Thinking | Analyze what you gain vs. what you sacrifice |

### 🧭 Life Engineering Agents (Life Optimization)

| Agent | Mental Models | Purpose |
|-------|---------------|---------|
| **Weekly Direction** | Pareto Principle, Goal Setting | Suggest weekly focus based on goals and priorities |
| **Energy Audit** | Pareto, Opportunity Cost | Identify energy drains and time allocation issues |
| **Decision Weight** | Decision Matrices, Expected Value | Help choose between options using weighted scoring |
| **Fear Decomposer** | Stoicism, Risk Analysis | Break fears into rational components |
| **Discipline Reminder** | Habit Formation, Systems | Monitor consistency patterns and provide reminders |
| **Long-Term Identity** | Identity-Based Habits | Check if actions align with long-term identity |

### Strategic Thinking Agents (Business Strategy)

| Agent | Mental Models | Purpose |
|-------|---------------|---------|
| **Business Stress Tester** | Premortem, Red Teaming | Attack business ideas to find weaknesses |
| **Competitive Positioning** | Competitive Analysis, Strategy | Analyze differentiation and market position |
| **Narrative Framer** | Storytelling, Psychology | Turn concepts into compelling stories |
| **Audience Persona** | Empathy Mapping, Psychology | Create detailed psychological personas |
| **Leverage Finder** | 80/20 Principle, Systems | Find highest ROI actions and leverage points |
| **Anti-Fragility** | Anti-Fragility Theory, Risk | Make systems stronger under stress |

### Communication Intelligence Agents

| Agent | Mental Models | Purpose |
|-------|---------------|---------|
| **Ego Filter** | Emotional Intelligence, NVC | Soften aggressive tone and reduce ego |
| **Power Rewriter** | Power Dynamics, Confidence | Make messages more authoritative |
| **Simplifier** | Feynman Technique, Teaching | Convert complex concepts into simple explanations |
| **Influence Pattern** | Cialdini's Principles, Psychology | Rewrite content to increase persuasion |
| **Hook Generator** | Psychology, Copywriting | Create powerful opening lines and hooks |

### AI Future Agents (Human + AI Collaboration)

| Agent | Mental Models | Purpose |
|-------|---------------|---------|
| **AI Readiness Assessor** | Change Management, Capability | Measure team AI readiness and maturity |
| **Copilot Discipline** | Prompt Engineering, Human-AI | Analyze and improve AI usage patterns |
| **Skill Gap Predictor** | Trend Analysis, Future Planning | Predict which skills will become obsolete |
| **Automation Finder** | Process Optimization, Systems | Identify repetitive tasks for automation |
| **Ethical Risk Scanner** | AI Ethics, Risk Management | Scan for AI misuse and ethical risks |
| **Cognitive Load Reducer** | Cognitive Psychology, UX | Reduce mental strain in workflows |

### Beyond Software Agents (Philosophical)

| Agent | Mental Models | Purpose |
|-------|---------------|---------|
| **Digital Dharma** | Essentialism, Value Theory | Analyze if work creates value or noise |
| **Silence Agent** | Subtraction, Strategic Quitting | Suggest what to stop doing |
| **Attention Protector** | Attention Economics, Focus | Identify and protect attention from leaks |
| **Long Horizon** | Scenario Planning, Time Horizon | Project current path 10 years forward |
| **Legacy Simulator** | Legacy Thinking, Impact | "What will people say about your work in 2040?" |

---

## Getting Started

### 1. Framework Setup

```bash
# Clone the repository
git clone https://github.com/anupsahoo/AtelierLabs.git
cd AtelierLabs

# Install framework dependencies
pip install -r requirements.txt

# Test the framework
python -c "from framework import CognitiveAgent; print('Framework ready!')"
```

### 2. Using Individual Agents

```python
# Import and use an agent
from cognitive.assumption_breaker import AssumptionBreakerAgent

async def analyze_idea():
    agent = AssumptionBreakerAgent()
    idea = "We will definitely capture 50% market share in 2 years"
    result = await agent.process(idea)
    print(f"Found {result.content['assumptions_analysis']['total_assumptions']} assumptions")

# Run the analysis
import asyncio
asyncio.run(analyze_idea())
```

### 3. Multi-Agent Workflows

```python
from framework import AgentOrchestrator

# Create orchestrator and register agents
orchestrator = AgentOrchestrator()
orchestrator.register_agent(AssumptionBreakerAgent())
orchestrator.register_agent(SecondOrderThinkingAgent())

# Create collaborative workflow
workflow_id = await orchestrator.create_collaborative_workflow(
    problem={"idea": "Launch new AI product"},
    agent_names=["Assumption Breaker", "Second Order Thinking"],
    collaboration_mode="sequential"
)

# Execute workflow
result = await orchestrator.execute_workflow(workflow_id, {"idea": "Launch new AI product"})
```

---

## Architecture Principles

1. **Unified Framework**: All agents inherit from the same base architecture
2. **Mental Models First**: Each agent applies specific mental models to problems
3. **Memory & Learning**: Agents learn from interactions and build patterns
4. **Inter-Agent Communication**: Agents can collaborate and share insights
5. **Observable Reasoning**: Every agent explains its thinking process
6. **Confidence Scoring**: Agents assess confidence in their conclusions
7. **Extensible Design**: Easy to add new mental models and reasoning methods

---

## Getting Started with Any Agent

Each agent is independent. To work with one:

1. Navigate into the agent's folder
2. Copy `.env.example` to `.env` and add your configuration (see the agent's README for details)
3. Run `make setup` to install dependencies
4. Run `make run` to execute, or `make test` to verify

Every agent README contains specific instructions, environment variables, and usage examples.

---

## Common Configuration

Most agents in this repository use LLM providers. The typical environment variables are:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | API key for OpenAI | `sk-...` |
| `OPENAI_MODEL` | Model to use | `gpt-4o` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

Each agent may have additional configuration. Refer to the `.env.example` file inside each agent's folder for the complete list.

---

## How to Navigate

Pick any agent that interests you. Open its README for context, then read the code starting from the entry point. Each agent is self-explanatory. There is no required order and no prerequisites. The repository rewards curiosity and careful reading.

---

## Author

Built by a technical leader working at the intersection of software architecture and intelligent systems. This repository is a way of sharing practical thinking about agent design through code rather than commentary.

---

## License

This repository is licensed under the MIT License.
