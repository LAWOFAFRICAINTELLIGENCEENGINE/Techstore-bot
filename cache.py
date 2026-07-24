"""
=========================================================
TechStore-bot Super-System
cache.py
=========================================================

Central cache manager.

Responsibilities

- Memory cache
- Disk cache
- AI response cache
- Database cache
- File cache
- Cache expiration
- Cache cleanup
- Cache statistics
- Future Redis support
- Future distributed cache

=========================================================
"""

# =====================================================
# IMPORTS
# =====================================================

import os
import json
import time
import shutil
import hashlib
import threading
import logging

from pathlib import Path
from datetime import datetime, timedelta

# =====================================================
# SETTINGS
# =====================================================

from settings import (
    CACHE_ENABLED,
    CACHE_DIRECTORY,
    CACHE_DEFAULT_TTL,
    CACHE_MAX_SIZE,
)

# =====================================================
# LOGGER
# =====================================================

logger = logging.getLogger("TechStore.Cache")

# =====================================================
# CACHE MANAGER
# =====================================================

class CacheManager:
    """
    Central cache manager.
    """

    def __init__(self):

        self.lock = threading.RLock()

        self.memory_cache = {}

        self.cache_hits = 0

        self.cache_misses = 0

        self.cache_directory = Path(CACHE_DIRECTORY)

        self.cache_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.initialize()

# =====================================================
# INITIALIZE
# =====================================================

    def initialize(self):
        """
        Initialize cache system.
        """

        logger.info("Initializing TechStore Cache...")

        if CACHE_ENABLED:

            logger.info("Cache enabled.")

        else:

            logger.warning("Cache disabled.")

# =====================================================
# CACHE STATUS
# =====================================================

    def is_enabled(self):
        """
        Return cache status.
        """

        return CACHE_ENABLED

# =====================================================
# CACHE DIRECTORY
# =====================================================

    def get_cache_directory(self):
        """
        Return cache directory.
        """

        return self.cache_directory

# =====================================================
# CACHE HEALTH
# =====================================================

    def health(self):
        """
        Return cache health.
        """

        return {

            "enabled": CACHE_ENABLED,

            "directory": str(self.cache_directory),

            "memory_entries": len(self.memory_cache),

            "hits": self.cache_hits,

            "misses": self.cache_misses,

        }

# =====================================================
# GLOBAL CACHE INSTANCE
# =====================================================

cache = CacheManager()

# ======================================================
# GENERATE CACHE KEY
# ======================================================

def generate_key(self, value):
    """
    Generate a unique cache key.
    """

    return hashlib.sha256(
        str(value).encode("utf-8")
    ).hexdigest()


# ======================================================
# STORE CACHE
# ======================================================

def set(self, key, value, ttl=CACHE_DEFAULT_TTL):
    """
    Store data in cache.
    """

    with self.lock:

        expires = time.time() + ttl

        self.memory_cache[key] = {

            "value": value,

            "expires": expires

        }

        return True


# ======================================================
# GET CACHE
# ======================================================

def get(self, key):
    """
    Retrieve cached data.
    """

    with self.lock:

        data = self.memory_cache.get(key)

        if data is None:

            self.cache_misses += 1

            return None

        if time.time() > data["expires"]:

            del self.memory_cache[key]

            self.cache_misses += 1

            return None

        self.cache_hits += 1

        return data["value"]


# ======================================================
# CACHE EXISTS
# ======================================================

def exists(self, key):
    """
    Check whether cache exists.
    """

    return self.get(key) is not None


# ======================================================
# UPDATE CACHE
# ======================================================

def update(self, key, value, ttl=CACHE_DEFAULT_TTL):
    """
    Update cached data.
    """

    return self.set(key, value, ttl)


# ======================================================
# DELETE CACHE
# ======================================================

def delete(self, key):
    """
    Delete cached item.
    """

    with self.lock:

        if key in self.memory_cache:

            del self.memory_cache[key]

            return True

        return False


# ======================================================
# CLEAR CACHE
# ======================================================

def clear(self):
    """
    Remove all cached items.
    """

    with self.lock:

        self.memory_cache.clear()

        return True


# ======================================================
# CLEAN EXPIRED CACHE
# ======================================================

def cleanup(self):
    """
    Remove expired cache.
    """

    now = time.time()

    expired = []

    with self.lock:

        for key, value in self.memory_cache.items():

            if value["expires"] <= now:

                expired.append(key)

        for key in expired:

            del self.memory_cache[key]

    return len(expired)


# ======================================================
# CACHE COUNT
# ======================================================

def cache_count(self):
    """
    Return total cached items.
    """

    return len(self.memory_cache)

# ======================================================
# AI CACHE KEY
# ======================================================

def generate_ai_key(self, prompt, context=""):
    """
    Generate a unique cache key for AI requests.
    """

    combined = f"{prompt}|{context}"

    return self.generate_key(combined)


# ======================================================
# CACHE AI RESPONSE
# ======================================================

def cache_ai_response(
    self,
    prompt,
    response,
    context="",
    ttl=CACHE_DEFAULT_TTL,
):
    """
    Store an AI response.
    """

    key = self.generate_ai_key(
        prompt,
        context,
    )

    return self.set(
        key,
        response,
        ttl,
    )


# ======================================================
# GET AI RESPONSE
# ======================================================

def get_cached_ai_response(
    self,
    prompt,
    context="",
):
    """
    Return cached AI response.
    """

    key = self.generate_ai_key(
        prompt,
        context,
    )

    return self.get(key)


# ======================================================
# AI CACHE EXISTS
# ======================================================

def ai_response_exists(
    self,
    prompt,
    context="",
):
    """
    Check whether an AI response exists.
    """

    return (
        self.get_cached_ai_response(
            prompt,
            context,
        )
        is not None
    )


# ======================================================
# DELETE AI RESPONSE
# ======================================================

def delete_ai_response(
    self,
    prompt,
    context="",
):
    """
    Delete cached AI response.
    """

    key = self.generate_ai_key(
        prompt,
        context,
    )

    return self.delete(key)


# ======================================================
# CLEAR AI CACHE
# ======================================================

def clear_ai_cache(self):
    """
    Clear all cached AI responses.
    """

    return self.clear()


# ======================================================
# AI CACHE STATISTICS
# ======================================================

def ai_cache_statistics(self):
    """
    Return AI cache statistics.
    """

    return {

        "cached_items": self.cache_count(),

        "cache_hits": self.cache_hits,

        "cache_misses": self.cache_misses,

        "hit_rate": (
            self.cache_hits /
            max(
                self.cache_hits +
                self.cache_misses,
                1,
            )
        ) * 100,

    }


    
