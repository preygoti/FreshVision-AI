import os

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

    target_link = '<link rel="stylesheet" href="/static/css/style.css">'
    if target_link in html:
        style_block = f'<style id="inlined-freshvision-styles">\n{css}\n</style>'
        html = html.replace(target_link, style_block)
        print('[+] Inlined style.css into index.html')
    else:
        print('[!] target_link not found')

    target_script = '<script src="/static/js/app.js"></script>'
    if target_script in html:
        script_block = f'<script id="inlined-freshvision-scripts">\n{js}\n</script>'
        html = html.replace(target_script, script_block)
        print('[+] Inlined app.js into index.html')
    else:
        print('[!] target_script not found')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'[+] templates/index.html updated successfully. Size: {len(html)} bytes')

if __name__ == '__main__':
    inline_assets()
