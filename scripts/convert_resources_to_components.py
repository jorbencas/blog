import re
import sys
import os

card_pattern = re.compile(
    r'<a href="([^"]+)" class="flex items-start gap-4 p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 hover:border-cyan-400 dark:hover:border-cyan-400 hover:shadow-xl hover:-translate-y-1 transition-all no-underline group">'
    r'\s*<img src="[^"]*" width="20" height="20" class="[^"]*" alt="[^"]*" loading="lazy" />'
    r'\s*<div>'
    r'\s*<span class="font-bold text-slate-900 dark:text-white group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors">([^<]+)</span>'
    r'\s*<p class="text-sm text-slate-500 dark:text-slate-400 mt-0\.5 leading-snug">(.*?)</p>'
    r'\s*</div>'
    r'\s*</a>',
    re.DOTALL
)

def convert_file(filepath):
    with open(filepath) as f:
        content = f.read()

    if "import ResourceCard from" in content:
        print(f"  Skipping {filepath} (already converted)")
        return

    lines = content.split('\n')

    fm_end = 0
    for i, line in enumerate(lines):
        if i > 0 and line.strip() == '---':
            fm_end = i + 1
            break

    result = []
    result.extend(lines[:fm_end])
    result.append("import ResourceCard from '@components/ResourceCard.astro';")
    result.append("import ResourceCategory from '@components/ResourceCategory.astro';")
    result.append('')

    section_header_pattern = re.compile(
        r'<div class="not-prose mt-12 mb-6"><h2 class="inline-flex items-center gap-2 bg-gradient-to-r from-sky-800 to-cyan-500 dark:from-sky-600 dark:to-cyan-400 px-5 py-2\.5 text-xs sm:text-sm font-black uppercase tracking-\[0\.25em\] text-white dark:text-slate-900 shadow-\[4px_4px_0px_0px_rgba\(6,182,212,0\.3\)\]" id="([^"]*)">([^<]+)</h2></div>',
        re.DOTALL
    )

    i = fm_end
    while i < len(lines):
        line = lines[i]
        hm = section_header_pattern.match(line)

        if hm:
            section_id = hm.group(1)
            section_title = hm.group(2)

            i += 1
            while i < len(lines) and 'not-prose grid' not in lines[i]:
                i += 1
            i += 1

            depth = 1
            card_lines = []
            while i < len(lines):
                l = lines[i]
                depth += l.count('<div') - l.count('</div>')
                if depth <= 0:
                    break
                card_lines.append(l)
                i += 1

            cards_text = '\n'.join(card_lines)

            result.append(f'<ResourceCategory id="{section_id}" title="{section_title}">')
            result.append('')

            for cm in card_pattern.finditer(cards_text):
                href = cm.group(1)
                title = cm.group(2)
                description = cm.group(3)
                description = description.replace('&amp;', '&')
                result.append(f'<ResourceCard')
                result.append(f'  href="{href}"')
                result.append(f'  title="{title}"')
                result.append(f'  description="{description}"')
                result.append(f'/>')
                result.append('')

            result.append('</ResourceCategory>')
            result.append('')
        else:
            result.append(line)

        i += 1

    with open(filepath, 'w') as f:
        f.write('\n'.join(result))

    sections = '\n'.join(result).count('<ResourceCategory')
    cards = '\n'.join(result).count('<ResourceCard')
    print(f"  Converted: {sections} sections, {cards} cards")
    return sections, cards


if __name__ == '__main__':
    blog_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    posts_dir = os.path.join(blog_dir, 'src', 'content', 'posts')

    targets = sys.argv[1:] if len(sys.argv) > 1 else [
        'resources.mdx',
        'resources2.mdx',
        'resources3.mdx',
    ]

    for target in targets:
        path = os.path.join(posts_dir, target)
        if os.path.exists(path):
            print(f"Converting {target}...")
            convert_file(path)
        else:
            print(f"Not found: {path}")

    print("Done!")
