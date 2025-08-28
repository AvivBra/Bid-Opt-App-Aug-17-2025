"""Campaign builder module - ONLY THE UPDATED SECTIONS."""

# Add this import at the top of the file (after existing imports):
from .processors.keyword_processor import KeywordProcessor
from .validators.keyword_validator import KeywordValidator


# Replace or update the get_processor function:
def get_processor(campaign_type: str):
    """Get the appropriate processor for campaign type.

    Args:
        campaign_type: Type of campaign

    Returns:
        Processor instance
    """
    # Map of campaign types to processor classes
    processor_map = {
        "Halloween Testing": HalloweenTestingProcessor,
        "Testing": KeywordProcessor,
        "Phrase": KeywordProcessor,
        "Broad": KeywordProcessor,
        "Halloween Phrase": KeywordProcessor,
        "Halloween Broad": KeywordProcessor,
        # Add PT processors when implemented
        # "Testing PT": ProductTargetingProcessor,
        # "Expanded": ProductTargetingProcessor,
        # "Halloween Testing PT": ProductTargetingProcessor,
        # "Halloween Expanded": ProductTargetingProcessor,
    }

    processor_class = processor_map.get(campaign_type)

    if not processor_class:
        raise ValueError(f"No processor found for campaign type: {campaign_type}")

    # For KeywordProcessor, pass the campaign type
    if processor_class == KeywordProcessor:
        return processor_class(campaign_type)
    else:
        return processor_class()


# Replace or update the get_validator function:
def get_validator(campaign_type: str):
    """Get the appropriate validator for campaign type.

    Args:
        campaign_type: Type of campaign

    Returns:
        Validator instance
    """
    # Map of campaign types to validator classes
    validator_map = {
        "Halloween Testing": HalloweenTestingValidator,
        "Testing": KeywordValidator,
        "Phrase": KeywordValidator,
        "Broad": KeywordValidator,
        "Halloween Phrase": KeywordValidator,
        "Halloween Broad": KeywordValidator,
        # Add PT validators when implemented
        # "Testing PT": ProductTargetingValidator,
        # "Expanded": ProductTargetingValidator,
        # "Halloween Testing PT": ProductTargetingValidator,
        # "Halloween Expanded": ProductTargetingValidator,
    }

    validator_class = validator_map.get(campaign_type)

    if not validator_class:
        raise ValueError(f"No validator found for campaign type: {campaign_type}")

    # For KeywordValidator, pass the campaign type
    if validator_class == KeywordValidator:
        return validator_class(campaign_type)
    else:
        return validator_class()
