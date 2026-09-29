import os
import re

def inline_assets():
    html_path = os.path.join('templates', 'index.html')
    css_path = os.path.join('static', 'css', 'style.css')
    js_path = os.path.join('static', 'js', 'app.js')

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()

    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()

    style_block = f'<style id="inlined-freshvision-styles">\n{css}\n</style>'
    if '<style id="inlined-freshvision-styles">' in html:
        html = re.sub(
            r'<style id="inlined-freshvision-styles">.*?</style>',
            style_block,
            html,
            flags=re.DOTALL
        )
        print('[+] Replaced existing inlined CSS block with updated style.css')
    elif '<link rel="stylesheet" href="/static/css/style.css">' in html:
        html = html.replace('<link rel="stylesheet" href="/static/css/style.css">', style_block)
        print('[+] Inlined style.css into index.html')

    script_block = f'<script id="inlined-freshvision-scripts">\n{js}\n</script>'
    if '<script id="inlined-freshvision-scripts">' in html:
        html = re.sub(
            r'<script id="inlined-freshvision-scripts">.*?</script>',
            script_block,
            html,
            flags=re.DOTALL
        )
        print('[+] Replaced existing inlined JS block with updated app.js')
    elif '<script src="/static/js/app.js"></script>' in html:
        html = html.replace('<script src="/static/js/app.js"></script>', script_block)
        print('[+] Inlined app.js into index.html')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'[+] templates/index.html updated successfully. Size: {len(html)} bytes')

if __name__ == '__main__':
    inline_assets()
