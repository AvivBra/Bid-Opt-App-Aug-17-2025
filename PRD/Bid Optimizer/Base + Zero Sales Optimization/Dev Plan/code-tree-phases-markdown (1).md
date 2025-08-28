# עץ קבצי קוד מתוקן - Bid Optimizer
## תאריך: דצמבר 2024, 12:10

```
bid-optimizer/
├── app/
│   ├── main.py [1]
│   ├── navigation.py [2]
│   ├── pages/
│   │   └── bid_optimizer.py [3]
│   ├── ui/
│   │   ├── layout.py [2]
│   │   ├── sidebar.py [2]
│   │   ├── shared/
│   │   │   ├── upload_section.py [3]
│   │   │   ├── validation_section.py [5]
│   │   │   ├── output_section.py [6]
│   │   │   └── page_header.py
│   │   └── components/
│   │       ├── file_cards.py
│   │       ├── checklist.py [5]
│   │       ├── buttons.py [3]
│   │       ├── alerts.py [5]
│   │       ├── progress_bar.py [6]
│   │       └── download_buttons.py [6]
│   └── state/
│       ├── session_manager.py [1]
│       ├── bid_state.py [4]
│       └── mock_data.py [10]
│
├── business/
│   ├── common/
│   │   ├── portfolio_filter.py [7]
│   │   └── excluded_portfolios.py [5]
│   ├── bid_optimizations/
│   │   ├── base_optimization.py [7]
│   │   └── zero_sales/
│   │       ├── validator.py [7]
│   │       ├── cleaner.py [7]
│   │       ├── processor.py [7]
│   │       └── orchestrator.py [8]
│   └── processors/
│       └── output_formatter.py [8]
│
├── data/
│   ├── readers/
│   │   ├── excel_reader.py [3]
│   │   └── csv_reader.py [4]
│   ├── writers/
│   │   └── excel_writer.py [8]
│   ├── validators/
│   │   ├── template_validator.py [3]
│   │   ├── bulk_validator.py [4]
│   │   └── portfolio_validator.py [5]
│   └── template_generator.py [3]
│
├── config/
│   ├── constants.py [1]
│   ├── settings.py [1]
│   ├── ui_text.py [3]
│   └── optimization_config.py [8]
│
├── utils/
│   ├── file_utils.py [1]
│   ├── filename_generator.py [1]
│   └── page_utils.py [6]
│
├── tests/
│   ├── unit/
│   │   └── test_zero_sales.py [9]
│   ├── integration/
│   │   └── test_bid_flow.py [9]
│   └── fixtures/
│       ├── valid_template.xlsx [9]
│       └── valid_bulk_60.xlsx [9]
│
├── requirements.txt [1]
├── README.md [10]
└── .streamlit/
    └── config.toml [1]
```