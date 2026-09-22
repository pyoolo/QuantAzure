# Contributing Guidelines

Thank you for considering contributing to the Study Material Repository! This document provides guidelines for submitting quality research materials and maintaining consistency across the archive.

## Before You Contribute

1. **Read the Main README**: Familiarize yourself with the repository structure and naming conventions in [README.md](README.md)
2. **Review Section-Specific Guides**: Each section has its own README with detailed guidelines
3. **Check for Duplicates**: Ensure your material doesn't duplicate existing content

## How to Contribute

### Option 1: Direct Upload via GitHub
1. Navigate to the appropriate section folder
2. Select the correct subdirectory for your material type
3. Use the "Add file" button to upload or create new files
4. Follow the naming conventions outlined in the relevant section README

### Option 2: Create a Pull Request
1. Fork the repository
2. Create a new branch: `git checkout -b add/your-material-name`
3. Add your files following the naming conventions
4. Create a descriptive commit message
5. Push to your fork and submit a pull request
6. Include a description of the materials and their relevance

## Naming Conventions

### File Names
- **Research Documents**: `YYYYMMDD_Topic_Description.pdf`
  - Example: `20240915_Tesla_CreditAnalysis.pdf`

- **Code Files**: `descriptive_name_lowercase.py`
  - Example: `risk_parity_strategy.py`

- **Data Files**: `DataType_Description_YYYYMM.csv`
  - Example: `EquityPrices_SP500_202409.csv`

- **Notebooks**: `YYYYMMDD_AnalysisType_Description.ipynb`
  - Example: `20240915_MachineLearning_StockPrediction.ipynb`

### Folder Names
- Use lowercase with hyphens: `folder-name`
- Avoid spaces and special characters
- Be descriptive: `credit-spread-analysis` (good) vs `data` (bad)

## Quality Standards

### For Research Documents
- [ ] Document includes a clear title and date
- [ ] Analysis includes proper citations and sources
- [ ] Key assumptions are documented
- [ ] Conclusion or recommendation is clearly stated
- [ ] Spell-checked and professionally formatted
- [ ] File size is reasonable (< 20MB)

### For Code/Notebooks
- [ ] Includes clear comments and docstrings
- [ ] Required libraries are documented
- [ ] Includes example usage or test case
- [ ] Code is reproducible with documented dependencies
- [ ] Follows PEP 8 style guide (for Python)
- [ ] Include a brief README in the folder if complex

### For Data Files
- [ ] Includes a data dictionary or schema
- [ ] Source is documented
- [ ] Date range is clearly specified
- [ ] Missing values are documented
- [ ] File is in a standard format (.csv, .xlsx, .parquet)
- [ ] File size is optimized (use .parquet for large files)

## Submission Checklist

Before submitting your contribution, ensure:

- [ ] Material is placed in the correct section and subdirectory
- [ ] Filename follows the established naming convention
- [ ] File includes a publication/analysis date
- [ ] If applicable, a brief summary is included (metadata file or in document)
- [ ] All sources are properly cited
- [ ] Material is original or properly attributed
- [ ] No proprietary or confidential information is included
- [ ] No personal identifying information is included (unless necessary)
- [ ] File is free of malware or suspicious content
- [ ] File is properly formatted and readable

## Section-Specific Guidelines

### 📊 Equities Section
- Valuation analysis should include DCF, comps, and precedent transactions
- Company analyses should follow the template in `equities/templates/`
- Include historical financial data and key metrics
- Document investment thesis with bull and bear cases

### 🏦 Fixed Income, Credit & Commodities Section
- Credit analyses should include leverage ratios and covenant analysis
- Bond analysis should document yield curves and spread relationships
- Include recovery and default probability analysis
- Document geopolitical and macro factors for commodities

### 🔬 Quantitative Research Section
- Code should be reproducible and well-documented
- Include performance metrics and backtesting results
- Document all assumptions and model parameters
- Provide comparison to benchmark strategies
- Include risk analysis and sensitivity testing

## Code Standards

### Python
```python
# File header
"""
Module description.

Author: Your Name
Date: YYYY-MM-DD
"""

# Docstrings for functions
def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
    """
    Calculate the Sharpe ratio of a return series.
    
    Parameters
    ----------
    returns : array-like
        Daily returns
    risk_free_rate : float
        Annual risk-free rate (default: 0.0)
    
    Returns
    -------
    sharpe_ratio : float
        Annualized Sharpe ratio
    """
    pass
```

### Jupyter Notebooks
- Add markdown cells explaining the analysis flow
- Include section headers with `#` markdown
- Document data sources and assumptions
- Clear output before committing (except final results)
- Save visualizations as separate PNG files if very large

## Prohibited Content

Do NOT submit:
- Proprietary trading strategies or models
- Confidential company information
- Personal financial data or credentials
- Copyrighted material without attribution
- Malware or malicious code
- Adult or inappropriate content

## Review Process

1. **Initial Check**: We verify the submission meets formatting and content standards
2. **Quality Review**: Materials are reviewed for accuracy and relevance
3. **Feedback**: We may request clarifications or improvements
4. **Acceptance**: Approved materials are merged into the repository

Review time is typically 2-5 business days.

## Questions?

If you have questions about contributing:
1. Check the section-specific README files
2. Review existing similar materials for examples
3. Open an issue with your question

## License & Attribution

By contributing to this repository, you agree that:
- Your contribution can be used for educational and professional purposes
- Materials are shared under the repository's license
- You have the right to contribute this material
- Proper attribution will be maintained

---

**Thank you for contributing to the Study Material Archive!**

We appreciate your effort in building this knowledge base for the financial research community.
