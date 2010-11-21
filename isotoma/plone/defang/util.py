
def unrestrictedTraverse(app, path):
    current = app
    for p in path:
        current = getattr(current, p)
    return current
