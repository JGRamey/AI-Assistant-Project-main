Below is the list of the agents that are currently implemented:

Coding Agents:
- **`src/agents/coding/smart_contract_ai_agent.py`**: An agent that utilizes the `SmartContractManager` to interact with smart contracts, allowing for the storage and retrieval of data from the blockchain.
- **`src/agents/coding/snippet_agent.py`**: A simple agent for saving and managing code snippets in a local SQLite database.

Communication Agents:
- **`src/agents/communication/voice_agent.py`**: An agent that handles voice-to-text and text-to-speech tasks, using Mimic 3 for TTS and STT.
- **`src/agents/communication/email_agent.py`**: An agent that handles email tasks, such as sending and receiving emails.
- **`src/agents/communication/social_agent.py`**: An agent that handles social media tasks, such as posting and managing social media accounts.
- **`src/agents/communication/texts_agent.py`**: An agent that handles SMS tasks, such as sending and receiving SMS messages.




Financial Agents:
- **`src/agents/financial/financial_agent.py`**: An agent that handles financial planning tasks, such as creating retirement plans and investment strategies.
- **`src/agents/financial/expense_report.py`**: An agent that generates expense reports based on user input.
- **`src/agents/financial/portfolio_agent.py`**: An agent that manages user portfolios and provides investment advice.
- **`src/agents/financial/trading_agent.py`**: An agent that handles trading tasks, such as buying and selling stocks and cryptocurrencies.




Possible Future Agents:

Financial Agents:
- **`src/agents/financial/stock_agent.py`**: An agent that provides information about stocks and their performance.

Communication Agents:
- **`src/agents/communication/learning_agent.py`**: An agent designed to learn and store user preferences in a local SQLite database. While also helping other agents learn and store user preferences.