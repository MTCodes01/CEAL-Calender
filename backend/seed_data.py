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
    Create all clubs with proper hierarchy and colors
    """
    # Parent Clubs
    parents = [
        ('ieee', 'IEEE', '#3B82F6'),
        ('foss', 'FOSS', '#10B981'),
        ('iedc', 'IEDC', '#F59E0B'),
        ('other', 'Other', '#6B7280'),
    ]

    parent_map = {}
    for slug, name, color in parents:
        club, created = Club.objects.update_or_create(
            slug=slug,
            defaults={'name': name, 'color': color, 'parent': None}
        )
        parent_map[slug] = club
        print(f"{'✓' if created else '→'} Parent: {name}")

    # Child Clubs
    children = [
        # IEEE Sub-clubs
        ('ieee-cs', 'IEEE CS', 'ieee'),
        ('ieee-embs', 'IEEE EMBS', 'ieee'),
        ('ieee-ias', 'IEEE IAS', 'ieee'),
        ('ieee-pes', 'IEEE PES', 'ieee'),
        ('ieee-pels', 'IEEE PELS', 'ieee'),
        ('ieee-ras', 'IEEE RAS', 'ieee'),
        ('ieee-sps', 'IEEE SPS', 'ieee'),
        ('ieee-wie', 'IEEE WIE', 'ieee'),
        
        # FOSS Sub-clubs
        ('foss-create101', 'CREATE101', 'foss'),
        ('foss-embed202', 'EMBED202', 'foss'),
        ('foss-train303', 'TRAIN303', 'foss'),
        ('foss-hack404', 'HACK404', 'foss'),
        ('foss-deploy505', 'DEPLOY505', 'foss'),
        
        # IEDC Sub-clubs
        ('iedc-edc', 'EDC', 'iedc'),
        ('iedc-impact-cafe', 'Impact Cafe', 'iedc'),
        
        # Other Clubs (assigned to 'other' parent for grouping, or kept independent if preferred)
        ('iste', 'ISTE', 'other'),
        ('tinkerhub', 'TinkerHub', 'other'),
        ('yavanika', 'Yavanika', 'other'),
        ('nss', 'NSS', 'other'),
        ('sports', 'Sports Club', 'other'),
    ]
    
    created_count = 0
    updated_count = 0
    
    for idx, (slug, name, parent_slug) in enumerate(children):
        # Use a distinct color for children or inherit/derive if needed. 
        # For now, using the palette cyclically.
        color = COLORS[idx % len(COLORS)]
        parent = parent_map.get(parent_slug)
        
        club, created = Club.objects.update_or_create(
            slug=slug,
            defaults={'name': name, 'color': color, 'parent': parent}
        )
        
        if created:
            created_count += 1
            print(f"  ✓ Child: {name} -> {parent.name}")
        else:
            updated_count += 1
            print(f"  → Updated: {name} -> {parent.name}")
    
    print(f"\n{'='*50}")
    print(f"Total clubs: {Club.objects.count()}")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Seeding clubs...")
    print(f"{'='*50}\n")
    create_clubs()
