"""Campaign validators module."""

from .base_validator import BaseCampaignValidator
from .halloween_testing import HalloweenTestingValidator
from .keyword_validator import KeywordValidator
from .product_targeting_validator import ProductTargetingValidator


def get_validator(campaign_type: str):
    """Get validator for campaign type.

    Args:
        campaign_type: Type of campaign

    Returns:
        Validator instance or None
    """
    # For keyword campaigns, use KeywordValidator
    keyword_campaigns = {
        "testing": KeywordValidator,
        "phrase": KeywordValidator,
        "broad": KeywordValidator,
        "halloween_phrase": KeywordValidator,
        "halloween_broad": KeywordValidator,
    }

    # For other specific validators
    specific_validators = {
        "halloween_testing": HalloweenTestingValidator,
    }

    # Check keyword campaigns first
    if campaign_type in keyword_campaigns:
        validator_class = keyword_campaigns[campaign_type]
        # Convert processor name back to UI name for KeywordValidator
        ui_name_map = {
            "testing": "Testing",
            "phrase": "Phrase",
            "broad": "Broad",
            "halloween_phrase": "Halloween Phrase",
            "halloween_broad": "Halloween Broad",
        }
        return validator_class(ui_name_map.get(campaign_type, campaign_type))

    # Check specific validators
    validator_class = specific_validators.get(campaign_type)
    if validator_class:
        return validator_class()

    return None


__all__ = [
    "BaseCampaignValidator",
    "HalloweenTestingValidator",
    "KeywordValidator",
    "ProductTargetingValidator",
    "get_validator",
]
