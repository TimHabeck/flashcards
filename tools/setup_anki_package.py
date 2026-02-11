import genanki
import csv
import os
import hashlib
import glob

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..'))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
EXPORTS_DIR = os.path.join(PROJECT_ROOT, 'exports')

# Ensure exports directory exists
os.makedirs(EXPORTS_DIR, exist_ok=True)

def load_file(filename):
    with open(os.path.join(TEMPLATES_DIR, filename), 'r', encoding='utf-8') as f:
        return f.read()

def get_deterministic_id(source_string):
    """Generates a consistent integer ID from a string."""
    hash_object = hashlib.sha256(source_string.encode('utf-8'))
    # Take first 8 bytes and convert to int, then modulo to fit Anki's ID range
    return int(hash_object.hexdigest()[:15], 16)

def get_course_name(course_dir):
    """Reads course name from course_info.txt"""
    info_path = os.path.join(course_dir, 'course_info.txt')
    if not os.path.exists(info_path):
        return os.path.basename(course_dir).replace('_', ' ').title()
    
    with open(info_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('course_name:'):
                return line.split(':', 1)[1].strip()
    return os.path.basename(course_dir).replace('_', ' ').title()


# 1. Define the Note Model
MODEL_ID = get_deterministic_id("AI Flashcards v1")
FRONT_HTML = load_file('front.html')
BACK_HTML = load_file('back.html')
STYLE_CSS = load_file('style.css')

my_model = genanki.Model(
  MODEL_ID,
  'AI Flashcards',
  fields=[
    {'name': 'Front'},
    {'name': 'Back'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': FRONT_HTML,
      'afmt': BACK_HTML,
    },
  ],
  css=STYLE_CSS,
  sort_field_index=0
)

# 2. Setup CLI arguments
import argparse
parser = argparse.ArgumentParser(description='Generate Anki packages for courses.')
parser.add_argument('course_folder', nargs='?', help='Optional: Specific course folder name to process')
args = parser.parse_args()

# 3. Iterate through courses and create packages
COURSES_DIR = os.path.join(PROJECT_ROOT, 'courses')
print(f"Scanning for courses in {COURSES_DIR}...")

if not os.path.exists(COURSES_DIR):
    print(f"Error: Directory {COURSES_DIR} not found.")
    courses = []
else:
    # If specific course requested
    if args.course_folder:
        if os.path.isdir(os.path.join(COURSES_DIR, args.course_folder)):
            courses = [args.course_folder]
        else:
            print(f"Error: Course folder '{args.course_folder}' not found in {COURSES_DIR}")
            courses = []
    else:
        # Scan all
        courses = [d for d in os.listdir(COURSES_DIR) if os.path.isdir(os.path.join(COURSES_DIR, d))]

for course in courses:
    course_path = os.path.join(COURSES_DIR, course)
    export_dir = os.path.join(course_path, 'anki_exports')
    
    if not os.path.exists(export_dir):
        print(f"Skipping {course}: No anki_exports folder found.")
        continue
        
    print(f"Processing course: {course}")
    
    # Create the unique deck for this course
    course_name = get_course_name(course_path)
    deck_name = f"Uni::{course_name}"
    deck_id = get_deterministic_id(deck_name)
    
    course_deck = genanki.Deck(deck_id, deck_name)
    
    # Iterate through all CSVs in anki_exports
    export_files = glob.glob(os.path.join(export_dir, '*.csv'))
    
    if not export_files:
        print(f"  No CSV files found in {export_dir}")
        continue

    for export_file in export_files:
        print(f"  - Reading {os.path.basename(export_file)}")
        with open(export_file, 'r', encoding='utf-8') as csvfile:
            # Check for header
            sample = csvfile.read(1024)
            csvfile.seek(0)
            has_header = csv.Sniffer().has_header(sample)
            
            reader = csv.reader(csvfile)
            if has_header:
                 pass

            # Robust reader: manually handle rows
            for row in reader:
                if not row or len(row) < 2: continue # Skip empty lines
                
                # Expected format: front_html, back_html, tags
                front = row[0]
                back = row[1]
                tags = row[2] if len(row) > 2 else ''
                
                # Generate deterministic GUID from Front content
                note_guid = get_deterministic_id(front)
                
                # Create the note
                my_note = genanki.Note(
                    model=my_model,
                    fields=[front, back],
                    guid=note_guid,
                    tags=tags.split(' ')
                )
                
                course_deck.add_note(my_note)
    
    # Save the Package PER COURSE in the EXPORTS_DIR
    output_filename = f"{course_name}.apkg"
    output_path = os.path.join(EXPORTS_DIR, output_filename)
    print(f"  Saving package to {output_filename}...")
    genanki.Package(course_deck).write_to_file(output_path)

print("Done!")
