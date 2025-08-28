"""Campaign builder module - ONLY THE UPDATED SECTIONS."""

# Add this import at the top of the file (after existing imports):
from .processors.keyword_processor import KeywordProcessor
from .processors.product_targeting_processor import ProductTargetingProcessor
from .processors.halloween_testing import HalloweenTestingProcessor
from .validators.keyword_validator import KeywordValidator
from .validators.product_targeting_validator import ProductTargetingValidator
from .validators.halloween_testing import HalloweenTestingValidator


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
        # Product Targeting processors
        "Testing PT": ProductTargetingProcessor,
        "Expanded": ProductTargetingProcessor,
        "Halloween Testing PT": ProductTargetingProcessor,
        "Halloween Expanded": ProductTargetingProcessor,
        # Handle orchestrator name conversions
        "halloween_testing": HalloweenTestingProcessor,
        "testing": KeywordProcessor,
        "phrase": KeywordProcessor,
        "broad": KeywordProcessor,
        "halloween_phrase": KeywordProcessor,
        "halloween_broad": KeywordProcessor,
        "testing_pt": ProductTargetingProcessor,
        "expanded": ProductTargetingProcessor,
        "halloween_testing_pt": ProductTargetingProcessor,
        "halloween_expanded": ProductTargetingProcessor,
    }

    processor_class = processor_map.get(campaign_type)

    if not processor_class:
        raise ValueError(f"No processor found for campaign type: {campaign_type}")

    # For KeywordProcessor and ProductTargetingProcessor, pass the campaign type
    # Convert lowercase back to UI format for processors
    ui_name_map = {
        "halloween_testing": "Halloween Testing",
        "testing": "Testing",
        "phrase": "Phrase", 
        "broad": "Broad",
        "halloween_phrase": "Halloween Phrase",
        "halloween_broad": "Halloween Broad",
        "testing_pt": "Testing PT",
        "expanded": "Expanded",
        "halloween_testing_pt": "Halloween Testing PT",
        "halloween_expanded": "Halloween Expanded",
    }
    
    ui_name = ui_name_map.get(campaign_type, campaign_type)
    
    if processor_class == KeywordProcessor:
        return processor_class(ui_name)
    elif processor_class == ProductTargetingProcessor:
        return processor_class(ui_name)
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
        # Product Targeting validators
        "Testing PT": ProductTargetingValidator,
        "Expanded": ProductTargetingValidator,
        "Halloween Testing PT": ProductTargetingValidator,
        "Halloween Expanded": ProductTargetingValidator,
        # Handle orchestrator name conversions
        "halloween_testing": HalloweenTestingValidator,
        "testing": KeywordValidator,
        "phrase": KeywordValidator,
        "broad": KeywordValidator,
        "halloween_phrase": KeywordValidator,
        "halloween_broad": KeywordValidator,
        "testing_pt": ProductTargetingValidator,
        "expanded": ProductTargetingValidator,
        "halloween_testing_pt": ProductTargetingValidator,
        "halloween_expanded": ProductTargetingValidator,
    }

    validator_class = validator_map.get(campaign_type)

    if not validator_class:
        raise ValueError(f"No validator found for campaign type: {campaign_type}")

    # For KeywordValidator and ProductTargetingValidator, pass the campaign type
    # Convert lowercase back to UI format for validators
    ui_name_map = {
        "halloween_testing": "Halloween Testing",
        "testing": "Testing",
        "phrase": "Phrase",
        "broad": "Broad", 
        "halloween_phrase": "Halloween Phrase",
        "halloween_broad": "Halloween Broad",
        "testing_pt": "Testing PT",
        "expanded": "Expanded",
        "halloween_testing_pt": "Halloween Testing PT",
        "halloween_expanded": "Halloween Expanded",
    }
    
    ui_name = ui_name_map.get(campaign_type, campaign_type)
    
    if validator_class == KeywordValidator:
        return validator_class(ui_name)
    elif validator_class == ProductTargetingValidator:
        return validator_class(ui_name)
    else:
        return validator_class()
