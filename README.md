# Multi-Agent AI System Demo

A FastAPI-based multi-agent AI system with specialized agents for plant care and shopping, powered by the openai-agents library and OpenAI's GPT models.

## Features

- 🤖 **Multi-Agent Architecture**: Two specialized AI agents with distinct capabilities
- 🔗 **MCP Integration**: Connects to external MCP servers with tool filtering per agent
- 🌱 **Plant Care Agent**: Expert advice on plant health, care, and troubleshooting with local watering calculator
- 🛒 **Shopping Agent**: Product discovery and checkout assistance
- 🚀 **FastAPI Backend**: Modern, fast, and well-documented API
- 📊 **Sentry Observability**: Comprehensive error tracking, performance monitoring, and insights
- 🐳 **Docker Support**: Easy deployment with Docker and docker-compose
- 📚 **Interactive API Docs**: Built-in Swagger UI and ReDoc documentation
- 🔧 **Configurable**: Environment-based configuration management

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd empower-plant-agent-demo
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key and other settings
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up development environment (optional)**

   ```bash
   make dev-setup
   ```

   This installs pre-commit hooks for automatic code formatting and import sorting.

5. **Run the application**
   ```bash
   python main.py
   # or
   make run
   ```

The API will be available at `http://localhost:8000`

## Agents Overview

The system includes two specialized AI agents, each with their own set of tools and capabilities:

### 🌱 Plant Care Agent (`/api/v1/chat/plant`)

**Purpose**: Provides expert advice on plant health, care, and troubleshooting

**Tools Available**:

- **get-plant-care-guide** (MCP): Retrieves comprehensive plant care guides from the MCP server

**Example Usage**:

```bash
curl -X POST "http://localhost:8000/api/v1/chat/plant" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How often should I water my succulent in winter?",
    "context": {
      "plant_type": "succulent",
      "pot_size": "small",
      "season": "winter"
    }
  }'
```

### 🛒 Shopping Agent (`/api/v1/chat/shopping`)

**Purpose**: Helps users find products and complete purchases

**Tools Available**:

- **get-products** (MCP): Retrieves available products based on search criteria
- **checkout** (MCP): Processes orders and handles the checkout flow

**Example Usage**:

```bash
curl -X POST "http://localhost:8000/api/v1/chat/shopping" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need gardening tools for beginners",
    "context": {
      "budget": "50",
      "experience": "beginner"
    }
  }'
```

### Docker Deployment

1. **Build and run with docker-compose**

   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually**
   ```bash
   docker build -t plant-agent .
   docker run -p 8000:8000 --env-file .env plant-agent
   ```

## API Usage

### Endpoints

#### Health Check

```bash
GET /api/v1/health
```

#### Chat with Plant Agent

```bash
POST /api/v1/chat/plant
Content-Type: application/json

{
  "message": "My plant's leaves are turning yellow. What should I do?",
  "context": {
    "plant_type": "pothos",
    "location": "indoor",
    "light_conditions": "medium"
  }
}
```

#### Chat with Shopping Agent

```bash
POST /api/v1/chat/shopping
Content-Type: application/json

{
  "message": "I need to find gardening tools for my balcony garden",
  "context": {
    "budget": "100",
    "space": "balcony",
    "experience": "beginner"
  }
}
```

#### Agents Information

```bash
GET /api/v1/agents/info          # All agents
GET /api/v1/agent/plant/info     # Plant agent only
GET /api/v1/agent/shopping/info  # Shopping agent only
```

#### Scheduler Status

```bash
GET /api/v1/scheduler/status
```

#### List Scheduled Jobs

```bash
GET /api/v1/scheduler/jobs
```

### Example Usage

```python
import requests

# Chat with the plant agent
response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={
        "message": "How often should I water my snake plant?",
        "context": {
            "plant_type": "snake plant",
            "pot_size": "medium",
            "location": "living room"
        }
    }
)

print(response.json()["response"])
```

## Observability with Sentry

The application includes comprehensive observability through Sentry integration:

### Features

- **Error Tracking**: Automatic capture of exceptions and errors
- **Performance Monitoring**: Transaction tracing for API requests and agent processing
- **Custom Context**: Plant query context and metadata for better debugging
- **Breadcrumbs**: Detailed execution flow tracking
- **Release Tracking**: Version-based error tracking and deployment monitoring

### Setup

