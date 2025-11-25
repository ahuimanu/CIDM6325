#!/bin/bash
# Restore TravelMathLite database from backup
# Usage: ./restore_airports.sh [backup_date]
#
# Examples:
#   ./restore_airports.sh                  # List available backups
#   ./restore_airports.sh 20251114_120000  # Restore specific backup

set -e

BACKUP_DIR="backups"

# Show usage if no argument
if [ -z "$1" ]; then
    echo "Usage: $0 <backup_date>"
    echo ""
    echo "Example: $0 20251114_120000"
    echo ""
    echo "Available backups:"
    echo "=================="
    
    if ls $BACKUP_DIR/db.sqlite3.* 1> /dev/null 2>&1; then
        for backup in $BACKUP_DIR/db.sqlite3.*; do
            DATE=$(basename $backup | sed 's/db.sqlite3.//')
            SIZE=$(ls -lh $backup | awk '{print $5}')
            MODIFIED=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" $backup 2>/dev/null || stat -c "%y" $backup 2>/dev/null | cut -d. -f1)
            echo "  📅 $DATE - $SIZE - $MODIFIED"
        done
    else
        echo "  No backups found in $BACKUP_DIR/"
    fi
    
    exit 1
fi

DATE=$1

# Validate backup exists
if [ ! -f "$BACKUP_DIR/db.sqlite3.$DATE" ]; then
    echo "❌ Error: Backup $BACKUP_DIR/db.sqlite3.$DATE not found"
    echo ""
    echo "Available backups:"
    ls -1 $BACKUP_DIR/db.sqlite3.* 2>/dev/null | sed 's/.*db.sqlite3./  /' || echo "  None"
    exit 1
fi

# Safety confirmation
echo "⚠️  WARNING: Database Restore Operation"
echo "======================================"
echo ""
echo "This will REPLACE your current database with:"
echo "  📦 Backup: $BACKUP_DIR/db.sqlite3.$DATE"
echo "  📊 Size: $(ls -lh $BACKUP_DIR/db.sqlite3.$DATE | awk '{print $5}')"
echo "  📅 Date: $(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" $BACKUP_DIR/db.sqlite3.$DATE 2>/dev/null || stat -c "%y" $BACKUP_DIR/db.sqlite3.$DATE 2>/dev/null | cut -d. -f1)"
echo ""
echo "Current database will be backed up to:"
echo "  💾 travelmathlite/db.sqlite3.pre_restore.$(date +%Y%m%d_%H%M%S)"
echo ""
read -p "Are you absolutely sure? Type 'yes' to continue: " -r
echo ""

if [[ ! $REPLY =~ ^yes$ ]]; then
    echo "❌ Cancelled. No changes made."
    exit 0
fi

# Backup current database before restore
if [ -f "travelmathlite/db.sqlite3" ]; then
    SAFETY_BACKUP="travelmathlite/db.sqlite3.pre_restore.$(date +%Y%m%d_%H%M%S)"
    echo "💾 Creating safety backup of current database..."
    cp travelmathlite/db.sqlite3 $SAFETY_BACKUP
    echo "   ✅ Saved: $SAFETY_BACKUP"
    echo ""
fi

# Perform restore
echo "🔄 Restoring database from $DATE..."
cp $BACKUP_DIR/db.sqlite3.$DATE travelmathlite/db.sqlite3
echo "   ✅ Database file restored"
echo ""

# Run migrations to ensure schema is current
echo "🔧 Running migrations..."
uv run python travelmathlite/manage.py migrate --no-input
echo "   ✅ Migrations applied"
echo ""

# Verify restore
echo "✅ Verifying restore..."
uv run python travelmathlite/manage.py shell -c "
from apps.airports.models import Airport
from apps.base.models import Country, City

airport_count = Airport.objects.count()
country_count = Country.objects.count()
city_count = City.objects.count()

print(f'   ✈️  Airports: {airport_count:,}')
print(f'   🌍 Countries: {country_count:,}')
print(f'   🏙️  Cities: {city_count:,}')
"
echo ""

echo "🎉 Restore complete!"
echo ""
echo "Next steps:"
echo "  1. Test your application thoroughly"
echo "  2. Run: uv run python travelmathlite/manage.py validate_airports"
echo "  3. Run: uv run python travelmathlite/manage.py test apps.airports apps.base"
echo ""
echo "If you need to undo this restore:"
echo "  ./restore_airports.sh <different_date>"
echo "  OR manually restore from: $SAFETY_BACKUP"
