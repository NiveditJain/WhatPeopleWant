<p align="center">
  <a href="https://x.com/peoplewant_">
    <img src="https://img.shields.io/twitter/follow/peoplewant_?style=social" alt="Follow on X">
  </a>
  <a href="./LICENSE">
    <img src="https://img.shields.io/github/license/NiveditJain/WhatPeopleWant" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Made%20with-Python-blue" alt="Made with Python">
  <img src="https://img.shields.io/badge/Docker-Compose-blue" alt="Docker Compose">
  <a href="https://github.com/exospherehost/exospherehost">
    <img src="https://img.shields.io/badge/Built%20on-exosphere.host-4B77FF" alt="Built on Exosphere">
  </a>
</p>

# WhatPeopleWant

🚀 **Discover What People Actually Want**

An AI-powered agent that scours Hacker News discussions to uncover real problems people are begging to have solved. Every 2 hours, we identify high-impact opportunities and share them on [X (Twitter)](https://x.com/peoplewant_) to help builders, makers, and entrepreneurs find their next big thing.

**Built with ❤️ by builders, for builders** - Powered by [exosphere.host](https://exosphere.host)

## How It Works

We scrape and analyze discussions from Hacker News to identify what people are asking for, what is missing, or what is underserved by current tools in the market. Using this data, a large language model (LLM) generates actionable problem statements for builders. The agent surfaces real needs and opportunities based on what the community is talking about right now.

This project depends upon the [Hacker News API](https://github.com/HackerNews/API) exposed by Y Combinator, which provides near real-time access to public Hacker News data through Firebase.

## Getting Started

### Option 1: Docker Compose (Recommended)

The easiest way to run WhatPeopleWant is using Docker Compose, which sets up all required services including MongoDB, Exosphere State Manager, and the application runners.

1. **Clone the repository:**
   ```
   git clone https://github.com/NiveditJain/WhatPeopleWant.git
   cd WhatPeopleWant
   ```

2. **Set up environment variables:**
   
   Create a `.env` file in the project root with the following variables:

   ```env
   # OpenAI Configuration
   # Get your API key from https://platform.openai.com/api-keys
   OPENAI_KEY=your_openai_key_here
   # For Azure OpenAI, use your Azure endpoint URL
   # For OpenAI, use https://api.openai.com/v1
   OPENAI_ENDPOINT=https://api.openai.com/v1

   # AWS SES Configuration (for email notifications)
   # Get your AWS credentials from AWS IAM Console
   AWS_SES_ACCESS_KEY=your_aws_ses_access_key_here
   AWS_SES_SECRET_KEY=your_aws_ses_secret_key_here
   # AWS region for SES (e.g., us-east-1, us-west-2, eu-west-1)
   AWS_SES_REGION=us-east-1
   # SES endpoint for your region (e.g., https://email.us-east-1.amazonaws.com)
   AWS_SES_REGION_ENDPOINT=https://email.us-east-1.amazonaws.com
   # Email address to send notifications from (must be verified in SES)
   AWS_SES_EMAIL=from@yourdomain.com
   # Comma-separated list of email addresses to receive notifications
   TO_EMAILS=to1@yourdomain.com,to2@yourdomain.com
   ```

   **Note:** The following variables are automatically configured by Docker Compose:
   - `MONGO_URI`: Set to connect to the MongoDB container
   - `EXOSPHERE_STATE_MANAGER_URI`: Set to connect to the state manager container  
   - `EXOSPHERE_API_KEY`: Set to the default API key for the state manager

3. **Start the application:**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - MongoDB database
   - Exosphere State Manager
   - Exosphere Dashboard (accessible at http://localhost:3000)
   - 4 runner instances for processing
   - Registration and scheduler services

4. **Monitor the application:**
   ```bash
   docker-compose logs -f
   ```

5. **Access the dashboard:**
   Open your browser and navigate to http://localhost:3000

### Option 2: Local Development

For local development, you can run the application directly on your machine.

1. **Clone the repository:**
   ```
   git clone https://github.com/NiveditJain/WhatPeopleWant.git
   cd WhatPeopleWant
   ```

2. **Install dependencies using [uv](https://github.com/astral-sh/uv):**
   ```
   uv sync
   ```

3. **Set environment variables:**

   Create a `.env` file in the project root (or set these variables in your environment) with the following keys:

   ```env
   # MongoDB Configuration
   MONGO_URI=your_mongo_connection_string

   # Exosphere Configuration
   EXOSPHERE_STATE_MANAGER_URI=your_state_manager_uri
   EXOSPHERE_API_KEY=your_api_key

   # OpenAI Configuration
   # Get your API key from https://platform.openai.com/api-keys
   OPENAI_KEY=your_openai_key_here
   # For Azure OpenAI, use your Azure endpoint URL
   # For OpenAI, use https://api.openai.com/v1
   OPENAI_ENDPOINT=https://api.openai.com/v1

   # AWS SES Configuration (for email notifications)
   # Get your AWS credentials from AWS IAM Console
   AWS_SES_ACCESS_KEY=your_aws_ses_access_key_here
   AWS_SES_SECRET_KEY=your_aws_ses_secret_key_here
   # AWS region for SES (e.g., us-east-1, us-west-2, eu-west-1)
   AWS_SES_REGION=us-east-1
   # SES endpoint for your region (e.g., https://email.us-east-1.amazonaws.com)
   AWS_SES_REGION_ENDPOINT=https://email.us-east-1.amazonaws.com
   # Email address to send notifications from (must be verified in SES)
   AWS_SES_EMAIL=from@yourdomain.com
   # Comma-separated list of email addresses to receive notifications
   TO_EMAILS=to1@yourdomain.com,to2@yourdomain.com
   ```

   Replace the placeholder values with your actual credentials.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License

## Acknowledgements

Built, hosted, and sponsored by [exosphere.host](https://exosphere.host)

---

Made with ❤️ by builders for builders