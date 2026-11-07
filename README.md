# 🌦️ AI Weather Agent

An AI-powered weather assistant built with Python, OpenRouter LLMs, and the Open-Meteo API. The agent understands natural-language queries, identifies when weather information is required, calls an external weather API through a Python tool, and generates human-readable responses.

It also supports conversational context, allowing users to ask follow-up questions without repeating the city name.

## ✨ Features

- **LLM Integration:** Uses OpenRouter with an OpenAI-compatible Python SDK.
- **Function Calling:** Allows the LLM to decide when to execute the weather tool.
- **Live Weather Data:** Retrieves current weather information using Open-Meteo.
- **Geocoding:** Converts city names into geographical coordinates.
- **Conversation History:** Maintains context during an active session.
- **Multilingual Queries:** Understands English, Hindi, and Hinglish queries.
- **Error Handling:** Handles invalid cities, connection failures, timeouts, and API errors.
- **Token Monitoring:** Displays prompt, completion, and total token consumption.
- **Model Tracking:** Displays the actual LLM selected by OpenRouter.

## 🏗️ Architecture

The application follows a simple tool-calling architecture.

```text
                 USER
                   |
                   v
              agent.py
                   |
                   v
              OPENROUTER
                (LLM)
                   |
             Tool Decision
                   |
                   v
             Tool Dispatcher
                   |
                   v
             weather_tool.py
                   |
                   v
              OPEN-METEO
                   |
             Weather Data
                   |
                   v
              OPENROUTER
                   |
                   v
          Natural Language Response
                   |
                   v
                  USER
```

### How It Works

1. The user submits a natural-language weather query.
2. The LLM interprets the request and decides whether to call the weather tool.
3. The Python application executes the requested function.
4. The weather tool retrieves geographical coordinates and current weather information.
5. The structured weather data is returned to the LLM.
6. The LLM generates a natural-language response.
7. The application displays the response along with API usage information.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| OpenRouter | LLM API access and model routing |
| OpenAI Python SDK | LLM communication and function calling |
| Open-Meteo | Weather and geocoding data |
| Requests | HTTP API communication |
| Python-dotenv | Environment variable management |
| JSON | Structured tool definitions and API responses |

## 📁 Project Structure

```text
ai-weather-agent/
│
├── src/
│   ├── agent.py
│   ├── weather_tool.py
│   ├── test_ai.py
│   ├── test_connection.py
│   └── test_weather.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/devaamirreza/ai-weather-agent.git
```

### 2. Navigate to the project directory

```bash
cd ai-weather-agent
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

For Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root.

Copy the contents of `.env.example`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Replace the placeholder with your OpenRouter API key.

You can obtain an API key through OpenRouter.

## 🚀 Running the Application

Execute the following command from the project root:

```bash
python src/agent.py
```

The application will start an interactive terminal session.

Type `exit` to terminate the conversation.

## 💬 Example Interaction

```text
AI Weather Agent
------------------------------

You: Patna ka mausam batao bhai

Fetching weather data...

Weather Assistant:

Patna is currently experiencing clear skies.

Temperature: 27.4°C
Feels Like: 29.5°C
Humidity: 55%
Wind Speed: 4.1 km/h
Cloud Cover: 0%
Precipitation: 0 mm

------------------------------

You: What about Delhi?

Fetching weather data...

Weather Assistant:

Delhi is currently experiencing clear skies.

Temperature: 27.7°C
Humidity: 51%
Wind Speed: 5.3 km/h

------------------------------

You: exit

Weather Agent: Goodbye!
```

*Weather values above are illustrative sample output, not guaranteed live conditions.*

## 📊 API Usage Monitoring

The application tracks token consumption for both LLM interactions:

- Tool selection
- Final response generation

It displays:

- Model name
- Prompt tokens
- Completion tokens
- Total tokens

Since the application uses OpenRouter's `openrouter/free` routing option, the actual model may vary between requests.

## 🌐 APIs Used

### OpenRouter

Used for accessing LLMs and enabling function/tool calling.

### Open-Meteo

Used for retrieving geographical coordinates and current weather information.

Open-Meteo provides the weather and geocoding endpoints used by this project.

## 🔐 Security

- API keys are stored in environment variables.
- The `.env` file is excluded through `.gitignore`.
- `.env.example` provides a template for configuration.
- The actual API key should never be committed to version control.

## 🔮 Future Enhancements

- Weather forecasts for upcoming days.
- Temperature and weather comparisons across multiple cities.
- Persistent conversation memory.
- Improved tool orchestration and error handling.
- Web-based user interface.
- Weather visualizations and charts.
- Docker-based deployment.

## 👨‍💻 Author

**MD Aamir Reza**

AI-enabled Automation | Python | Data Analytics | Power Platform

---

*Built as a hands-on project to explore LLM integration, function calling, external APIs, and practical AI agent development.*