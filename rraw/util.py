def children(listing):
    return listing['data']['children']

def extract_body(listing, skip_authors=[]):
    for child in children(listing):
        kind = child['kind']
        data = child['data']

        if not 'body' in data:
            continue

        if skip_authors and data['author'] in skip_authors:
            continue

        yield data['body']

        if kind == 't1' and data['replies']:
            for c in extract_body(data['replies']):
                yield c

