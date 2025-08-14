# Playwright CI Flow

This project is a multi-container application that uses Docker Compose to orchestrate several services, including a React frontend, a Node.js backend, a Python-based MCP service, a Python-based LLM service, and a Node.js-based Playwright testing service.

## Getting Started

To get started, you will need to have Docker and Docker Compose installed on your machine. Once you have those installed, you can clone this repository and run the following command to start all the services:

```
docker-compose up -d
```

This will start all the services in the background. You can then access the frontend by navigating to `http://localhost:3000` in your browser.

## Services

*   **Frontend:** A React application that serves as the user interface for the application.
*   **Backend:** A Node.js application that serves as the backend for the application.
*   **MCP Service:** A Python application that provides a set of services that can be used by the backend.
*   **LLM Service:** A Python application that provides a large language model that can be used by the backend.
*   **Playwright Service:** A Node.js application that can be used to run Playwright tests.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

