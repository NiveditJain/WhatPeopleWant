# WhatPeopleWant
Agent to help builders find what to build (build on exosphere.host)
WhatPeopleWant is an intelligent agent designed to help builders, makers, and entrepreneurs discover high-impact problems to solve, leveraging the power of [exosphere.host](https://exosphere.host).

## How It Works

We scrape and analyze discussions from Hacker News to identify what people are asking for, what is missing, or what is underserved by current tools in the market. Using this data, a large language model (LLM) generates actionable problem statements for builders. The agent surfaces real needs and opportunities based on what the community is talking about right now.

This project depends upon the [Hacker News API](https://github.com/HackerNews/API) exposed by Y Combinator, which provides near real-time access to public Hacker News data through Firebase.

## Getting Started

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

   ```
   EXOSPHERE_STATE_MANAGER_URI=your_state_manager_uri
   EXOSPHERE_API_KEY=your_api_key
   MONGO_URI=your_mongo_connection_string
   ```

   Replace `your_state_manager_uri`, `your_api_key`, and `your_mongo_connection_string` with your actual credentials.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License

## Acknowledgements

Built, hosted, and sponsored by [exosphere.host](https://exosphere.host)

---

Made with ❤️ by builders for builders