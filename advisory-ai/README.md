# Advisory AI

What if you could get brutally honest feedback on your business ideas from world-class advisors? What if Steve Jobs could tell you what to cut, Charlie Munger could show you how your idea fails, and Naval Ravikant could map your leverage points?

**Advisory AI** gives you exactly that - 5 AI agents inspired by legendary thinkers, each providing structured critique through their unique lens. No sugar-coating, no false encouragement, just the kind of feedback that turns good ideas into great ones.

## The Problem

You have an idea. Maybe it's a startup concept, a product feature, or a strategic pivot. You know it needs scrutiny, but your friends are too polite, your team is too invested, and hiring real advisors costs $50K+ per year.

Most feedback you get is either:
- **Too nice**: "That sounds great!" (not helpful)
- **Too vague**: "I'm not sure about the market" (not actionable)  
- **Too shallow**: Surface-level concerns without deep analysis

## The Solution

Five AI agents, each embodying the thinking patterns of legendary advisors:

- **Jobs Lens**: Ruthless simplicity and user obsession
- **Naval Lens**: Leverage, wealth creation, and first principles
- **Munger Lens**: Mental models, inversion, and avoiding stupidity
- **Indian Philosophy Lens**: Dharma, long-term thinking, and ethical frameworks
- **Ruthless Capitalist Lens**: Moats, pricing power, and competitive dynamics

Plus a **Synthesis Agent** that reconciles disagreements and creates actionable plans.

## Quick Start

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2

# Clone and setup
git clone https://github.com/anupsahoo/advisory-ai
cd advisory-ai
make setup

# Verify everything works
advisory doctor

# Get feedback on your idea
advisory critique --input examples/idea.md
```

## Usage Examples

### Full Board Critique (Default)
```bash
advisory critique --input my-idea.md --output critique.md
```
Gets feedback from all 5 agents plus synthesis.

### Single Lens Analysis
```bash
advisory critique --lens jobs --input my-idea.md
advisory critique --lens naval --input my-idea.md  
advisory critique --lens munger --input my-idea.md
```

### JSON Output for Automation
```bash
advisory critique --input my-idea.md --json --output results.json
```

### Interactive Mode
```bash
advisory critique --input my-idea.md --interactive
```
Agents ask clarifying questions before providing feedback.

## What You Get

Each agent provides:

- **Brutal One-Liner**: The harsh truth in one sentence
- **Key Questions**: What they'd ask in a real advisory meeting
- **Assumptions Analysis**: What you're taking for granted
- **Risk Assessment**: What could go wrong and why
- **Bold Move**: One counterintuitive action to consider
- **Scorecard**: Numerical ratings on key dimensions
- **30-Day Experiment**: Concrete next steps to validate/invalidate
- **Blog References**: Relevant articles from curated knowledge base

### Sample Output Structure

```markdown
# Board Critique: AI-Powered Fitness App

## Jobs Lens: Ruthless Simplicity

**Brutal Truth**: "You're building a feature factory, not solving a real problem."

**What I Would Cut**: 
- Social features (focus on individual transformation first)
- Gamification (motivation comes from results, not points)
- Multiple workout types (master one thing first)

**Key Questions**:
1. What's the one thing users will do every single day?
2. How is this 10x better than opening YouTube?
3. What would you remove if you only had 1 screen?

**Scorecard**:
- Simplicity: 3/10
- User Focus: 6/10  
- Differentiation: 4/10

**30-Day Experiment**: Build a single-feature MVP that does ONE thing perfectly.
```

## Architecture

### Local-First Design
- **Ollama Integration**: Runs completely offline with local models
- **OpenAI Fallback**: Optional API key for cloud models
- **Zero Dependencies**: No external services required
- **Privacy-First**: Your ideas never leave your machine (unless you choose cloud)

### Agent Framework
```
src/board/
├── agents/
│   ├── base.py           # Agent interface & contracts
│   ├── jobs.py           # Jobs lens implementation  
│   ├── naval.py          # Naval lens implementation
│   ├── munger.py         # Munger lens implementation
│   ├── indian_philosophy.py  # Indian philosophy lens
│   ├── ruthless_capitalist.py # Capitalist lens
│   └── synthesis.py      # Synthesis agent
├── runtime/
│   └── providers.py      # Ollama + OpenAI providers
├── scoring/
│   └── rubrics.py        # Scoring frameworks
├── retrieval/
│   └── blog_refs.py      # Blog reference matching
└── prompts/              # Agent prompt templates
```

## Configuration

### Environment Variables
```bash
# Optional: Use OpenAI instead of Ollama
export OPENAI_API_KEY="your-key-here"

