# Escape Game Data Processing

## Introduction
This project provides tools for scraping, processing, integrating, and recommending escape room games. The primary components include:
- `EscapeGameScraper`: A scraper for gathering game URLs and detailed game information from workshop websites.
- `CommentKeywordProcessor`: A processor for extracting keywords from game reviews.
- `GameDataIntegrator`: An integrator that combines game data with extracted keywords.
- `EscapeGameRecommender`: A Gradio-based interface for recommending games based on user input keywords.

## System Architecture
1. **Build an escape games database.**
    - **Build basic information from escape games.**
        - Use web crawler technology to save basic information from escape games.
    - **Comment keyword integration from escape games.**
        - Use web crawler technology to crawl comments from escape games.
        - Organize comments into keywords and save.
    - **Database integration from all escape games' information.**
2. **Design interface.**
    - Connect escape games database to an interactive recommendation system using Gradio.

## File Descriptions

### `basic_information.py`
Contains the `EscapeGameScraper` class which is responsible for:
- Generating workshop URLs from a list of workshop IDs.
- Scraping game URLs from these workshop pages.
- Fetching detailed game information from the scraped URLs.

### `comment_keyword.py`
Contains the `CommentKeywordProcessor` class and `KeywordExtractor` class:
- `KeywordExtractor` is used to extract keywords from a list of game reviews.
- `CommentKeywordProcessor` processes and saves the extracted keywords for each game.

### `database_integration.py`
Contains the `GameDataIntegrator` class which:
- Integrates game review keywords into the main game data.
- Extracts additional keywords from the game content description.
- Saves the combined data for further analysis.

### `design_interface.py`
Contains the `EscapeGameRecommender` class which:
- Loads the integrated game data.
- Extracts keywords from user input using jieba.
- Matches the input keywords with games in the database.
- Provides formatted game information as a recommendation based on the input keywords.
- Launches a Gradio web interface for interactive recommendations.

## Usage
1. Start by using the `basic_information.py` script to scrape game data.
2. Run `comment_keyword.py` to extract and process review keywords.
3. Use `database_integration.py` to integrate the review keywords with the game data.
4. Finally, run `design_interface.py` to launch an interactive Gradio interface for recommending escape games based on user input.

## Requirements
- Python 3.x
- `requests`, `beautifulsoup4`, `numpy`, `jieba`, `gradio`

## Installation
Install the necessary packages using pip:
```bash
pip install requests beautifulsoup4 numpy jieba gradio
