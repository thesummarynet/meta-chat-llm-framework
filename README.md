# MetaChat Framework

MetaChat is a sophisticated AI framework that demonstrates the concept of meta-level conversation enhancement. It processes conversations through multiple AI passes to generate more effective responses.

## Core Concept

The MetaChat framework uses a two-step process:

1. **Meta-Analysis**: A "Sales Manager" AI analyzes the conversation between a user and an assistant, providing insights and advice on how to improve the interaction.

2. **Enhanced Response**: These insights are then fed to a second AI pass that generates an improved response, taking into account the advice from the "manager."

This meta-level approach allows for more strategic and contextually appropriate responses than a single-pass AI conversation.

## Features

- **Role Transformation**: Customize the roles in the conversation (e.g., "Inquirer" and "Sales Assistant")
- **Multi-stage AI Processing**: Pass conversations through multiple AI perspectives
- **Persistent Chat History**: Store and retrieve chat sessions using TinyDB
- **Modern Streamlit UI**: Clean, interactive interface for demonstration
- **Extensible Framework**: Easily add new system prompts and roles

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

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in requirements.txt

## License

MIT

## Author

Ivan D. Ivanov (pseudonym: Ivan Vega Dobrinov)