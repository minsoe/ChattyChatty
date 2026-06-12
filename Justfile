sync:
    uv sync --project chatty_services --all-extras
    uv sync --project packages/chatty_ai --all-extras
    uv sync --project packages/chatty_agent --all-extras
    uv sync --project packages/chatty_core --all-extras
    uv sync --project packages/chatty_test_services --all-extras

test:
    uv run --project chatty_services pytest chatty_services
    uv run --project packages/chatty_ai pytest packages/chatty_ai
    uv run --project packages/chatty_core pytest packages/chatty_core
    uv run --project packages/chatty_agent pytest packages/chatty_agent

clean:
    rm -rf chatty_services/.venv
    rm -rf packages/chatty_ai/.venv
    rm -rf packages/chatty_agent/.venv
    rm -rf packages/chatty_core/.venv
    rm -rf packages/chatty_test_services/.venv