# TravelMathLite Visual Check Scripts

## Search Visual Check

### Setup

Install Playwright browsers:

```bash
uv run playwright install chromium
```

### Run

From repository root:

```bash
uv run python travelmathlite/scripts/visual_check_search.py
```

Or from `travelmathlite/` directory:

```bash
uv run python scripts/visual_check_search.py
```

### Output

Screenshots saved to `travelmathlite/screenshots/search/`:

- `01-empty-search.png` - Empty search results page
- `02-navbar-search-filled.png` - Navbar search form with query entered
- `03-search-results-dallas.png` - Search results for "Dallas"
- `04-search-results-airport.png` - Search results for "Airport"
- `05-search-results-page2.png` - Second page of paginated results (if applicable)

### Environment Variables

- `VISUAL_CHECK_HOST` - Server host (default: `127.0.0.1`)
- `VISUAL_CHECK_PORT` - Server port (default: `8010`)

### Notes

The script:

1. Starts a temporary Django dev server on port 8010
2. Launches headless Chromium browser
3. Captures screenshots at key interaction points
4. Terminates server and exits

Playwright dependency is ephemeral (installed via `uvx --with`).
