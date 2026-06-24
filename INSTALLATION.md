# Installation & Setup Guide

## System Requirements

- Python 3.8+
- Git
- 2GB RAM minimum
- Internet connection

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/asifceo1/amazon-wholesale-automation.git
cd amazon-wholesale-automation
```

### 2. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Get API Keys

#### Keepa API Key
1. Visit https://keepa.com/#!api
2. Sign up for free account
3. Generate API key from dashboard
4. Free tier: Limited calls per month

#### Helium 10 API Key
1. Visit https://www.helium10.com/tools/apis
2. Subscribe to a plan (free trial available)
3. Generate API key

#### Amazon SP-API (Optional)
1. Register as Amazon Seller
2. Go to Seller Central > Settings > User Permissions
3. Request API access
4. Follow authorization flow

### 5. Configure Application

```bash
# Create config directory
mkdir -p config data/products data/distributors data/opportunities logs

# Copy example config
cp config/config.example.yaml config/config.yaml

# Edit with your settings
nano config/config.yaml  # or use your editor
```

### 6. Test Installation

```bash
# Run help
python src/main.py --help

# Run with mock data (no API calls)
python src/main.py --mode full --num-products 5
```

## Docker Installation (Alternative)

### Prerequisites
- Docker 20.10+
- Docker Compose 1.29+

### Steps

```bash
# Clone repository
git clone https://github.com/asifceo1/amazon-wholesale-automation.git
cd amazon-wholesale-automation

# Create .env file
echo "KEEPA_API_KEY=your_key_here" > .env
echo "HELIUM10_API_KEY=your_key_here" >> .env

# Build and run
docker-compose build
docker-compose up

# View logs
docker-compose logs -f app

# Access results
docker exec wholesale-automation ls -la data/
```

## Verification

### Check Installation

```bash
# Should return version
python src/main.py --help

# Should complete without errors
python src/main.py --mode research --num-products 3 --verbose
```

### Verify Configuration

```bash
# Check if config loads correctly
python -c "from src.utils.config_loader import load_config; print(load_config())"
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'src'"

```bash
# Make sure you're in the project root directory
cd amazon-wholesale-automation
pwd  # Should show .../amazon-wholesale-automation
```

### "No module named 'yaml'"

```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

### "API key invalid"

```bash
# Verify key in config/config.yaml
# Get correct key from:
# - Keepa: https://keepa.com/#!api
# - Helium 10: https://www.helium10.com/tools/apis
```

### "Permission denied" (macOS/Linux)

```bash
# Make scripts executable
chmod +x src/main.py
```

## Next Steps

1. Read [QUICKSTART.md](QUICKSTART.md) for usage examples
2. Check [config/config.example.yaml](config/config.example.yaml) for all options
3. See [README.md](README.md) for complete documentation

## Getting Help

- Check logs: `cat logs/automation.log`
- Review test cases: `pytest tests/`
- Open GitHub issue with error details

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove project directory
cd ..
rm -rf amazon-wholesale-automation
```
