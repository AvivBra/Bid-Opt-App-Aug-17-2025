"""Campaign processors module."""

from .base_processor import BaseCampaignProcessor
from .halloween_testing import HalloweenTestingProcessor


def get_processor(campaign_type: str):
    """Get processor for campaign type.
    
    Args:
        campaign_type: Type of campaign
        
    Returns:
        Processor instance or None
    """
    processors = {
        "halloween_testing": HalloweenTestingProcessor,
    }
    
    processor_class = processors.get(campaign_type)
    if processor_class:
        return processor_class()
    return None


__all__ = ["BaseCampaignProcessor", "HalloweenTestingProcessor", "get_processor"]