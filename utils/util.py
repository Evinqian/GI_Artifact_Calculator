from utils.data import weight

def prob(m, a, b, c, d):
    w = weight.copy()
    p = 1
    w[m] = 0
    p = p * w[a] / sum(w)
    w[a] = 0
    p = p * w[b] / sum(w)
    w[b] = 0
    p = p * w[c] / sum(w)
    w[c] = 0
    p = p * w[d] / sum(w)
    return p


def dict_mul(x: dict, a: dict) -> dict | None:
    res = dict()
    try:
        for k1, v1 in x.items():
            if v1 == 0.0:
                continue
            for k2, v2 in a.items():
                if v2 == 0.0:
                    continue
                k, v = max(k1, k2), v1 * v2
                if k not in res:
                    res[k] = 0
                res[k] += v
    except Exception as e:
        print("dict_mul error: %s" % repr(e))
        return None
    return res

def dict_add(x: dict, a: dict) -> dict | None:
    res = dict()
    try:
        for k1, v1 in x.items():
            if v1 == 0.0:
                continue
            for k2, v2 in a.items():
                if v2 == 0.0:
                    continue
                k, v = (k1 + k2), v1 * v2
                if k not in res:
                    res[k] = 0
                res[k] += v
    except Exception as e:
        print("dict_add error: %s" % repr(e))
        return None
    return res

def dict_pow(x: dict, a: int) -> dict | None:
    res = x.copy()
    while a > 0:
        if a % 2:
            res = dict_mul(res, x)
            a -= 1
        else:
            res = dict_mul(res, res)
            a >>= 1
    return res
