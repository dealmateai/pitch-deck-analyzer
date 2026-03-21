"""
LLM extractor for higher-accuracy structured information extraction.
Supports OpenAI-compatible chat completion providers.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional

import requests

from config import LLM_CONFIG
from utils.logger import log


class LLMExtractor:
    """LLM-based extraction with schema-guided JSON output."""

    def __init__(self):
        self.provider = LLM_CONFIG.get("provider", "groq")
        self.api_key = LLM_CONFIG.get("api_key", "")
        self.model = LLM_CONFIG.get("model", "llama-3.1-8b-instant")
        self.timeout = LLM_CONFIG.get("timeout_seconds", 40)
        self.max_input_chars = LLM_CONFIG.get("max_input_chars", 18000)
        self.enabled = LLM_CONFIG.get("enabled", True) and bool(self.api_key)

        if self.enabled:
            log.info(f"LLM extractor enabled: provider={self.provider}, model={self.model}")
        else:
            log.info("LLM extractor disabled (set LLM_API_KEY and USE_LLM_EXTRACTION=true)")

    def is_available(self) -> bool:
        return self.enabled

    def extract(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract company/founder info as structured JSON."""
        if not self.enabled:
            return None

        if not text or not text.strip():
            return None

        prompt_text = self._clean_and_clip(text)

        system_prompt = (
            "You are an expert startup pitch deck analyst."
            " Return ONLY valid JSON (no markdown, no commentary)."
            " Do not fabricate values; set null when unsure."
            " Extract concise official company name (no taglines)."
            " Extract precise founder names, education, and numeric market/traction metrics from the text only."
        )

        user_prompt = (
            "Extract startup company and founder details from the pitch deck text."
            " Focus on factual data stated in the deck (no guesses)."
            " Prefer numeric values with units for market and traction if present."
            " Keep company name concise (strip slogans/taglines)."
            " If a value is absent, return null.\n\n"
            "Return JSON with this exact shape:\n"
            "{\n"
            "  \"company\": {\n"
            "    \"name\": string|null,\n"
            "    \"industry\": string|null,\n"
            "    \"problem\": string|null,\n"
            "    \"solution\": string|null,\n"
            "    \"market_size\": {\"tam\": string|null, \"sam\": string|null, \"som\": string|null, \"growth_rate\": string|null},\n"
            "    \"traction\": {\"users\": string|null, \"revenue\": string|null, \"monthly_growth\": string|null, \"customers\": string|null},\n"
            "    \"business_model\": string|null\n"
            "  },\n"
            "  \"founder\": {\n"
            "    \"names\": [string],\n"
            "    \"count\": number|null,\n"
            "    \"experience_level\": string|null,\n"
            "    \"education\": {\"top_school\": string|null, \"degree\": string|null, \"field\": string|null},\n"
            "    \"technical_background\": boolean|null,\n"
            "    \"previous_companies\": [{\"name\": string, \"position\": string}],\n"
            "    \"startup_experience\": boolean|null,\n"
            "    \"domain_expertise\": string|null\n"
            "  }\n"
            "}\n\n"
            "Pitch deck text (cleaned):\n"
            f"{prompt_text}"
        )

        payload = {
            "model": self.model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
        }

        try:
            url, headers = self._provider_endpoint()
            response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            raw_content = data["choices"][0]["message"]["content"]
            parsed = self._parse_json(raw_content)
            if not parsed:
                return None

            return {
                "company": parsed.get("company", {}),
                "founder": parsed.get("founder", {}),
            }

        except Exception as exc:
            log.warning(f"LLM extraction failed, using rule-based fallback: {exc}")
            return None

    def _parse_json(self, raw: str) -> Optional[Dict[str, Any]]:
        """Parse JSON safely, including markdown fenced output fallback."""
        if not raw:
            return None

        text = raw.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
        if fence_match:
            try:
                return json.loads(fence_match.group(1))
            except json.JSONDecodeError:
                return None

        first = text.find("{")
        last = text.rfind("}")
        if first != -1 and last != -1 and last > first:
            try:
                return json.loads(text[first : last + 1])
            except json.JSONDecodeError:
                return None

        return None

    def _provider_endpoint(self) -> tuple[str, Dict[str, str]]:
        """Return endpoint URL and headers for configured provider."""
        if self.provider == "together":
            url = "https://api.together.xyz/v1/chat/completions"
        elif self.provider == "openai":
            url = "https://api.openai.com/v1/chat/completions"
        else:
            url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        return url, headers

    def _clean_and_clip(self, text: str) -> str:
        """Lightly clean whitespace and clip to max length."""
        cleaned = re.sub(r"\s+", " ", text or "").strip()
        return cleaned[: self.max_input_chars]
