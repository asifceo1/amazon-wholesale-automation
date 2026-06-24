# Quick Start Guide - Amazon Wholesale Automation

## 🚀 Get Started in 5 Minutes

### Step 1: Clone & Setup

```bash
git clone https://github.com/asifceo1/amazon-wholesale-automation.git
cd amazon-wholesale-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure

```bash
# Copy example config
cp config/config.example.yaml config/config.yaml

# Edit with your API keys
nano config/config.yaml
```

### Step 3: Run Full Research Pipeline

```bash
# Run complete automation
python src/main.py --mode full --category "Health & Beauty" --num-products 20

# Check results
ls data/products/
ls data/distributors/
ls data/opportunities/
```

### Step 4: View Results

Open the generated CSV files in Excel or your spreadsheet app:
- `data/products/research_*.csv` - Product research results
- `data/distributors/distributors_*.csv` - Discovered distributors
- `data/opportunities/opportunities_*.csv` - Scored opportunities

---

## 📊 Common Commands

### Research Products Only
```bash
python src/main.py --mode research --keywords "supplement,protein,vitamin" --num-products 30
```

### Find Distributors for Specific Brands
```bash
python src/main.py --mode distributor --brands "Nature's Way,GNC"
```

### Full Pipeline with Custom Config
```bash
python src/main.py --mode full --config config/custom.yaml --num-products 50
```

### Verbose Logging
```bash
python src/main.py --mode full --verbose
```

---

## 🔑 Required Configuration

At minimum, you need to configure:

```yaml
apis:
  keepa_key: "YOUR_KEY"
  helium10_key: "YOUR_KEY"

research:
  min_profit_margin: 15
  min_monthly_revenue: 2000
  categories:
    - "Health & Beauty"
    - "Pet Supplies"

output:
  format: "csv"
```

---

## 📁 Output Files

### research_*.csv
Columns: ASIN, Product Name, Brand, Category, Price, Monthly Sales, Margin %, Sellers, Rating

### distributors_*.csv
Columns: Distributor Name, Brand, Authorization Status, Contact Email, Phone, Website

### opportunities_*.csv
Columns: Product, Score, ROI %, Recommendation, Best Distributors

---

## 🆘 Troubleshooting

**Module not found errors?**
```bash
pip install -r requirements.txt
```

**Config file not found?**
```bash
cp config/config.example.yaml config/config.yaml
```

**API key errors?**
```bash
# Verify your keys in config/config.yaml
# Get keys from:
# - Keepa: https://keepa.com/#!api
# - Helium 10: https://www.helium10.com/tools/apis
```

---

## 🐳 Docker Usage (Optional)

```bash
# Build image
docker-compose build

# Run automation
docker-compose up

# Check results
docker exec wholesale-automation ls -la data/
```

---

## 📈 Next Steps

1. **Review Results** - Open CSV files and analyze top opportunities
2. **Contact Distributors** - Use email/phone from distributor findings
3. **Apply for Accounts** - Submit wholesale applications
4. **Schedule Regular Runs** - Set up automated weekly research
5. **Expand Categories** - Run research on multiple niches

---

## 💡 Pro Tips

- Start with 1-2 product categories to test
- Use `--num-products 10` initially to verify setup
- Check logs in `logs/automation.log` for debugging
- Export results to Excel for team review
- Create separate configs for different strategies

---

## 📚 Full Documentation

See [README.md](README.md) for detailed documentation.

Questions? Open an issue on GitHub!
