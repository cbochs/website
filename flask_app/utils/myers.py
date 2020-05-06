from base64 import b64encode, b64decode


# An implementation following James Coglan's article: The Myers diff algorithm
# https://blog.jcoglan.com/2017/02/12/the-myers-diff-algorithm-part-1/


def diff(a, b, key=None):
    trace = _shortest_edit(a, b, key=key)
    steps = _backtrack(a, b, trace)
    return steps


def apply(a, b, steps):
    n, m = len(a), len(b)
    x, y = 0, 0
    i = 0

    ap = []

    if len(steps) == 0:
        return a

    while x < n and y < m:
        if i < len(steps):
            px, py, nx, ny = steps[i]
        else:
            px, py, nx, ny = -1, -1, -1, -1

        if x == px and y == py:
            if px == nx:
                ap.append(b[py])
            if py == ny:
                pass # remove a[px]
            x, y = nx, ny
            i = i + 1
        else:
            ap.append(a[x])
            x, y = x + 1, y + 1

    return ap


def revert(a, b, steps):
    pass # TODO


def explain(a, b, steps, key=None):
    if key is None:
        key = lambda x: x

    print('DIFF')
    for px, py, x, y in steps:
        elem_a = key(a[px]) if px < len(a) else None
        elem_b = key(b[py]) if py < len(b) else None
        if x == px:
            print(f'\033[32m + {elem_b}\033[39m')
        elif y == py:
            print(f'\033[31m - {elem_a}\033[39m')
        else:
            print(f'   {elem_a}')
    print('\n')


def _shortest_edit(a, b, key=None):
    n, m = len(a), len(b)

    if key is None:
        key = lambda x: x

    # The time complexity of this algorithm is O(n + m)
    # The space complexity is bad with O((n + m)**2)
    max_ = n + m

    v = [0 for _ in range(-max_, max_ + 1)] # store only the x-coordinates
    t = [] # keep a trace for backtracking the steps afterwards

    # Working with the principle that,
    # - move RIGHT along the grid -> delete from a
    # - move DOWN  along the grid -> insert from b

    # The negative indexing used with k is a neat workaround for realizing
    # an array with a centred zero value. This can be achieved by making the
    # values array twice the maximum number of steps. E.g.
    # v[-max] ... v[-2] v[-1] v[0] v[1] v[2] v[3] ... v[max]

    for d in range(0, max_ + 1): # need to be inclusive
        # We need to keep a copy of every iteration so that we can backtrace
        t.append(v.copy())

        for k in range(-d, d + 1, 2): # again, inclusive
            # -d indicates we are moving directly down the wall of the grid
            # +d indicates we are moving directly east the wall of the grid
            # ~d if ...
            if k == -d or (k != d and v[k - 1] < v[k + 1]):
                x = v[k + 1]     # move DOWN
            else:
                x = v[k - 1] + 1 # move RIGHT

            y = x - k

            while x < n and y < m and key(a[x]) == key(b[y]):
                x, y = x + 1, y + 1

            v[k] = x # don't need to store y, can be inferred

            if x >= n and y >= m:
                return t


def _backtrack(a, b, trace):
    x, y = len(a), len(b) # we are starting at the end -> beginning

    s = []

    for i, v in enumerate(reversed(trace)):
        d = len(trace) - 1 - i # can't do reversed(enumerate(trace))... :P
        k = x - y

        if k == -d or (k != d and v[k - 1] < v[k + 1]):
            prev_k = k + 1 # move UP
        else:
            prev_k = k - 1 # move LEFT

        prev_x = v[prev_k]
        prev_y = prev_x - prev_k

        while x > prev_x and y > prev_y:
            s.append((x - 1, y - 1, x, y))
            x, y = x - 1, y - 1

        if d > 0:
            s.append((prev_x, prev_y, x, y))

        x, y = prev_x, prev_y

    # The steps are now in reverse order, but correct direction
    s.reverse()

    return s


def _encode(steps):
    steps_serial = '\n'.join([' '.join(map(str, step)) for step in steps])
    steps_b64 = b64encode(steps_serial.encode('ascii')).decode('ascii')
    return steps_b64


def _decode(steps_b64):
    steps_serial = b64decode(steps_b64).decode('ascii')
    steps = [tuple(map(int, step.split(' '))) for step in steps_serial.split('\n')]
    return steps
