import os
import click
from typing import Optional, List, Dict
from .api import MochiAPI

def get_api() -> MochiAPI:
    """Get API client instance."""
    api_key = os.getenv('MOCHI_API_KEY')
    if not api_key:
        raise click.ClickException(
            "MOCHI_API_KEY environment variable not set. "
            "Please set it with your API key from Mochi Cards."
        )
    return MochiAPI(api_key)

def select_deck(api: MochiAPI) -> str:
    decks = api.list_decks()['docs']
    if not decks:
        raise click.ClickException("No decks found. Create one first with 'mochi deck new'")
    
    click.echo("\nAvailable decks:")
    for idx, deck in enumerate(decks, 1):
        click.echo(f"{idx}. {deck['name']}")
    
    while True:
        choice = click.prompt("\nSelect deck number", type=int)
        if 1 <= choice <= len(decks):
            return decks[choice-1]['id']
        click.echo("Invalid choice. Please try again.")

@click.group()
def cli():
    pass

# Simplified deck commands
@cli.group(name='deck')
def deck_cmd():
    pass

@deck_cmd.command(name='list')
def list_decks():
    try:
        decks = get_api().list_decks()['docs']
        if not decks:
            click.echo("No decks found")
            return
        
        click.echo("\nYour Decks:")
        for deck in decks:
            click.echo(f"• {deck['name']}")
    except Exception as e:
        raise click.ClickException(str(e))

@deck_cmd.command(name='new')
@click.argument('name')
def create_deck(name: str):
    try:
        deck = get_api().create_deck(name=name)
        click.echo(f"Created deck: {deck['name']}")
    except Exception as e:
        raise click.ClickException(str(e))

# Simplified card commands
@cli.group(name='card')
def card_cmd():
    pass

@card_cmd.command(name='add')
@click.option('--deck-id', help='Deck ID (if not provided, will show deck selection)')
def add_card(deck_id: Optional[str]):
    try:
        api = get_api()
        
        # Get deck ID through selection if not provided
        if not deck_id:
            deck_id = select_deck(api)
        
        # Get card content
        front = click.prompt("Front of card")
        back = click.prompt("Back of card")
        
        # Create the card
        card = api.create_card(
            deck_id=deck_id,
            content=f"# {front}\n---\n{back}"
        )
        
        click.echo("\n✨ Card created successfully!")
        click.echo(f"Front: {front}")
        click.echo(f"Back: {back}")
    
    except Exception as e:
        raise click.ClickException(str(e))

@card_cmd.command(name='list')
@click.option('--deck-id', help='Deck ID (if not provided, will show deck selection)')
def list_cards(deck_id: Optional[str]):
    """List cards in a deck"""
    try:
        api = get_api()
        
        # Get deck ID through selection if not provided
        if not deck_id:
            deck_id = select_deck(api)
        
        cards = api.list_cards(deck_id=deck_id)['docs']
        if not cards:
            click.echo("No cards found in this deck")
            return
        
        click.echo("\nCards in deck:")
        for card in cards:
            # Extract front content (everything before ---)
            content = card['content'].split('---')[0].strip()
            if content.startswith('# '):
                content = content[2:]  # Remove Markdown header
            click.echo(f"• {content}")
    
    except Exception as e:
        raise click.ClickException(str(e))

def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)

if __name__ == '__main__':
    main()