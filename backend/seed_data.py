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
    Create all clubs with proper hierarchy, colors, and order
    """
    # Parent Clubs (Major Clubs)
    parents = [
        ('foss', 'FOSS', '#10B981', 0),
        ('iedc', 'IEDC', '#F59E0B', 1),
        ('ieee', 'IEEE', '#3B82F6', 2),
        ('iste', 'ISTE', '#6366F1', 3),
        ('tinkerhub', 'TinkerHub', '#EC4899', 4),
        ('yavanika', 'Yavanika', '#8B5CF6', 5),
        ('nss', 'NSS', '#EF4444', 6),
        ('sports', 'Sports', '#F97316', 7),
    ]

    parent_map = {}
    for slug, name, color, order in parents:
        club, created = Club.objects.update_or_create(
            slug=slug,
            defaults={'name': name, 'color': color, 'parent': None, 'order': order}
        )
        parent_map[slug] = club
        print(f"{'✓' if created else '→'} Parent: {name}")

    # Child Clubs (Sub-clubs)
    children = [
        # FOSS Sub-clubs
        ('create101', 'CREATE101', 'foss', 0),
        ('embed202', 'EMBED202', 'foss', 1),
        ('train303', 'TRAIN303', 'foss', 2),
        ('hack404', 'HACK404', 'foss', 3),
        ('deploy505', 'DEPLOY505', 'foss', 4),
        
        # IEDC Sub-clubs
        ('edc', 'EDC', 'iedc', 0),
        
        # IEEE Sub-clubs
        ('ieee-cs', 'CS', 'ieee', 0),
        ('ieee-embs', 'EMBS', 'ieee', 1),
        ('ieee-ias', 'IAS', 'ieee', 2),
        ('ieee-pels', 'PELS', 'ieee', 3),
        ('ieee-pes', 'PES', 'ieee', 4),
        ('ieee-ras', 'RAS', 'ieee', 5),
        ('ieee-sps', 'SPS', 'ieee', 6),
        ('ieee-wie', 'WIE', 'ieee', 7),
    ]
    
    for slug, name, parent_slug, order in children:
        parent = parent_map.get(parent_slug)
        # Use a slightly different shade or the same as parent
        color = parent.color
        
        club, created = Club.objects.update_or_create(
            slug=slug,
            defaults={'name': name, 'color': color, 'parent': parent, 'order': order}
        )
        print(f"  {'✓' if created else '→'} Child: {name} -> {parent.name}")

    # Remove old 'other' group if it exists
    Club.objects.filter(slug='other').delete()

    print(f"\n{'='*50}")
    print(f"Total clubs: {Club.objects.count()}")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Seeding clubs...")
    print(f"{'='*50}\n")
    create_clubs()
