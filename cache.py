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


# ======================================================
# FILE CACHE KEY
# ======================================================

def generate_file_key(self, file_path):
    """
    Generate cache key for a file.
    """

    return self.generate_key(str(file_path))


# ======================================================
# CACHE FILE
# ======================================================

def cache_file(
    self,
    file_path,
    file_data,
    ttl=CACHE_DEFAULT_TTL,
):
    """
    Cache a file.
    """

    key = self.generate_file_key(file_path)

    return self.set(
        key,
        file_data,
        ttl,
    )


# ======================================================
# GET CACHED FILE
# ======================================================

def get_cached_file(self, file_path):
    """
    Retrieve cached file.
    """

    key = self.generate_file_key(file_path)

    return self.get(key)


# ======================================================
# FILE EXISTS
# ======================================================

def file_cache_exists(self, file_path):
    """
    Check if cached file exists.
    """

    return (
        self.get_cached_file(file_path)
        is not None
    )


# ======================================================
# DELETE FILE CACHE
# ======================================================

def delete_cached_file(self, file_path):
    """
    Delete cached file.
    """

    key = self.generate_file_key(file_path)

    return self.delete(key)


# ======================================================
# IMAGE CACHE
# ======================================================

def cache_image(
    self,
    image_path,
    image_data,
    ttl=CACHE_DEFAULT_TTL,
):

    return self.cache_file(
        image_path,
        image_data,
        ttl,
    )


# ======================================================
# VIDEO CACHE
# ======================================================

def cache_video(
    self,
    video_path,
    video_data,
    ttl=CACHE_DEFAULT_TTL,
):

    return self.cache_file(
        video_path,
        video_data,
        ttl,
    )


# ======================================================
# VOICE CACHE
# ======================================================

def cache_voice(
    self,
    voice_path,
    voice_data,
    ttl=CACHE_DEFAULT_TTL,
):

    return self.cache_file(
        voice_path,
        voice_data,
        ttl,
    )


# ======================================================
# DOCUMENT CACHE
# ======================================================

def cache_document(
    self,
    document_path,
    document_data,
    ttl=CACHE_DEFAULT_TTL,
):

    return self.cache_file(
        document_path,
        document_data,
        ttl,
    )


# ======================================================
# CACHE FILE STATISTICS
# ======================================================

def file_cache_statistics(self):
    """
    Return file cache statistics.
    """

    return {

        "cached_items": self.cache_count(),

        "hits": self.cache_hits,

        "misses": self.cache_misses,

    }

# ======================================================
# REMOVE OLDEST CACHE ENTRY
# ======================================================

def evict_oldest(self):
    """
    Remove the oldest cached item.
    """

    with self.lock:

        if not self.memory_cache:
            return False

        oldest_key = min(
            self.memory_cache,
            key=lambda key: self.memory_cache[key]["expires"]
        )

        del self.memory_cache[oldest_key]

        return True


# ======================================================
# ENFORCE CACHE SIZE
# ======================================================

def enforce_cache_limit(self):
    """
    Keep cache within maximum size.
    """

    while len(self.memory_cache) > CACHE_MAX_SIZE:

        self.evict_oldest()


# ======================================================
# STORE WITH LIMIT
# ======================================================

def smart_set(
    self,
    key,
    value,
    ttl=CACHE_DEFAULT_TTL,
):
    """
    Store cache while respecting limits.
    """

    result = self.set(
        key,
        value,
        ttl,
    )

    self.enforce_cache_limit()

    return result


# ======================================================
# CACHE MEMORY USAGE
# ======================================================

def memory_usage(self):
    """
    Estimate cache memory usage.
    """

    total = 0

    for item in self.memory_cache.values():

        total += len(str(item))

    return total


# ======================================================
# CACHE HIT RATE
# ======================================================

def hit_rate(self):
    """
    Return cache hit percentage.
    """

    total = self.cache_hits + self.cache_misses

    if total == 0:

        return 0.0

    return (self.cache_hits / total) * 100


# ======================================================
# CACHE MISS RATE
# ======================================================

def miss_rate(self):
    """
    Return cache miss percentage.
    """

    total = self.cache_hits + self.cache_misses

    if total == 0:

        return 0.0

    return (self.cache_misses / total) * 100


