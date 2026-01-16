# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Docker Pulls Statistics Dashboard that tracks download metrics for Docker images and GitHub releases. The project automatically collects data daily via GitHub Actions, visualizes it with Chart.js, and deploys to GitHub Pages.

**Live Demo:** https://sunny0826.github.io/docker-pulls-statistics/

## Development Commands

```bash
# Install dependencies
pip install requests pandas
npm install

# Fetch latest stats from Docker Hub and GitHub APIs
npm run fetch

# Convert CSV data to JSON for the web dashboard
npm run convert

# Preview the dashboard locally (serves on port 8000)
npm run preview

# Generate screenshot of the chart
npm run capture
```

## Data Pipeline Architecture

The project follows a linear data flow:

```
APIs (Docker Hub, GitHub) → fetch_stats.py → stats.csv → convert_to_json.py → stats.json → index.html → capture-chart.js → chart-preview.png
```

### Pipeline Stages

1. **Data Collection** (`scripts/fetch_stats.py`)
   - Fetches pull counts for `kwdb/kwdb` and `kwdb/kwdb_comp_env` Docker images
   - Fetches GitHub release download counts from `kwdb/kwdb`
   - Implements exponential backoff retry (max 3 attempts)
   - Appends timestamped entries to `data/stats.csv`

2. **Data Transformation** (`scripts/convert_to_json.py`)
   - Converts CSV to JSON structure using Pandas
   - Outputs to `docs/data/stats.json`

3. **Visualization** (`docs/index.html`)
   - Single-page Chart.js dashboard
   - Displays 3 datasets: kwdb, kwdb_comp_env, github_release_downloads

4. **Screenshot Generation** (`scripts/capture-chart.js`)
   - Uses Puppeteer to capture chart as PNG
   - Outputs to `docs/chart-preview.png`

### Automation

GitHub Actions (`.github/workflows/stats.yml`) runs the full pipeline daily at midnight UTC and commits results back to the repository.

## Directory Structure

```
data/           # Source data: stats.csv
docs/           # Web dashboard and generated assets
scripts/        # Python fetch/convert scripts, Node screenshot script
.github/        # GitHub Actions workflow
```

## Data Schema

**CSV (`data/stats.csv`)**: Columns are `date`, `kwdb/kwdb`, `kwdb/kwdb_comp_env`, `kwdb/release`

**JSON (`docs/data/stats.json`)**: Structure with arrays for `dates`, `kwdb`, `kwdb_comp_env`, `github_release_downloads`

## API Endpoints

- Docker Hub: `https://hub.docker.com/v2/repositories/{image}/`
- GitHub Releases: `https://api.github.com/repos/{repo}/releases`

## Error Handling Pattern

Python scripts use exponential backoff retry with max 3 attempts. Failed API calls return 0 and are logged to stderr.

## Deployment

The `docs/` folder is deployed to GitHub Pages. All automated commits use the message: "Update docker stats data"
