"""Instagram Graph API poster for medicohelp.ai."""

from __future__ import annotations

import asyncio
import base64
import logging
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"


class InstagramPoster:
    """Posts images and carousels to Instagram via the Graph API."""

    def __init__(self, settings) -> None:
        self.settings = settings

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    @property
    def is_configured(self) -> bool:
        """Return True when all required Instagram credentials are present."""
        return bool(
            self.settings.instagram_user_id
            and self.settings.instagram_access_token
            and self.settings.imgbb_api_key
        )

    async def upload_to_imgbb(self, image_path: Path) -> str:
        """Upload a local image to imgbb.com and return its public URL."""
        if not self.settings.imgbb_api_key:
            raise RuntimeError("imgbb_api_key is not configured")

        logger.debug("Uploading %s to imgbb", image_path.name)

        with image_path.open("rb") as fh:
            encoded = base64.b64encode(fh.read()).decode("utf-8")

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://api.imgbb.com/1/upload",
                data={
                    "key": self.settings.imgbb_api_key,
                    "image": encoded,
                    "name": image_path.stem,
                },
            )
            response.raise_for_status()
            result = response.json()

        url: str = result["data"]["url"]
        logger.info("Uploaded %s → %s", image_path.name, url)
        return url

    async def post_carousel(self, image_paths: list[Path], caption: str) -> str:
        """
        Upload images, create individual containers, create a carousel
        container, then publish it.  Returns the published post ID.
        """
        self._require_configured()

        if len(image_paths) < 2:
            raise ValueError("A carousel requires at least 2 images")
        if len(image_paths) > 10:
            image_paths = image_paths[:10]

        logger.info("Starting Instagram carousel post (%d slides)", len(image_paths))

        # 1. Upload every image to imgbb to obtain a public URL.
        public_urls: list[str] = []
        for path in image_paths:
            url = await self.upload_to_imgbb(path)
            public_urls.append(url)

        # 2. Create one media container per image (child containers).
        container_ids: list[str] = []
        for url in public_urls:
            cid = await self._create_image_container(url, is_carousel_item=True)
            container_ids.append(cid)
            await asyncio.sleep(1)  # respect rate limits

        # 3. Create the carousel container (parent).
        carousel_id = await self._create_carousel_container(container_ids, caption)

        # 4. Give the API a moment to process.
        await asyncio.sleep(3)

        # 5. Publish.
        post_id = await self._publish_media(carousel_id)
        logger.info("Instagram carousel published: post_id=%s", post_id)
        return post_id

    async def post_single_image(self, image_path: Path, caption: str) -> str:
        """Upload one image and publish it. Returns the published post ID."""
        self._require_configured()

        logger.info("Starting Instagram single-image post: %s", image_path.name)
        url = await self.upload_to_imgbb(image_path)
        container_id = await self._create_image_container(url, caption=caption)
        await asyncio.sleep(2)
        post_id = await self._publish_media(container_id)
        logger.info("Instagram single image published: post_id=%s", post_id)
        return post_id

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _create_image_container(
        self,
        image_url: str,
        caption: str = "",
        *,
        is_carousel_item: bool = False,
    ) -> str:
        """
        Create a single media container.

        When ``is_carousel_item=True`` the container is marked as a child
        of a future carousel; the ``caption`` is therefore ignored (it is
        set on the parent carousel container instead).
        """
        params: dict = {
            "image_url": image_url,
            "access_token": self.settings.instagram_access_token,
        }
        if is_carousel_item:
            params["is_carousel_item"] = "true"
        elif caption:
            params["caption"] = caption

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{GRAPH_API_BASE}/{self.settings.instagram_user_id}/media",
                params=params,
            )
            self._raise_for_api_error(response, "create image container")

        container_id: str = response.json()["id"]
        logger.debug("Created image container: %s", container_id)
        return container_id

    async def _create_carousel_container(
        self, child_container_ids: list[str], caption: str
    ) -> str:
        """Create the parent carousel container that references child containers."""
        children_csv = ",".join(child_container_ids)

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{GRAPH_API_BASE}/{self.settings.instagram_user_id}/media",
                params={
                    "media_type": "CAROUSEL",
                    "children": children_csv,
                    "caption": caption,
                    "access_token": self.settings.instagram_access_token,
                },
            )
            self._raise_for_api_error(response, "create carousel container")

        carousel_id: str = response.json()["id"]
        logger.debug("Created carousel container: %s", carousel_id)
        return carousel_id

    async def _publish_media(self, container_id: str) -> str:
        """Publish a media container (single or carousel). Returns the post ID."""
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{GRAPH_API_BASE}/{self.settings.instagram_user_id}/media_publish",
                params={
                    "creation_id": container_id,
                    "access_token": self.settings.instagram_access_token,
                },
            )
            self._raise_for_api_error(response, "publish media")

        post_id: str = response.json()["id"]
        return post_id

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _require_configured(self) -> None:
        if not self.is_configured:
            raise RuntimeError(
                "Instagram is not fully configured. "
                "Set INSTAGRAM_USER_ID, INSTAGRAM_ACCESS_TOKEN, and IMGBB_API_KEY."
            )

    @staticmethod
    def _raise_for_api_error(response: httpx.Response, context: str) -> None:
        """Raise a descriptive RuntimeError when the Graph API returns an error."""
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            try:
                error_detail = response.json().get("error", {})
            except Exception:
                error_detail = response.text
            raise RuntimeError(
                f"Instagram Graph API error during '{context}': {error_detail}"
            ) from None
