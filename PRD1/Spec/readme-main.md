# Bid Optimizer - Product Requirements & Development Documentation

## 📋 Overview

Comprehensive documentation for the Bid Optimizer application - an automated bid management system for Amazon Ads campaigns.

### Key Changes in This Version
- **5 separate upload buttons** instead of single Bulk file
- **Modular validation** - each optimization validates independently  
- **No global cleaning** - each optimization handles its own data
- **Template with 2 sheets**: Port Values + Top ASINs

## 📁 Documentation Structure

```
New PRD/
├── Spec/           # Product specifications
├── Dev Plan/       # Development guidelines
├── Testing/        # Test plans and scenarios
└── README.md       # This file
```

## 🚀 Quick Start for Developers

### 1. Start Here
- Read `Spec/Core/app-principles.md` - Core concepts
- Review `Spec/Core/architecture-spec.md` - System architecture
- Check `Dev Plan/development-phases.md` - Implementation plan

### 2. Key Specifications
- `Spec/IO/io-spec.md` - File formats and structure
- `Spec/UI/ui-spec.md` - User interface requirements
- `Spec/Optimizations/optimization-framework.md` - How optimizations work

### 3. Zero Sales Implementation
- `Spec/Optimizations/zero-sales/zero-sales-spec.md` - Complete specification
- **Important**: Keep calculation logic EXACTLY as existing code

## 🏗️ Architecture Highlights

### 4-Layer Architecture
1. **UI Layer** - Streamlit interface
2. **Business Layer** - Orchestration
3. **Optimizations Layer** - Modular optimizations
4. **Data Layer** - File I/O

### Key Principle: Modular Optimizations
Each optimization:
- Declares required files
- Validates independently
- Cleans its own data
- Processes independently

## 💻 Development Approach

### Build New Application
- **DO NOT modify existing app**
- Build fresh with correct architecture
- Reference `Dev Plan/development-phases.md` for what to reuse

### Reuse from Existing Code
| Component | Reuse | Build New |
|-----------|-------|-----------|
| UI Style & Colors | ✅ | |
| Zero Sales Formulas | ✅ | |
| File Readers | ✅ | |
| File Writers | ✅ | |
| Validation Logic | | ✅ |
| Orchestrator | | ✅ |
| Folder Structure | | ✅ |

## 📝 File Specifications

### Input Files
1. **Template** - Portfolio settings (2 sheets)
2. **Bulk 30** - 30 days data
3. **Bulk 60** - 60 days data  
4. **Bulk 7** - 7 days data
5. **Data Rova** - Profitability data

### Output Files
- **Working File** - With helper columns
- **Clean File** - For Amazon upload

## 🧪 Testing

### Test Scenarios
See `Testing/test-scenarios.md` for:
- Happy path
- Missing portfolios
- File size limits
- Multiple optimizations

### Mock Data
Use `Testing/mock-data-spec.md` for UI development without backend

## 📊 Zero Sales Optimization

### Required Files
- Template
- Bulk 60

### Validation
- All portfolios in Bulk must exist in Template
- Required columns: Units, Clicks, Portfolio Name

### Processing
Keeps existing calculation logic:
- 4 calculation cases based on Target CPA and "up and" in name
- Minimum bid: $0.02
- Maximum bid: $1.25

## ⏱️ Timeline

### Phase A: UI (2 days)
- Complete UI with mock data
- All 5 upload buttons
- Validation display
- Download section

### Phase B: Logic (3 days)  
- File readers
- Optimization framework
- Zero Sales implementation
- File generation

**Total: 5 working days**

## ✅ Success Criteria

### UI
- [ ] 5 separate upload buttons work
- [ ] Validation messages clear
- [ ] Progress tracking smooth
- [ ] Downloads functional

### Logic
- [ ] Zero Sales calculations identical to existing
- [ ] Files readable by Amazon
- [ ] Performance < 10 seconds for 100K rows
- [ ] Clean architecture

## 📞 Key Contacts

For questions about specifications:
- Review relevant document in `Spec/` folder
- Check `Testing/test-scenarios.md` for expected behavior

## 🔄 Version Control

This documentation represents the complete rewrite of the Bid Optimizer application with modular architecture.

**Version:** 2.0
**Date:** January 2024
**Status:** Ready for Development