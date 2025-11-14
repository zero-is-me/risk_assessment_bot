import asyncio
import aiohttp
import logging
import hashlib
import json
from typing import Dict, Any, Optional
from datetime import datetime
import redis
from config.settings import settings

logger = logging.getLogger(__name__)

class APIManager:
    """Centralized API request manager with caching and retry logic"""
    
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL)
        except:
            logger.warning("Redis not available, caching disabled")
            self.redis_client = None
        
        self.rate_limits = {}
        self.session = None
    
    async def init_session(self):
        """Initialize aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    def _get_cache_key(self, url: str, params: Dict = None) -> str:
        """Generate cache key"""
        key_data = f"{url}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Get from cache"""
        if not self.redis_client:
            return None
        
        try:
            cached = self.redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except Exception as e:
            logger.warning(f"Cache retrieval error: {e}")
        
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict, ttl: int = None):
        """Save to cache"""
        if not self.redis_client:
            return
        
        try:
            ttl = ttl or settings.CACHE_TTL
            self.redis_client.setex(cache_key, ttl, json.dumps(data))
        except Exception as e:
            logger.warning(f"Cache save error: {e}")
    
    async def fetch(
        self,
        url: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        api_name: str = "generic",
        use_cache: bool = True,
        cache_ttl: Optional[int] = None
    ) -> Dict[str, Any]:
        """Make API request with retry and caching"""
        
        cache_key = self._get_cache_key(url, params or json_data)
        
        if use_cache:
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                logger.info(f"Cache HIT: {api_name}")
                return cached_data
        
        await self.init_session()
        
        headers = headers or {}
        headers.setdefault("User-Agent", "EnterpriseRiskAssessment/3.0")
        
        for attempt in range(settings.API_RETRY_ATTEMPTS):
            try:
                if method.upper() == "GET":
                    async with self.session.get(
                        url,
                        params=params,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=settings.API_TIMEOUT)
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            result = {
                                "status": "success",
                                "data": data,
                                "cached": False,
                                "timestamp": datetime.now().isoformat()
                            }
                            
                            if use_cache:
                                self._save_to_cache(cache_key, result, cache_ttl)
                            
                            return result
                
                elif method.upper() == "POST":
                    async with self.session.post(
                        url,
                        json=json_data,
                        params=params,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=settings.API_TIMEOUT)
                    ) as response:
                        if response.status in [200, 201]:
                            data = await response.json()
                            result = {
                                "status": "success",
                                "data": data,
                                "cached": False,
                                "timestamp": datetime.now().isoformat()
                            }
                            
                            if use_cache:
                                self._save_to_cache(cache_key, result, cache_ttl)
                            
                            return result
            
            except asyncio.TimeoutError:
                logger.warning(f"Timeout on {api_name} (attempt {attempt + 1})")
                if attempt < settings.API_RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(2 ** attempt)
            
            except Exception as e:
                logger.error(f"Error on {api_name}: {str(e)}")
                if attempt < settings.API_RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(2 ** attempt)
        
        return {
            "status": "failed",
            "error": f"Failed after {settings.API_RETRY_ATTEMPTS} attempts",
            "url": url,
            "cached": False,
            "timestamp": datetime.now().isoformat()
        }

api_manager = APIManager()