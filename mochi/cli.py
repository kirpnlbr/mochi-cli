import os
import click
from typing import Optional, List, Dict
from .api import MochiAPI

def get_api() -> MochiAPI:
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

@cli.group(name='card')
def card_cmd():
    pass

@card_cmd.command(name='add')
@click.option('--deck-id', help='Deck ID (if not provided, will show deck selection)')
def add_card(deck_id: Optional[str]):
    """Add new cards (interactive) - keeps adding until you're done"""
    try:
        api = get_api()
        
        if not deck_id:
            deck_id = select_deck(api)
        
        cards_added = 0
        
        while True:
            
            if cards_added > 0:
                click.echo(f"\n✨ Cards added so far: {cards_added}\n")
            
            front = click.prompt("Front of card (or 'q' to quit)")
            
            if front.lower() == 'q':
                break
            
            back = click.prompt("Back of card")
            
            card = api.create_card(
                deck_id=deck_id,
                content=f"# {front}\n---\n{back}"
            )
            
            cards_added += 1
            
            click.echo("\n✅ Card added successfully!")
            click.echo(f"Front: {front}")
            click.echo(f"Back: {back}")
            
            if not click.confirm("\nAdd another card?", default=True):
                break
        
        if cards_added > 0:
            click.echo(f"\n🎉 Added {cards_added} cards to your deck!")
        
    except Exception as e:
        raise click.ClickException(str(e))

@card_cmd.command(name='list')
@click.option('--deck-id', help='Deck ID (if not provided, will show deck selection)')
def list_cards(deck_id: Optional[str]):
    try:
        api = get_api()
        
        if not deck_id:
            deck_id = select_deck(api)
        
        cards = api.list_cards(deck_id=deck_id)['docs']
        if not cards:
            click.echo("No cards found in this deck")
            return
        
        click.echo("\nCards in deck:")
        for card in cards:
            content = card['content'].split('---')[0].strip()
            if content.startswith('# '):
                content = content[2:]
            click.echo(f"• {content}")
    
    except Exception as e:
        raise click.ClickException(str(e))

def main():
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)

if __name__ == '__main__':
    main()