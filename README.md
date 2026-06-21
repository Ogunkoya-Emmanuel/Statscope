# Statscope

Understand any dataset in plain language.

Statscope analyzes your CSV and Excel files, explaining what the data means without requiring statistics knowledge.

## Features

- **Human-Friendly Explanations** - Insights explained in plain language
- **Smart Data Cleaning** - Handles currency (₦, $, €, £), percentages, commas
- **Automatic ID Detection** - Skips meaningless ID columns
- **Outlier Detection** - Identifies unusual values
- **Correlation Analysis** - Shows which columns relate to each other
- **Category Analysis** - Visualizes most common values
- **PDF Reports** - Download formatted analysis reports
- **Beginner Mode** - Toggle for simplified or detailed explanations

## Quick Start

### Prerequisites

- Python 3.11 or higher (3.14+ has limited package support)
- pip (Python package manager)

### Installation

1. Clone or download this repository

2. Navigate to project folder:
```bash
   cd statscope
```

3. Create virtual environment:
```bash
   python -m venv venv
```

4. Activate virtual environment:
```bash
   # Windows PowerShell
   venv\Scripts\Activate.ps1
   
   # Windows Command Prompt
   venv\Scripts\activate.bat
   
   # Mac/Linux
   source venv/bin/activate
```

5. Install dependencies:
```bash
   pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python -m streamlit run app.py
```

Opens at `http://localhost:8501`

### How to Use

1. **Upload a file**
   - CSV or Excel (.xlsx, .xls)
   - Or check "Use sample dataset" to test with built-in data

2. **Toggle explanation mode**
   - "Explain like I'm new" for simplified language
   - Uncheck for technical details

3. **Review insights**
   - Dataset overview
   - Data quality report
   - Numeric analysis with distributions
   - Correlation heatmap
   - Category breakdowns

4. **Download PDF report** - Save your analysis

## File Structure
statscope/

├── venv/                  (virtual environment - ignore)

├── data/

│   └── sample_dataset.csv (built-in test data)

├── app.py                 (main UI)

├── analyzer.py            (analysis logic)

├── visualizer.py          (chart creation)

├── requirements.txt       (dependencies)

├── .gitignore            (git ignore rules)

└── README.md             (this file)

## Supported Formats

- CSV (.csv)
- Excel (.xlsx, .xls)

## Data Cleaning

Automatically handles:
- Currency: ₦5,000 → 5000
- Percentages: 45% → 45
- Thousands: 1,200 → 1200
- Mixed formats in same column

## Deactivate Virtual Environment

When finished:
```bash
deactivate
```

## Troubleshooting

### Port 8501 already in use
```bash
python -m streamlit run app.py --server.port 8502
```

### Module not found
```bash
pip install -r requirements.txt --upgrade
```

### Virtual environment won't activate (Windows PowerShell)
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### Installation fails with Python 3.14
Python 3.14 is very new and some packages lack pre-built wheels.

**Solution:** Use Python 3.11 or 3.12 instead:
1. Download from [python.org](https://www.python.org/downloads/)
2. Create new virtual environment with Python 3.11/3.12
3. Install dependencies again

### Requirements.txt without versions
If you see errors during installation, edit `requirements.txt` to remove version numbers:
```txt
streamlit
pandas
matplotlib
seaborn
openpyxl
reportlab
numpy
```

This lets pip find compatible pre-built wheels automatically.

## Testing

Try with these datasets:
- Sales data (detect trends, correlations)
- Survey responses (analyze categories)
- Weather data (see distributions)
- Student grades (find patterns)
- Any CSV with mixed data types

## Dependencies

- **streamlit** - Web UI framework
- **pandas** - Data manipulation
- **matplotlib** - Chart creation
- **seaborn** - Statistical visualizations
- **numpy** - Numerical computing
- **openpyxl** - Excel support
- **reportlab** - PDF generation

See `requirements.txt` for versions.

## How It Works

1. **Upload** - Select CSV or Excel file
2. **Analyze** - Detect columns, clean data, calculate statistics
3. **Explain** - Generate human-friendly insights
4. **Visualize** - Create charts for each insight
5. **Export** - Download report as PDF

## Architecture

- **app.py** - Streamlit UI and user interaction
- **analyzer.py** - Data processing and insight generation
- **visualizer.py** - Chart creation and formatting

Clean separation allows easy testing and feature additions.

## Future Features

- Multi-file comparison
- Time series forecasting
- Advanced statistical tests
- Data transformation tools
- Real-time data connections
- Export to different formats

## Common Issues

**Question:** Can I use this offline?
**Answer:** Yes. After installation, everything runs locally. No internet required.

**Question:** What file sizes can it handle?
**Answer:** Tested up to 100MB. Larger files may be slow.

**Question:** Does it store my data?
**Answer:** No. All data stays on your computer. Nothing is uploaded anywhere.

## Project Structure Notes

- `venv/` - Virtual environment (do not commit)
- `data/` - Sample datasets
- `.gitignore` - Git ignore rules (respects venv/)
- `requirements.txt` - Python dependencies

## Contributing

Found a bug? Have a suggestion?
- Test with different datasets
- Document what works/doesn't work
- Share feedback

## License

MIT License - Use and modify freely

## Built With

- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- ReportLab

## Author

Data analysis tool built from scratch. Learning project with real-world impact potential.

## Support

Stuck? Try:
1. Check troubleshooting section
2. Verify virtual environment is activated `(venv)` prefix visible
3. Ensure all dependencies installed `pip list`
4. Try different dataset
5. Check Python version `python --version`