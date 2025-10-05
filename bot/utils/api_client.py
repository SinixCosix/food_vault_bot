import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
from decouple import config


class APIClient:
    """Client for interacting with the Django REST API from the bot"""
    
    def __init__(self):
        self.base_url = config('API_BASE_URL', default='http://localhost:8000/api')
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to the API"""
        if not self.session:
            raise RuntimeError("APIClient must be used as async context manager")
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with self.session.request(method, url, json=data) as response:
                # No content
                if response.status == 204:
                    return {}
                content_type = response.headers.get('Content-Type', '')
                # Prefer JSON when content-type is JSON
                if 'application/json' in content_type or content_type.endswith('+json'):
                    result = await response.json()
                else:
                    # Fallback to text for non-JSON responses (e.g., HTML errors)
                    text = await response.text()
                    if response.status >= 400:
                        raise Exception(f"API Error {response.status}: {text}")
                    # For successful non-JSON, return empty payload with raw text
                    return {'raw': text}
                
                if response.status >= 400:
                    raise Exception(f"API Error {response.status}: {result.get('error', result)}")
                
                return result
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
    
    async def create_product(self, category: str, variant: str, telegram_id: int, 
                           username: str = '', flavors: List[str] = None, 
                           groups: List[str] = None, ratings: Optional[List[Dict[str, Any]]] = None,
                           comments: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Create a new product with optional nested ratings and comments"""
        data = {
            'category': category,
            'variant': variant,
            'telegram_id': telegram_id,
            'username': username,
            'flavors': flavors or [],
            'groups': groups or []
        }
        if ratings is not None:
            data['ratings'] = ratings
        if comments is not None:
            data['comments'] = comments
        return await self._make_request('POST', 'products/', data)
    
    async def get_products(self, category: Optional[str] = None, 
                          group: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get products with optional filtering"""
        params = {}
        if category:
            params['category'] = category
        if group:
            params['group'] = group
        
        endpoint = 'products/'
        if params:
            query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
            endpoint += f"?{query_string}"
        
        return await self._make_request('GET', endpoint)
    
    async def update_product(self, product_id: int, **kwargs) -> Dict[str, Any]:
        """Update an existing product"""
        return await self._make_request('PUT', f'products/{product_id}/', kwargs)
    
    async def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        await self._make_request('DELETE', f'products/{product_id}/')
        return True
    
    async def add_rating(self, product_id: int, telegram_id: int, rating: int) -> Dict[str, Any]:
        """Add or update a rating for a product"""
        data = {
            'product_id': product_id,
            'telegram_id': telegram_id,
            'rating': rating
        }
        return await self._make_request('POST', 'products/ratings/', data)
    
    async def add_comment(self, product_id: int, telegram_id: int, comment: str) -> Dict[str, Any]:
        """Add a comment to a product"""
        data = {
            'product_id': product_id,
            'telegram_id': telegram_id,
            'comment': comment
        }
        return await self._make_request('POST', 'products/comments/', data)


# Convenience functions for bot handlers
async def create_product_from_bot_data(bot_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a product from bot state data"""
    async with APIClient() as client:
        return await client.create_product(
            category=bot_data.get('category', ''),
            variant=bot_data.get('variant', ''),
            telegram_id=bot_data.get('telegram_id'),
            username=bot_data.get('username', ''),
            flavors=bot_data.get('flavors', []),
            groups=bot_data.get('groups', []),
            ratings=bot_data.get('ratings'),
            comments=bot_data.get('comments')
        )


async def save_rating_from_bot(product_id: int, telegram_id: int, rating: int) -> Dict[str, Any]:
    """Save a rating from bot interaction"""
    async with APIClient() as client:
        return await client.add_rating(product_id, telegram_id, rating)


async def save_comment_from_bot(product_id: int, telegram_id: int, comment: str) -> Dict[str, Any]:
    """Save a comment from bot interaction"""
    async with APIClient() as client:
        return await client.add_comment(product_id, telegram_id, comment)

