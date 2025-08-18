```
bid-optimizer/
├── app/
│   ├── main.py                     # Entry point with page router
│   ├── navigation.py               # Sidebar navigation
│   │
│   ├── pages/                      # Pages directory
│   │   ├── __init__.py
│   │   ├── bid_optimizer.py        # Bid Optimizer page
│   │   └── campaigns_optimizer.py  # Campaigns Optimizer page
│   │
│   ├── ui/
│   │   ├── layout.py               # Shared dark mode CSS
│   │   ├── theme.py                # Violet theme + Inter font
│   │   ├── sidebar.py              # Sidebar component
│   │   │
│   │   ├── shared/                 # Shared components
│   │   │   ├── __init__.py
│   │   │   ├── upload_section.py   # Shared upload UI
│   │   │   ├── validation_section.py
│   │   │   ├── output_section.py
│   │   │   └── page_header.py     # Dynamic page header
│   │   │
│   │   ├── components/             # Reusable components
│   │   │   ├── __init__.py
│   │   │   ├── file_cards.py      # Bulk 7/30/60 + Data Rova buttons
│   │   │   ├── template_uploader.py # Template with tabs
│   │   │   ├── checklist.py
│   │   │   ├── buttons.py
│   │   │   ├── alerts.py
│   │   │   ├── progress_bar.py
│   │   │   └── download_buttons.py
│   │   │
│   │   └── panels/                 # Legacy (for compatibility)
│   │       ├── upload_panel.py
│   │       ├── validate_panel.py
│   │       └── output_panel.py
│   │
│   └── state/
│       ├── __init__.py
│       ├── session_manager.py      # Updated for multi-page
│       ├── bid_state.py           # Bid Optimizer state
│       ├── campaigns_state.py     # Campaigns Optimizer state
│       └── mock_data.py
│
├── business/
│   ├── __init__.py
│   │
│   ├── bid_optimizations/         # Bid Optimizer logic
│   │   ├── __init__.py
│   │   ├── base_optimization.py
│   │   ├── zero_sales/
│   │   │   ├── __init__.py
│   │   │   ├── validator.py      # Validation inside optimization
│   │   │   ├── cleaner.py        # Cleaning inside optimization
│   │   │   └── processor.py      # Main processing logic
│   │   └── [13 other optimizations]/
│   │
│   ├── campaign_optimizations/    # Campaigns Optimizer logic
│   │   ├── __init__.py
│   │   ├── base_campaign_opt.py
│   │   ├── negation/
│   │   │   ├── __init__.py
│   │   │   ├── validator.py
│   │   │   ├── cleaner.py
│   │   │   └── processor.py
│   │   └── harvesting/
│   │       ├── __init__.py
│   │       ├── validator.py
│   │       ├── cleaner.py
│   │       └── processor.py
│   │
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── file_generator.py
│   │   └── output_formatter.py    # Shared output formatting
│   │
│   └── services/
│       ├── __init__.py
│       ├── bid_orchestrator.py    # Bid Optimizer orchestrator
│       └── campaign_orchestrator.py # Campaigns orchestrator
│
├── data/
│   ├── __init__.py
│   ├── readers/
│   │   ├── __init__.py
│   │   ├── excel_reader.py
│   │   └── csv_reader.py
│   ├── writers/
│   │   ├── __init__.py
│   │   └── output_writer.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── portfolio.py
│   │   ├── asin.py                # For Top ASINs tab
│   │   └── validation_result.py
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── bid_template.py        # Port Values tab
│   │   └── asin_template.py       # Top ASINs tab
│   └── template_generator.py
│
├── integrations/
│   ├── __init__.py
│   └── data_rova/
│       ├── __init__.py
│       ├── client.py
│       └── auth.py
│
├── config/
│   ├── __init__.py
│   ├── constants.py               # Updated with both pages
│   ├── navigation.py              # Navigation config
│   ├── settings.py
│   └── ui_text.py                # Text for both pages
│
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   ├── filename_generator.py
│   └── page_utils.py            # Page-specific utilities
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── bid_optimizer/       # Bid Optimizer tests
│   │   │   ├── test_zero_sales.py
│   │   │   └── test_bid_validations.py
│   │   ├── campaigns_optimizer/ # Campaigns tests
│   │   │   ├── test_negation.py
│   │   │   └── test_harvesting.py
│   │   └── shared/              # Shared tests
│   │       ├── test_readers.py
│   │       └── test_file_generator.py
│   │
│   ├── integration/
│   │   ├── test_bid_flow.py
│   │   ├── test_campaigns_flow.py
│   │   └── test_navigation.py
│   │
│   └── fixtures/
│       ├── bid_optimizer/
│       │   ├── template_port_values.xlsx
│       │   ├── template_top_asins.xlsx
│       │   ├── bulk_7.xlsx
│       │   ├── bulk_30.xlsx
│       │   └── bulk_60.xlsx
│       └── campaigns_optimizer/
│           └── campaign_data.xlsx
│
├── .streamlit/
│   └── config.toml               # Dark mode, violet, Inter font
│
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .gitignore
└── README.md
```