# Bid Optimizer for Amazon Ads

## Overview
An automated bid optimization system for Amazon Ads campaigns. The application processes bulk campaign data and automatically adjusts bids based on performance metrics.

## Installation

### Requirements
- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum
- Windows/Mac/Linux

### Setup
1. Clone the repository:
```bash
git clone [repository-url]
cd bid-optimizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app/main.py
```

The application will open in your default browser at http://localhost:8501

## Usage

### Step 1: Upload Files
1. Download the Template file using the "Download Template" button
2. Fill in the Template with your portfolio data:
   - Portfolio Name
   - Base Bid (0.02 - 4.00 or "Ignore")
   - Target CPA (optional)
3. Upload the completed Template
4. Upload your Bulk 60 file from Amazon Ads

### Step 2: Select Optimization
- Currently, only "Zero Sales" optimization is available
- Check the Zero Sales checkbox to enable it

### Step 3: Process Files
- Click "Process Files" to start the optimization
- Wait for processing to complete (10-30 seconds for typical files)

### Step 4: Download Results
- Click "Download Working File" to get the optimized Excel file
- The file contains two sheets:
  - Targeting: Optimized keywords and product targeting
  - Bidding Adjustment: Bidding adjustments (unchanged)

## File Structure

```
bid-optimizer/
├── app/                    # UI and navigation
│   ├── main.py            # Entry point
│   ├── navigation.py      # Sidebar navigation
│   ├── pages/             # Application pages
│   ├── ui/                # UI components
│   └── state/             # Session state management
├── business/              # Business logic
│   ├── bid_optimizations/ # Optimization algorithms
│   └── common/            # Shared business logic
├── data/                  # Data handling
│   ├── readers/           # File readers
│   ├── validators/        # Data validators
│   └── writers/           # File writers
├── config/                # Configuration
├── utils/                 # Utility functions
└── tests/                 # Test files
```

## Features

### Phase 1 (Current)
- ✅ Zero Sales Optimization
- ✅ Template file generation and validation
- ✅ Bulk 60 file processing
- ✅ Working file generation with bid adjustments
- ✅ Dark mode UI
- ✅ Session state management

### Phase 2 (Planned)
- ⏳ 13 additional optimization algorithms
- ⏳ Campaigns Optimizer
- ⏳ Clean file generation
- ⏳ Bulk 7/30 support
- ⏳ Data Rova integration

## Known Limitations
- Maximum file size: 40MB
- Maximum rows: 500,000
- Only Excel (.xlsx) and CSV formats supported
- Bulk file must have exactly 48 columns
- Processing time increases linearly with file size

## Troubleshooting

### Common Issues

**Issue**: Application won't start
- **Solution**: Ensure Python 3.8+ is installed and all dependencies are installed

**Issue**: File upload fails
- **Solution**: Check file size (<40MB) and format (.xlsx or .csv)

**Issue**: Template validation fails
- **Solution**: Ensure Portfolio Names are unique and Base Bids are within range (0.02-4.00)

**Issue**: Processing takes too long
- **Solution**: Files over 100,000 rows may take 30+ seconds. Be patient.

**Issue**: Pink highlighted rows in output
- **Solution**: These rows have bid calculation issues. Review the Bid values manually.

## Contributing

### Development Setup
1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest tests/
```

3. Check code style:
```bash
pylint business/ data/
```

### Code Style
- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to all functions
- Keep functions under 50 lines

### Testing
- Write unit tests for new functions
- Ensure 80%+ code coverage
- Test with various file sizes

## License
Proprietary - All rights reserved

## Support
For issues or questions, contact the development team.

---
**Version**: 1.0.0  
**Last Updated**: December 2024