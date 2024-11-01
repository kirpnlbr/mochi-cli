# Mochi CLI

A command-line interface for interacting with the Mochi Cards API.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mochi-cli.git
cd mochi-cli
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install the package in development mode:
```bash
pip install -e .
```

4. Set up your environment:
```bash
cp .env.example .env
# Edit .env and add your Mochi API key
```

## Usage

Basic commands:

```bash
# List all decks
mochi decks list

# Create a new deck
mochi decks create "My New Deck" --description "Description"

# Create a card
mochi cards create --deck-id <deck_id> --front "Front text" --back "Back text"
```

## Development

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
pytest
```

## License

MIT