1. **Create a Sentry account** at [sentry.io](https://sentry.io)

2. **Create a new project** for your Python/FastAPI application

3. **Get your DSN** from the project settings

4. **Configure environment variables**:

   ```bash
   SENTRY_DSN=https://your-dsn@sentry.io/project-id
   SENTRY_ENVIRONMENT=production  # or development, staging, etc.
   SENTRY_TRACES_SAMPLE_RATE=1.0  # 100% of transactions (adjust for production)
   SENTRY_PROFILES_SAMPLE_RATE=1.0  # 100% profiling (adjust for production)
   ```

5. **For production**, consider reducing sample rates:
   ```bash
   SENTRY_TRACES_SAMPLE_RATE=0.1  # 10% of transactions
   SENTRY_PROFILES_SAMPLE_RATE=0.1  # 10% profiling
   ```

### Monitoring Features

- **Automatic Error Tracking**: All exceptions are automatically captured
- **API Performance Monitoring**: FastAPI routes are automatically traced
- **Database Query Tracing**: Automatic database performance monitoring
- **HTTP Request Tracking**: Outbound HTTP requests are automatically traced
- **Logging Integration**: Error-level logs are sent as Sentry events

## Configuration

Configure the application using environment variables or the `.env` file:

| Variable                      | Description                        | Default                       |
| ----------------------------- | ---------------------------------- | ----------------------------- |
| `OPENAI_API_KEY`              | OpenAI API key                     | Required                      |
| `OPENAI_MODEL`                | OpenAI model to use                | `gpt-4`                       |
| `API_HOST`                    | Host to bind the server            | `0.0.0.0`                     |
| `API_PORT`                    | Port to bind the server            | `8000`                        |
| `SECRET_KEY`                  | Secret key for security            | `your-secret-key-change-this` |
| `MAX_TOKENS`                  | Maximum tokens per response        | `1000`                        |
| `TEMPERATURE`                 | AI response creativity (0-1)       | `0.7`                         |
| `MCP_SERVER_URL`              | MCP server URL for tools           | `https://...`                 |
| `SENTRY_DSN`                  | Sentry DSN for error tracking      | Optional                      |
| `SENTRY_ENVIRONMENT`          | Sentry environment name            | `development`                 |
| `SENTRY_TRACES_SAMPLE_RATE`   | Performance monitoring sample rate | `1.0`                         |
| `SENTRY_PROFILES_SAMPLE_RATE` | Profiling sample rate              | `1.0`                         |

## Project Structure

```
empower-plant-agent-demo/
├── app/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── plant_agent.py  # Plant empowerment agent using openai-agents
│   └── api/
│       ├── __init__.py
│       ├── auth.py         # Authentication utilities
│       ├── models.py       # Pydantic models
│       └── routes.py       # API routes
├── config.py               # Configuration management
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
└── README.md             # This file
```

## Development

### Development Setup

For the best development experience with automatic import sorting and code formatting:

1. **Install development dependencies**:

   ```bash
   make dev-setup
   ```

2. **VS Code users**: The project includes VS Code settings for automatic import sorting and formatting on save.

3. **Manual formatting**:
   ```bash
   make format      # Format code with black and sort imports
   make lint        # Run linting checks
   make sort-imports # Sort imports only
   ```

### Running Tests

```bash
pytest
# or
make test
```

### Code Quality Tools

The project uses several tools to maintain code quality:

- **isort**: Automatic import sorting (configured to work with black)
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking
- **pre-commit**: Git hooks for automatic code quality checks

### Available Make Commands

```bash
make install      # Install dependencies
make dev-setup    # Set up development environment
make format       # Format code and sort imports
make lint         # Run all linting checks
make test         # Run tests
make run          # Run the application
make docker-run   # Run with Docker
make clean        # Clean up generated files
```

### Adding New Agents

1. Create a new agent module using `openai_agents.Agent` directly as a module variable:

   ```python
   # app/agents/my_agent.py
   from openai_agents import Agent, Runner

   # Create agent as module variable
   my_agent = Agent(
       name="MyAgent",
       instructions="You are a helpful assistant specialized in...",
       model="gpt-4"
   )

   async def process_message(message: str) -> str:
       result = await Runner.run(my_agent, message)
       return result.final_output
   ```

2. Import and use in `app/api/routes.py`:

   ```python
   from app.agents.my_agent import my_agent, process_message
   ```

3. Update the main application to include new endpoints

## API Documentation

Once the application is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue in the repository or contact the maintainers.

---

Happy plant parenting! 🌿
