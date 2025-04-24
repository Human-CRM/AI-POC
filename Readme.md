# Alfred

AI-chatbot to enrich company and clients data !

## How to use:

Create a `.env` file (You can see `.env.example`):

```
ANTHROPIC_API_KEY="Your Anthropic Key"
TAVILY_API_KEY="Your Tavily Key"
APOLLO_API_KEY="Your Apollo.io Key"
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_HOST="https://cloud.langfuse.com"
```

Go to the root of the repo and start the project with docker compose

```
cd <Path/To/The/Repo>

docker compose up --build
```