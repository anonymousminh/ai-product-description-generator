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


    def get_social_caption(self) -> str:
        title = self.product_metadata.get("title", "product")
        features = self.product_metadata.get("features", [])

        caption = f"Discover the amazing {title}! "
        if features:
            caption += f"Featuring {features[0].lower()} and more. "
        caption += "Get yours today! #" + title.replace(" ", "") + " #Innovation"

        return caption[:280]

    def get_seo_rich_description(self) -> str:
        title = self.product_metadata.get("title", "product") 
        category = self.product_metadata.get("category", "category")
        features = self.product_metadata.get("features", [])

        keywords = [title.lower(), category.lower()] + [f.lower() for f in features]
        keywords_str = ", ".join(sorted(list(set(keywords))))

        seo_description = (
            f"Buy the best {title} in the {category}. Key features include: {', '.join(features)}. "\
            f"Experience quality and innovation with our {title}. "\
            f"Keywords: {keywords_str}."
        )

        return seo_description[:160]
