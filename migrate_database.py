#!/usr/bin/env python3
"""
Database migration script to add PokeAPI columns to existing Pokemon table
"""

import os
import sys
import sqlite3
from pathlib import Path

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def migrate_database():
    """Add new PokeAPI columns to the Pokemon table"""
    
    # Find the database file
    db_path = None
    possible_paths = [
        'app/pokemon.db',
        'pokemon.db',
        'instance/pokemon.db'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ Database file not found. Creating new database structure...")
        # If no database exists, we'll create it with the app
        return create_new_database()
    
    print(f"📁 Found database at: {db_path}")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if new columns already exist
        cursor.execute("PRAGMA table_info(pokemon)")
        columns = [row[1] for row in cursor.fetchall()]
        
        new_columns = [
            ('sprite_url', 'VARCHAR(255)'),
            ('sprite_shiny_url', 'VARCHAR(255)'),
            ('official_artwork_url', 'VARCHAR(255)'),
            ('description', 'TEXT'),
            ('genus', 'VARCHAR(50)'),
            ('height', 'INTEGER'),
            ('weight', 'INTEGER'),
            ('base_happiness', 'INTEGER'),
            ('capture_rate', 'INTEGER'),
            ('is_legendary', 'BOOLEAN DEFAULT 0'),
            ('is_mythical', 'BOOLEAN DEFAULT 0'),
            ('habitat', 'VARCHAR(50)'),
            ('pokemon_color', 'VARCHAR(20)'),
            ('abilities', 'TEXT'),
            ('base_stats', 'TEXT')
        ]
        
        added_columns = []
        
        for col_name, col_type in new_columns:
            if col_name not in columns:
                print(f"➕ Adding column: {col_name}")
                try:
                    cursor.execute(f"ALTER TABLE pokemon ADD COLUMN {col_name} {col_type}")
                    added_columns.append(col_name)
                except sqlite3.OperationalError as e:
                    if "duplicate column name" not in str(e).lower():
                        print(f"⚠️  Warning adding {col_name}: {e}")
            else:
                print(f"✅ Column {col_name} already exists")
        
        conn.commit()
        
        if added_columns:
            print(f"🎉 Successfully added {len(added_columns)} new columns:")
            for col in added_columns:
                print(f"   - {col}")
        else:
            print("✅ All columns already exist - no migration needed")
        
        # Verify the migration
        cursor.execute("PRAGMA table_info(pokemon)")
        final_columns = [row[1] for row in cursor.fetchall()]
        print(f"📊 Pokemon table now has {len(final_columns)} columns")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def create_new_database():
    """Create a new database with the full schema"""
    print("🆕 Creating new database with full PokeAPI schema...")
    
    # Import Flask app to create database
    try:
        from app import create_app
        from app.models.pokemon import db
        
        app = create_app()
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ New database created successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Failed to create new database: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting database migration for PokeAPI integration...")
    
    if migrate_database():
        print("🎉 Database migration completed successfully!")
        print("\n💡 You can now import Pokemon with enhanced PokeAPI data!")
    else:
        print("❌ Database migration failed!")
        sys.exit(1)