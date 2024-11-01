"""
Command Line Interface for Mochi Cards
"""
import os
import click
import json
from .api import MochiAPI
from typing import Optional

def get_api() -> MochiAPI:
    """Get API client instance."""
    api_key = os.getenv('MOCHI_API_KEY')
    if not api_key:
        raise click.ClickException(
            "MOCHI_API_KEY environment variable not set. "
            "Please set it with your API key from Mochi Cards."
        )
    return MochiAPI(api_key)

def format_output(data: dict) -> str:
    """Format dictionary output as pretty JSON."""
    return json.dumps(data, indent=2)

@click.group()
def cli():
    """Mochi Cards CLI - Manage your flashcards from the command line."""
    pass

# Deck commands
@cli.group()
def decks():
    """Manage decks."""
    pass

@decks.command(name='list')
@click.option('--bookmark', help='Pagination bookmark')
def list_decks(bookmark: Optional[str]):
    """List all decks."""
    try:
        result = get_api().list_decks(bookmark=bookmark)
        click.echo(format_output(result))
    except Exception as e:
        raise click.ClickException(str(e))

@decks.command(name='create')
@click.argument('name')
@click.option('--parent-id', help='Parent deck ID')
@click.option('--sort', type=int, help='Sort order')
@click.option('--archived/--not-archived', default=False, help='Whether the deck is archived')
@click.option('--show-sides/--hide-sides', default=True, help='Show both sides of cards')
@click.option('--sort-by', 
    type=click.Choice(['none', 'lexicographically', 'created-at', 'updated-at', 'retention-rate-asc', 'interval-length']),
    default='lexicographically',
    help='How to sort cards')
@click.option('--cards-view',
    type=click.Choice(['list', 'grid', 'note', 'column']),
    default='list',
    help='How to display cards')
@click.option('--review-reverse/--no-review-reverse', default=False, help='Enable reverse review')
def create_deck(name, parent_id, sort, archived, show_sides, sort_by, cards_view, review_reverse):
    """Create a new deck."""
    try:
        result = get_api().create_deck(
            name=name,
            parent_id=parent_id,
            sort=sort,
            archived=archived,
            show_sides=show_sides,
            sort_by=sort_by,
            cards_view=cards_view,
            review_reverse=review_reverse
        )
        click.echo(format_output(result))
    except Exception as e:
        raise click.ClickException(str(e))

@decks.command(name='get')
@click.argument('deck_id')
def get_deck(deck_id):
    """Get details of a specific deck."""
    try:
        result = get_api().get_deck(deck_id)
        click.echo(format_output(result))
    except Exception as e:
        raise click.ClickException(str(e))

@decks.command(name='delete')
@click.argument('deck_id')
@click.confirmation_option(prompt='Are you sure you want to delete this deck?')
def delete_deck(deck_id):
    """Delete a deck."""
    try:
        get_api().delete_deck(deck_id)
        click.echo(f"Deck {deck_id} deleted successfully.")
    except Exception as e:
        raise click.ClickException(str(e))

# Card commands
@cli.group()
def cards():
    """Manage cards."""
    pass

@cards.command(name='list')
@click.option('--deck-id', help='Filter by deck ID')
@click.option('--bookmark', help='Pagination bookmark')
@click.option('--limit', type=int, help='Number of cards to return')
def list_cards(deck_id, bookmark, limit):
    """List cards, optionally filtered by deck."""
    try:
        result = get_api().list_cards(deck_id=deck_id, bookmark=bookmark, limit=limit)
        click.echo(format_output(result))
    except Exception as e:
        raise click.ClickException(str(e))

@cards.command(name='create')
@click.option('--deck-id', required=True, help='ID of the deck to add the card to')
@click.option('--front', prompt=True, help='Front side of the card')
@click.option('--back', prompt=True, help='Back side of the card')
@click.option('--template-id', help='Template ID to use')
@click.option('--archived/--not-archived', default=False, help='Whether the card is archived')
@click.option('--review-reverse/--no-review-reverse', default=False, help='Enable reverse review')
def create_card(deck_id, front, back, template_id, archived, review_reverse):
    """Create a new card."""
    try:
        # Format content as a simple two-sided card
        content = f"# {front}\n---\n{back}"
        result = get_api().create_card(
            deck_id=deck_id,
            content=content,
            template_id=template_id,
            archived=archived,
            review_reverse=review_reverse
        )
        click.echo(format_output(result))
    except Exception as e:
        raise click.ClickException(str(e))

@cards.command(name='get')
@click.argument('card_id')
def get_card(card_id):
    """Get details of a specific card."""
    try:
        result = get_api().get_card(card_id)
        click.echo(format_output(result))
    except Exception as e:
        raise click.ClickException(str(e))

@cards.command(name='delete')
@click.argument('card_id')
@click.confirmation_option(prompt='Are you sure you want to delete this card?')
def delete_card(card_id):
    """Delete a card."""
    try:
        get_api().delete_card(card_id)
        click.echo(f"Card {card_id} deleted successfully.")
    except Exception as e:
        raise click.ClickException(str(e))

@cards.command(name='attach')
@click.argument('card_id')
@click.argument('file_path', type=click.Path(exists=True))
def add_attachment(card_id, file_path):
    """Add an attachment to a card."""
    try:
        result = get_api().add_attachment(card_id, file_path)
        click.echo(format_output(result))
    except Exception as e:
        raise click.ClickException(str(e))

# Template commands
@cli.group()
def templates():
    """Manage templates."""
    pass

@templates.command(name='list')
@click.option('--bookmark', help='Pagination bookmark')
def list_templates(bookmark):
    """List all templates."""
    try:
        result = get_api().list_templates(bookmark=bookmark)
        click.echo(format_output(result))
    except Exception as e:
        raise click.ClickException(str(e))

@templates.command(name='get')
@click.argument('template_id')
def get_template(template_id):
    """Get details of a specific template."""
    try:
        result = get_api().get_template(template_id)
        click.echo(format_output(result))
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