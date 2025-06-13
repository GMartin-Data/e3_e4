# CollibrIA - Serverless SQL Agent

## 🎯 Project Overview

CollibrIA is a serverless SQL agent that enables users to interact with databases using natural language through a chatbot interface. Built on AWS with a focus on scalability, security, and user experience.

## 🏗️ Architecture

- **Frontend**: Static HTML/CSS/JS served via CloudFront
- **Backend**: FastAPI on AWS Lambda
- **AI/ML**: Amazon Bedrock (Mistral Large / Claude)
- **Database**: Amazon RDS (MySQL)
- **Authentication**: AWS Cognito
- **Storage**: DynamoDB for conversations and feedback
- **Monitoring**: CloudWatch with custom metrics

## 🚀 Key Features

- Natural language to SQL query conversion
- Secure, read-only database access
- User authentication and session management
- Conversation history tracking
- User feedback system
- Full French language support (coming soon)
- Comprehensive monitoring and alerting

## 📋 Prerequisites

- Python 3.12
- AWS Account with Bedrock access in eu-west-3
- AWS CLI configured
- MySQL (for local development)

## 🛠️ Technology Stack

### Core

- **Package Management**: uv
- **Configuration**: pydantic-settings
- **Testing**: pytest
- **Linting/Formatting**: ruff
- **Logging**: Python's built-in logging (JSON format)

### Backend

- **Framework**: FastAPI
- **AI Agent**: LangChain with create_sql_agent
- **LLM**: Amazon Bedrock (Mistral Large)
- **Validation**: Pydantic V2

### AWS Services

- Lambda (compute)
- API Gateway (REST API)
- RDS (MySQL database)
- DynamoDB (conversation storage)
- Cognito (authentication)
- S3 + CloudFront (static hosting)
- CloudWatch (monitoring)
- SNS (alerting)

### Infrastructure as Code

- AWS SAM (Serverless Application Model) - YAML-based, no additional runtime needed

## 🏃‍♂️ Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/e3_e4.git
cd e3_e4

# Install dependencies with uv
uv sync

# Run tests
uv run pytest

# Start local development
# (Instructions coming soon)
```

## 📁 Project Structure

```
e3_e4/
├── src/
│   └── e3_e4/
│       ├── __init__.py
│       ├── agent/         # SQL agent logic
│       ├── api/           # FastAPI application
│       ├── models/        # Pydantic models
│       ├── services/      # Business logic
│       └── utils/         # Utilities
├── tests/                 # Test files
├── infrastructure/        # AWS IaC files
├── frontend/             # Static HTML/CSS/JS
├── docs/                 # Documentation
├── pyproject.toml        # Project configuration
├── README.md
└── .gitignore
```

## 🧪 Development Workflow

1. **TDD Approach**: Write tests first (Red → Green → Refactor)
2. **Branch Strategy**: Feature branches merged to main
3. **Commit Convention**: Use conventional commits
4. **Code Quality**: Enforced via pre-commit hooks

## 📊 Monitoring

The application tracks:

- **AI Metrics**: Token usage, execution time, reasoning steps
- **System Metrics**: Lambda duration, API errors, cold starts
- **Business Metrics**: User interactions, feedback scores

## 🤝 Contributing

(Guidelines coming soon)

## 📝 License

(To be determined)

## 🙏 Acknowledgments

Built as a pedagogical project to demonstrate best practices in serverless AI application development on AWS.
