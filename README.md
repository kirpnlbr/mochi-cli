# Mochi CLI

A command-line interface for managing your Mochi Cards flashcards.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kirpnlbr/mochi-cli.git
cd mochi-cli
```

2. Install the package:
```bash
pip install -e .
```

3. Set up your Mochi API key:
```bash
export MOCHI_API_KEY=your_api_key_here
```

## Usage

### Deck Management

List all decks:
```bash
mochi deck list
```

Create a new deck:
```bash
mochi deck new "My Deck Name"
```

### Card Management

Add a new card (interactive):
```bash
mochi card add
```
This will:
1. Show you a list of your decks to choose from
2. Prompt for the front text
3. Prompt for the back text

List cards in a deck:
```bash
mochi card list
```

## Development

1. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.