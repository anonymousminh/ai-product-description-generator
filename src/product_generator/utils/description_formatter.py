import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DescriptionFormatter:
    def __init__(self, full_description: str):
        self.full_description = full_description

    def get_short_description(self) -> str:
        # Simple approach: take the first sentence or a fixed number of words
        sentences = self.full_description.split(". ")
        if sentences:
            short_desc = sentences[0]
            if len(short_desc.split()) > 30: # If first sentence is too long, truncate
                short_desc = " ".join(short_desc.split()[:30]) + "..."
            return short_desc.strip() + "."
        return ""

    def get_detailed_description(self) -> str:
        # For detailed, you might just return the full description
        # or apply minor formatting like ensuring paragraphs.
        return self.full_description.strip()

    # Placeholder for future formats (social, SEO)
    def get_social_caption(self) -> str:
        return ""

    def get_seo_rich_description(self) -> str:
        return ""

