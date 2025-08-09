import requests
from django.conf import settings
from typing import Dict, Optional

class TMDBService:
    """Service class for interacting with The Movie Database (TMDB) API"""
    
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL
        
        if not self.api_key:
            raise ValueError("TMDB_API_KEY is not configured in settings")
    
    def search_movies(self, query: str, page: int = 1) -> Dict:
        """
        Search for movies by title
        
        Args:
            query: Movie title to search for
            page: Page number for pagination (default: 1)
            
        Returns:
            Dict containing search results from TMDB API
        """
        url = f"{self.base_url}/search/movie"
        params = {
            'query': query,
            'page': page
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error searching movies: {e}")
            return {'results': [], 'total_results': 0}
    
    def get_movie_details(self, tmdb_id: int) -> Optional[Dict]:
        """
        Get detailed information for a specific movie
        
        Args:
            tmdb_id: TMDB movie ID
            
        Returns:
            Dict containing movie details or None if not found
        """
        url = f"{self.base_url}/movie/{tmdb_id}"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching movie details: {e}")
            return None
    
    def get_full_poster_url(self, poster_path: str) -> str:
        """
        Convert TMDB poster path to full URL
        
        Args:
            poster_path: Relative path from TMDB API
            
        Returns:
            Full URL to poster image
        """
        if not poster_path:
            return ""
        return f"{self.image_base_url}{poster_path}"
    
    def format_movie_for_database(self, tmdb_movie: Dict) -> Dict:
        """
        Format TMDB movie data for database storage
        
        Args:
            tmdb_movie: Movie data from TMDB API
            
        Returns:
            Dict formatted for Movie model
        """
        release_date = tmdb_movie.get('release_date', '')
        year = None
        if release_date:
            try:
                year = int(release_date.split('-')[0])
            except (ValueError, IndexError):
                year = None
        
        return {
            'title': tmdb_movie.get('title', ''),
            'year': year,
            'poster_url': self.get_full_poster_url(tmdb_movie.get('poster_path', '')),
            'tmdb_id': tmdb_movie.get('id'),
            'overview': tmdb_movie.get('overview', ''),
            'release_date': tmdb_movie.get('release_date', ''),
            'vote_average': tmdb_movie.get('vote_average', 0),
            'vote_count': tmdb_movie.get('vote_count', 0),
        }