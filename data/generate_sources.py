""" Helper script that creates HTML list entries from sources data in JSON files.
"""

import json
import os
import re
from pathlib import Path

def has_date_in_title(work_title):
    """Check if work title contains a date pattern like 'vom DD.MM.YYYY' or similar."""
    # Look for date patterns like "vom 17.07.1912" or "vom 13.08.1814"
    date_pattern = r'vom\s+\d{1,2}\.\d{1,2}\.\d{4}'
    return bool(re.search(date_pattern, work_title, re.IGNORECASE))

def generate_sources_html():
    """Generate sources.html from all JSON files."""
    script_dir = Path(__file__).parent
    json_files = sorted([f for f in script_dir.glob("*.json") if f.name != "sources.html"])

    output_lines = []

    for idx, json_file in enumerate(json_files, start=1):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            name = data['name']
            work_title = data['work-title']
            author = data.get('author', '')
            year = data['year']
            page = data['page']
            source_urls = data['sources']

            parts = [f'<li id="lit{idx}"><em>{name}</em> in „{work_title}“']
            if author:
                parts.append(f'von {author}')
            if year and not has_date_in_title(work_title):
                parts.append(f'({year})')
            parts.append(f'S. {page}')
            parts.append(', '.join([f'<a href="{url}">↗&#xFE0E;</a>' for url in source_urls]) + '</li>')
            output_lines.append(' '.join(parts))

        except Exception as e:
            print(f"Error processing {json_file}: {e}", file=os.sys.stderr)
            continue

    output_file = script_dir / 'sources.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"Generated {output_file} with {len(output_lines)} entries")

if __name__ == '__main__':
    generate_sources_html()