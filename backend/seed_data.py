"""
Seed data script to populate clubs

Run this script with:
    python manage.py shell < seed_data.py

Or manually:
    python manage.py shell
    >>> exec(open('seed_data.py').read())
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ceal_calendar.settings')
django.setup()

from clubs.models import Club

# Color palette for clubs
COLORS = [
    '#3B82F6',  # Blue
    '#EF4444',  # Red
    '#10B981',  # Green
    '#F59E0B',  # Amber
    '#8B5CF6',  # Purple
    '#EC4899',  # Pink
    '#14B8A6',  # Teal
    '#F97316',  # Orange
    '#06B6D4',  # Cyan
    '#84CC16',  # Lime
    '#6366F1',  # Indigo
    '#A855F7',  # Violet
]

def create_clubs():
    """
    Create all clubs with proper colors
    """
    clubs_data = [
        # IEEE Clubs
        ('ieee-cs', 'IEEE Computer Society'),
        ('ieee-embs', 'IEEE EMBS'),
        ('ieee-ias', 'IEEE IAS'),
        ('ieee-pes', 'IEEE PES'),
        ('ieee-pels', 'IEEE PELS'),
        ('ieee-ras', 'IEEE RAS'),
        ('ieee-sps', 'IEEE SPS'),
        ('ieee-wie', 'IEEE WIE'),
        
        # FOSS Clubs
        ('foss-create101', 'FOSS CREATE101'),
        ('foss-embed202', 'FOSS EMBED202'),
        ('foss-train303', 'FOSS TRAIN303'),
        ('foss-hack404', 'FOSS HACK404'),
        ('foss-deploy505', 'FOSS DEPLOY505'),
        
        # IEDC Clubs
        ('iedc-edc', 'EDC'),
        ('iedc-impact-cafe', 'Impact Cafe'),
        
        # Other Clubs
        ('iste', 'ISTE'),
        ('tinkerhub', 'TinkerHub'),
        ('yavanika', 'Yavanika'),
        ('nss', 'NSS'),
        ('sports', 'Sports Club'),
    ]
    
    created_count = 0
    updated_count = 0
    
    for idx, (slug, name) in enumerate(clubs_data):
        color = COLORS[idx % len(COLORS)]
        
        club, created = Club.objects.update_or_create(
            slug=slug,
            defaults={'name': name, 'color': color}
        )
        
        if created:
            created_count += 1
            print(f"✓ Created: {name} ({slug}) - {color}")
        else:
            updated_count += 1
            print(f"→ Updated: {name} ({slug}) - {color}")
    
    print(f"\n{'='*50}")
    print(f"Created {created_count} new clubs")
    print(f"Updated {updated_count} existing clubs")
    print(f"Total clubs: {Club.objects.count()}")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Seeding clubs...")
    print(f"{'='*50}\n")
    create_clubs()
