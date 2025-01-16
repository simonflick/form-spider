from collections import defaultdict

class URLTree:
    def __init__(self):
        self.tree = defaultdict(self.tree_factory)

    def tree_factory(self):
        return defaultdict(self.tree_factory)

    def add(self, url):
        parts = url.replace('https://', '').replace('http://', '').rstrip('/').split('/')
        d = self.tree
        for part in parts:
            d = d[part]

    def format(self, form_messages, base_netloc):
        return self.format_rec(self.tree, '', '', form_messages, base_netloc)

    def format_rec(self, tree, prefix, path, form_messages, base_netloc):
        output = []
        
        for key in sorted(tree.keys()):
            line = f'{prefix}{key}/'
            current_path = path + key + '/'
            full_url = construct_url(base_netloc, current_path)

            if full_url in form_messages:
                line += f'  {form_messages[full_url]}'

            output.append(line)

            if tree[key]:
                sub_prefix = prefix + '    '
                output.append(self.format_rec(tree[key], sub_prefix, current_path, form_messages, base_netloc))

        return '\n'.join(output)

def construct_url(base_netloc, path):
    if path.startswith(base_netloc):
        return f'https://{path}'.rstrip('/')
    else:
        return f'https://{base_netloc}/{path}'.rstrip('/')