# Optional: Custom Ollama endpoint  
export OLLAMA_BASE_URL="http://localhost:11434"

# Optional: Default model override
export BOARD_MODEL="llama2:13b"
```

### Blog References
The system includes a curated knowledge base (`resources/blog_index.yml`) that agents reference when providing feedback. Add your own articles:

```yaml
- title: "First Principles Thinking in Product Development"
  url: "https://yourblog.com/first-principles"
  tags: ["first-principles", "product", "strategy"]
  
- title: "Why Most Startups Fail: A Munger Analysis"  
  url: "https://yourblog.com/startup-failures"
  tags: ["startups", "mental-models", "failure"]
```

## Advanced Usage

### Custom Prompts
Modify agent behavior by editing prompt templates in `src/board/prompts/`:

```
prompts/
├── system.txt           # Base system prompt
├── jobs_lens.txt        # Jobs-specific instructions
├── naval_lens.txt       # Naval-specific instructions  
└── synthesis.txt        # Synthesis agent prompt
```

### Batch Processing
```bash
# Process multiple ideas
for idea in ideas/*.md; do
    advisory critique --input "$idea" --output "critiques/$(basename "$idea")"
done
```

### Integration with CI/CD
```yaml
# .github/workflows/idea-review.yml
- name: Review Product Ideas
  run: |
    advisory critique --input product-ideas.md --json --output review.json
    # Parse results and comment on PR
```

## Development

### Setup Development Environment
```bash
make dev
```

### Run Tests
```bash
make test
```

### Code Quality
```bash
make lint
```

### Adding New Agents
1. Create agent class in `src/board/agents/your_agent.py`
2. Implement the `Agent` interface from `base.py`
3. Add prompt template in `src/board/prompts/`
4. Register in CLI (`src/board/cli.py`)
5. Add tests in `tests/agents/`

## Troubleshooting

### Ollama Issues
```bash
# Check if Ollama is running
advisory doctor

# Install/update Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required model
ollama pull llama2
```

### Performance Optimization
- Use smaller models for faster responses: `ollama pull llama2:7b`
- Enable GPU acceleration in Ollama settings
- Use `--json` output for programmatic processing

### Common Issues

**"Model not found"**: Run `ollama pull llama2` or set `BOARD_MODEL` env var

**"Connection refused"**: Ensure Ollama is running (`ollama serve`)

**"Slow responses"**: Try smaller model or enable GPU acceleration

## Philosophy

This tool embodies the same independence philosophy as our [Atelier Lab](https://anupsahoo.dev/atelier-lab) - complete self-containment, no external dependencies, and full control over your data and processes.

Just like our 35+ thinking agents, each advisory member is designed to:
- Work independently without shared state
- Provide transparent reasoning processes  
- Operate offline-first with cloud as optional
- Give you complete ownership of the system

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- New agent lenses (e.g., Bezos, Buffett, Gandhi)
- Additional output formats (PDF, HTML, Slack)
- Integration with popular tools (Notion, Obsidian)
- Performance optimizations
- Better prompt engineering

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related Projects

- [Atelier Lab](https://github.com/anupsahoo/AtelierLabs) - 35+ independent thinking agents
- [Custom Subscription System](https://anupsahoo.dev/architecture/custom-subscription-system) - Build your own email system
- [AI Agent Frameworks](https://anupsahoo.dev/ai-landscape/ai-agent-frameworks) - Comprehensive framework comparison

---

**Built with independence in mind. No vendor lock-in, no external dependencies, no compromises.**
