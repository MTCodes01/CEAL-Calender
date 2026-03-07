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
        ('d-ceal', 'DAKSHA', '#EF4444', 0),    # Red
        ('y-ceal', 'YANTHRA', '#10B981', 1),   # Green
        ('foss', 'FOSS', '#14B8A6', 2),        # Teal/Green
        ('iedc', 'IEDC', '#F59E0B', 3),        # Amber
        ('ieee', 'IEEE', '#3B82F6', 4),        # Blue
        ('iste', 'ISTE', '#6366F1', 5),        # indigo
        ('tinkerhub', 'TinkerHub', '#EC4899', 6), # Pink
        ('yavanika', 'Yavanika', '#8B5CF6', 7),   # Purple
        ('nss', 'NSS', '#EF4444', 8),          # Red
        ('sports', 'Sports', '#F97316', 9),     # Orange
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
    # Format: (slug, name, parent_slug, order, color_override)
    children = [
        # FOSS Sub-clubs
        ('create101', 'CREATE101', 'foss', 0, '#EF4444'),  # Red
        ('embed202', 'EMBED202', 'foss', 1, '#F59E0B'),  # Yellow
        ('train303', 'TRAIN303', 'foss', 2, '#3B82F6'),  # Blue
        ('hack404', 'HACK404', 'foss', 3, '#10B981'),   # Green
        ('deploy505', 'DEPLOY505', 'foss', 4, '#EC4899'),  # Pink/Purple
        
        # IEDC Sub-clubs
        ('edc', 'EDC', 'iedc', 0, None),
        
        # IEEE Sub-clubs
        ('ieee-cs', 'IEEE CS', 'ieee', 0, None),
        ('ieee-embs', 'IEEE EMBS', 'ieee', 1, None),
        ('ieee-ias', 'IEEE IAS', 'ieee', 2, None),
        ('ieee-pels', 'IEEE PELS', 'ieee', 3, None),
        ('ieee-pes', 'IEEE PES', 'ieee', 4, None),
        ('ieee-ras', 'IEEE RAS', 'ieee', 5, None),
        ('ieee-sps', 'IEEE SPS', 'ieee', 6, None),
        ('ieee-wie', 'IEEE WIE', 'ieee', 7, None),
    ]
    
    for slug, name, parent_slug, order, color_override in children:
        parent = parent_map.get(parent_slug)
        # Use a slightly different shade or the same as parent
        color = color_override if color_override else parent.color
        
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
