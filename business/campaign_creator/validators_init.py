"""Campaign validators module."""

from .base_validator import BaseCampaignValidator
from .halloween_testing import HalloweenTestingValidator


def get_validator(campaign_type: str) -> BaseCampaignValidator:
    """Get validator for campaign type.
    
    Args:
        campaign_type: Type of campaign
        
    Returns:
        Validator instance or None
    """
    validators = {
        "halloween_testing": HalloweenTestingValidator,
    }
    
    validator_class = validators.get(campaign_type)
    if validator_class:
        return validator_class()
    return None


__all__ = ["BaseCampaignValidator", "HalloweenTestingValidator", "get_validator"]
