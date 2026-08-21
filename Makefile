.PHONY: help dev run setup target

target: help

setup:
	@mkdir -p instance
	@echo "SECRET_KEY = '$$(openssl rand -base64 32)'" > ./instance/config.py

dev:
	@uv run flask run

run:
	@uv run main.py

help:
	@echo "Project Name: MPR"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "  targets:"
	@echo "    dev: Development run"
	@echo "         Runs the project in development mode."
	@echo ""
	@echo "    run: Production run"
	@echo "         Runs the project in production mode."
	@echo ""
	@echo "  setup: Setup project"
	@echo "         Creates instance directory and generates secret key."
	@echo ""
	@echo "   help: Help"
	@echo "         Shows this message."
