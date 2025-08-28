"""Campaign processors module."""

from .base_processor import BaseCampaignProcessor
from .halloween_testing import HalloweenTestingProcessor
from .keyword_processor import KeywordProcessor
from .product_targeting_processor import ProductTargetingProcessor


def get_processor(campaign_type: str):
    """Get processor for campaign type.

    Args:
        campaign_type: Type of campaign

    Returns:
        Processor instance or None
    """
    # For keyword campaigns, use KeywordProcessor
    keyword_campaigns = {
        "testing": KeywordProcessor,
        "phrase": KeywordProcessor,
        "broad": KeywordProcessor,
        "halloween_phrase": KeywordProcessor,
        "halloween_broad": KeywordProcessor,
    }

    # For other specific processors
    specific_processors = {
        "halloween_testing": HalloweenTestingProcessor,
    }

    # Check keyword campaigns first
    if campaign_type in keyword_campaigns:
        processor_class = keyword_campaigns[campaign_type]
        # Convert processor name back to UI name for KeywordProcessor
        ui_name_map = {
            "testing": "Testing",
            "phrase": "Phrase",
            "broad": "Broad",
            "halloween_phrase": "Halloween Phrase",
            "halloween_broad": "Halloween Broad",
        }
        return processor_class(ui_name_map.get(campaign_type, campaign_type))

    # Check specific processors
    processor_class = specific_processors.get(campaign_type)
    if processor_class:
        return processor_class()

    return None


__all__ = [
    "BaseCampaignProcessor",
    "HalloweenTestingProcessor",
    "KeywordProcessor",
    "ProductTargetingProcessor",
    "get_processor",
]