# ======================================================
# SMART CACHE REPORT
# ======================================================

def smart_cache_report(self):
    """
    Return smart cache statistics.
    """

    return {

        "entries": self.cache_count(),

        "memory_usage": self.memory_usage(),

        "hit_rate": self.hit_rate(),

        "miss_rate": self.miss_rate(),

        "hits": self.cache_hits,

        "misses": self.cache_misses,

    }

# ======================================================
# CACHE HEALTH CHECK
# ======================================================

def cache_health(self):
    """
    Return cache health information.
    """

    return {

        "status": "healthy" if CACHE_ENABLED else "disabled",

        "enabled": CACHE_ENABLED,

        "entries": self.cache_count(),

        "hits": self.cache_hits,

        "misses": self.cache_misses,

        "hit_rate": self.hit_rate(),

        "memory_usage": self.memory_usage(),

        "cache_directory": str(self.cache_directory),

    }


# ======================================================
# VALIDATE CACHE
# ======================================================

def validate_cache(self):
    """
    Validate cache contents.
    """

    invalid = []

    now = time.time()

    for key, value in self.memory_cache.items():

        if "value" not in value:

            invalid.append(key)

            continue

        if "expires" not in value:

            invalid.append(key)

            continue

        if value["expires"] < now:

            invalid.append(key)

    return invalid


# ======================================================
# REPAIR CACHE
# ======================================================

def repair_cache(self):
    """
    Remove invalid cache entries.
    """

    invalid = self.validate_cache()

    for key in invalid:

        self.delete(key)

    return len(invalid)


# ======================================================
# CACHE DIAGNOSTICS
# ======================================================

def diagnostics(self):
    """
    Return cache diagnostics.
    """

    return {

        "health": self.cache_health(),

        "invalid_entries": len(self.validate_cache()),

        "cached_items": self.cache_count(),

        "hits": self.cache_hits,

        "misses": self.cache_misses,

    }


# ======================================================
# RESET CACHE STATISTICS
# ======================================================

def reset_statistics(self):
    """
    Reset cache statistics.
    """

    self.cache_hits = 0

    self.cache_misses = 0

    return True


# ======================================================
# EXPORT CACHE REPORT
# ======================================================

def cache_report(self):
    """
    Return complete cache report.
    """

    return {

        "health": self.cache_health(),

        "diagnostics": self.diagnostics(),

        "statistics": self.smart_cache_report(),

    }


# ======================================================
# SAVE CACHE
# ======================================================

def save_cache(self):
    """
    Save memory cache to disk.
    """

    cache_file = self.cache_directory / "cache.json"

    with open(cache_file, "w", encoding="utf-8") as file:

        json.dump(self.memory_cache, file, indent=4)

    return cache_file


# ======================================================
# LOAD CACHE
# ======================================================

def load_cache(self):
    """
    Load cache from disk.
    """

    cache_file = self.cache_directory / "cache.json"

    if not cache_file.exists():

        return False

    with open(cache_file, "r", encoding="utf-8") as file:

        self.memory_cache = json.load(file)

    return True


# ======================================================
# BACKUP CACHE
# ======================================================

def backup_cache(self):
    """
    Create a cache backup.
    """

    return self.save_cache()


# ======================================================
# RESTORE CACHE
# ======================================================

def restore_cache(self):
    """
    Restore cache from backup.
    """

    return self.load_cache()


# ======================================================
# CACHE VERSION
# ======================================================

def cache_version(self):
    """
    Return cache version.
    """

    return "1.0.0"


# ======================================================
# CACHE INFORMATION
# ======================================================

def cache_information(self):
    """
    Return production cache information.
    """

    return {

        "version": self.cache_version(),

        "enabled": CACHE_ENABLED,

        "directory": str(self.cache_directory),

        "entries": self.cache_count(),

        "hits": self.cache_hits,

        "misses": self.cache_misses,

    }


# ======================================================
# PRODUCTION CACHE CHECK
# ======================================================

def production_ready(self):
    """
    Verify cache is ready for production.
    """

    return {

        "ready": CACHE_ENABLED,

        "directory_exists": self.cache_directory.exists(),

        "cache_entries": self.cache_count(),

        "health": self.cache_health(),

}


