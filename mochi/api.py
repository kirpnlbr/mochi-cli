from typing import Optional, Dict, List, BinaryIO
import requests
from requests.auth import HTTPBasicAuth
import os

class MochiAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('MOCHI_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided or set in MOCHI_API_KEY environment variable")
        
        self.base_url = "https://app.mochi.cards/api"
        self.auth = HTTPBasicAuth(self.api_key, "")
        
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.request(
            method=method,
            url=url,
            auth=self.auth,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

    # Deck operations
    def list_decks(self, bookmark: Optional[str] = None) -> Dict:
        params = {"bookmark": bookmark} if bookmark else None
        return self._request("GET", "decks", params=params)

    def create_deck(
        self, 
        name: str,
        parent_id: Optional[str] = None,
        sort: Optional[int] = None,
        archived: bool = False,
        show_sides: bool = True,
        sort_by: str = "lexicographically",
        cards_view: str = "list",
        review_reverse: bool = False,
    ) -> Dict:
        data = {
            "name": name,
            "parent-id": parent_id,
            "sort": sort,
            "archived?": archived,
            "show-sides?": show_sides,
            "sort-by": sort_by,
            "cards-view": cards_view,
            "review-reverse?": review_reverse
        }
        return self._request("POST", "decks", json={k: v for k, v in data.items() if v is not None})

    def get_deck(self, deck_id: str) -> Dict:
        return self._request("GET", f"decks/{deck_id}")

    def update_deck(self, deck_id: str, **kwargs) -> Dict:
        return self._request("POST", f"decks/{deck_id}", json=kwargs)

    def delete_deck(self, deck_id: str) -> None:
        self._request("DELETE", f"decks/{deck_id}")

    # Card operations
    def list_cards(self, deck_id: Optional[str] = None, bookmark: Optional[str] = None, limit: Optional[int] = None) -> Dict:
        params = {}
        if deck_id:
            params["deck-id"] = deck_id
        if bookmark:
            params["bookmark"] = bookmark
        if limit:
            params["limit"] = limit
        return self._request("GET", "cards", params=params)

    def create_card(
        self,
        deck_id: str,
        content: str,
        template_id: Optional[str] = None,
        fields: Optional[Dict] = None,
        archived: bool = False,
        review_reverse: bool = False,
        pos: Optional[str] = None,
    ) -> Dict:
        data = {
            "deck-id": deck_id,
            "content": content,
            "template-id": template_id,
            "fields": fields or {},
            "archived?": archived,
            "review-reverse?": review_reverse,
            "pos": pos
        }
        return self._request("POST", "cards", json={k: v for k, v in data.items() if v is not None})

    def get_card(self, card_id: str) -> Dict:
        return self._request("GET", f"cards/{card_id}")

    def update_card(self, card_id: str, **kwargs) -> Dict:
        return self._request("POST", f"cards/{card_id}", json=kwargs)

    def delete_card(self, card_id: str) -> None:
        self._request("DELETE", f"cards/{card_id}")

    def add_attachment(self, card_id: str, file_path: str) -> Dict:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            url = f"{self.base_url}/cards/{card_id}/attachments"
            response = requests.post(url, files=files, auth=self.auth)
            response.raise_for_status()
            return response.json()

    # Template operations
    def list_templates(self, bookmark: Optional[str] = None) -> Dict:
        params = {"bookmark": bookmark} if bookmark else None
        return self._request("GET", "templates", params=params)

    def get_template(self, template_id: str) -> Dict:
        return self._request("GET", f"templates/{template_id}")