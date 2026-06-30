import math


def set_test_path():
    return "src/tests/"


def tuplepow(xs, pow):
    out = ()
    # Append each x^2 to out
    for x in xs:
        out += (math.pow(x, pow),)
    return out


def tuplesquare(xs):
    return tuplepow(xs, 2)


def tuplecube(xs):
    return tuplepow(xs, 3)


def tuplesqrt(xs):
    return tuplepow(xs, 0.5)


def col_square(df, x, newcol):
    df[newcol] = df[x].apply(math.pow, args=(2,))
    return df


def col_sqrt(df, x, newcol):
    df[newcol] = df[x].apply(math.pow, args=(0.5,))
    return df
