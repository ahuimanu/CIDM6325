#!/bin/bash
# Backup TravelMathLite database and airport data
# Usage: ./backup_airports.sh

set -e

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Ensure backup directory exists
mkdir -p $BACKUP_DIR

echo "🔄 Starting backup: $DATE"

# Backup SQLite database (development)
if [ -f "travelmathlite/db.sqlite3" ]; then
    echo "📦 Backing up SQLite database..."
    cp travelmathlite/db.sqlite3 $BACKUP_DIR/db.sqlite3.$DATE
    echo "   ✅ Saved: $BACKUP_DIR/db.sqlite3.$DATE"
else
    echo "   ⚠️  No SQLite database found (production setup?)"
fi

# Backup airports as JSON fixture
echo "✈️  Backing up airports..."
uv run python travelmathlite/manage.py dumpdata airports.Airport --indent 2 > $BACKUP_DIR/airports_$DATE.json
AIRPORT_COUNT=$(grep -c '"model": "airports.airport"' $BACKUP_DIR/airports_$DATE.json || echo "0")
echo "   ✅ Saved: $BACKUP_DIR/airports_$DATE.json ($AIRPORT_COUNT records)"

# Backup countries and cities
echo "🌍 Backing up countries and cities..."
uv run python travelmathlite/manage.py dumpdata base.Country base.City --indent 2 > $BACKUP_DIR/base_$DATE.json
COUNTRY_COUNT=$(grep -c '"model": "base.country"' $BACKUP_DIR/base_$DATE.json || echo "0")
CITY_COUNT=$(grep -c '"model": "base.city"' $BACKUP_DIR/base_$DATE.json || echo "0")
echo "   ✅ Saved: $BACKUP_DIR/base_$DATE.json ($COUNTRY_COUNT countries, $CITY_COUNT cities)"

# Show backup sizes
echo ""
echo "📊 Backup summary:"
ls -lh $BACKUP_DIR/*$DATE* | awk '{print "   " $9, "-", $5}'

# Cleanup old backups (keep last 7 days)
echo ""
echo "🗑️  Cleaning up old backups (>7 days)..."
DELETED_JSON=$(find $BACKUP_DIR -name "*.json" -mtime +7 -delete -print | wc -l)
DELETED_DB=$(find $BACKUP_DIR -name "db.sqlite3.*" -mtime +7 -delete -print | wc -l)
echo "   Deleted: $DELETED_JSON JSON files, $DELETED_DB databases"

echo ""
echo "✅ Backup complete!"
echo "   Location: $BACKUP_DIR/*$DATE*"
echo "   Restore with: ./backups/restore_airports.sh $DATE"
