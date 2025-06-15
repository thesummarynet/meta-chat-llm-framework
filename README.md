# MetaChat Framework

MetaChat is a sophisticated AI framework that demonstrates the concept of meta-level conversation enhancement. It processes conversations through multiple AI passes to generate more effective responses. This innovative approach creates a supervisory layer that guides conversational AI to produce higher quality, more contextually appropriate responses.

## How It Works

MetaChat takes a unique approach to AI conversations by adding a meta-cognitive layer to the interaction:

1. When a user sends a message, the entire conversation history is first analyzed by a supervisory AI (in the demo, a "Sales Manager")
2. This supervisor provides strategic guidance and advice on how to best respond
3. A second AI pass takes this advice and generates an enhanced response to the user
4. The user receives only the final response, but the system preserves the meta-level insights

This creates a powerful learning loop that continuously improves conversation quality while maintaining a natural user experience.

## Core Concept

The MetaChat framework uses a two-step process:

1. **Meta-Analysis**: A supervisory AI (in this demo, a "Sales Manager") analyzes the conversation between a user and an assistant, providing insights and advice on how to improve the interaction.

2. **Enhanced Response**: These insights are then fed to a second AI pass that generates an improved response, taking into account the advice from the "manager."

This meta-level approach allows for more strategic and contextually appropriate responses than a single-pass AI conversation. While the demo implements a sales scenario, the framework is designed to be adaptable to any context where expert oversight would improve conversation quality.

## Features

- **Role Transformation**: Customize the roles in the conversation (e.g., "Inquirer" and "Sales Assistant")
- **Multi-stage AI Processing**: Pass conversations through multiple AI perspectives
- **Persistent Chat History**: Store and retrieve chat sessions using TinyDB
- **Modern Streamlit UI**: Clean, interactive interface for demonstration
- **Extensible Framework**: Easily add new system prompts and roles

## Use Cases

The MetaChat framework can be applied to numerous scenarios beyond the sales demo included in this repository:

### Customer Service Optimization
- **Meta Role**: Customer Experience Manager
- **Function**: Analyze support conversations to suggest more empathetic responses, identify missed opportunities to resolve issues, and guide support agents toward faster resolution

### Technical Support Enhancement
- **Meta Role**: Senior Technical Advisor
- **Function**: Review technical support conversations to identify missing troubleshooting steps, suggest clearer explanations of complex concepts, and ensure accurate information is provided

### Educational Tutoring
- **Meta Role**: Master Educator
- **Function**: Analyze tutoring sessions to identify knowledge gaps, suggest better teaching approaches, and recommend personalized learning paths

### Healthcare Communication
- **Meta Role**: Clinical Communication Specialist
- **Function**: Review patient interactions to ensure medical information is presented clearly, empathetically, and accurately while maintaining appropriate bedside manner

### Legal Consultation
- **Meta Role**: Senior Partner
- **Function**: Provide oversight on legal consultations to ensure comprehensive advice, appropriate risk disclosure, and client-friendly explanations of complex legal concepts

### Therapy and Counseling
- **Meta Role**: Clinical Supervisor
- **Function**: Guide therapeutic conversations with best practices, ensure appropriate therapeutic techniques are employed, and maintain ethical boundaries

Each of these scenarios leverages the same core framework, with only the system prompts needing to be customized for the specific domain.

## Project Structure

```
metachat/
├── app.py                 # Main application entry point
├── config.py              # Configuration settings
├── meta_framework.py      # Core framework implementation
├── requirements.txt       # Python dependencies
├── data/                  # Database storage
├── utils/
│   ├── chat_utils.py      # Chat management utilities
│   └── openai_utils.py    # OpenAI API utilities
└── ui/
    └── streamlit_app.py   # Streamlit user interface
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/thesummarynet/meta-chat-llm-framework
   cd meta-chat-llm-framework
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Alternatively, you can provide your API key in the Streamlit interface.

## Usage

Run the application:

```bash
python app.py
```

This will start the Streamlit interface. You can then:

1. Create a new chat session
2. Configure custom roles for the conversation
3. Send messages as the user
4. See the enhanced AI responses
5. Toggle the display of "Sales Manager" insights

## Extending the Framework

You can add new system prompts in the `config.py` file or through the `add_system_prompt` method in the `MetaChat` class. This allows you to create different meta-perspectives beyond the default sales scenario.

### Adding a New Meta-Perspective

To implement a new use case, follow these steps:

1. **Define new system prompts**: Create at least two new system prompts:
   - One for the meta-level supervisor role (e.g., "Technical Support Manager")
   - One for the enhanced assistant role (e.g., "Enhanced Technical Support Agent")

2. **Add prompts to the framework**:
   ```python
   metachat = MetaChat()
   metachat.add_system_prompt(
       prompt_id=3,
       name="Technical Support Manager",
       message="You are a technical support manager reviewing conversations...",
       model="gpt-4o"
   )
   metachat.add_system_prompt(
       prompt_id=4,
       name="Enhanced Technical Support Agent",
       message="You are a technical support agent who has received advice...",
       model="gpt-4o"
   )
   ```

3. **Customize role names**: Update the user interface to reflect the new roles:
   ```python
   st.session_state.user_role = "Customer with Technical Issue"
   st.session_state.assistant_role = "Technical Support Agent"
   ```

The framework's architecture is designed to be domain-agnostic, making it adaptable to virtually any scenario where expert oversight would improve conversation quality.

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in requirements.txt

## License

MIT

## Author

Ivan D. Ivanov (aka Ivan Vega Dobrinov)