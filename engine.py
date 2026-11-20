import json, os, sys, urllib.request, urllib.error
ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")
def post(path, body):
    req = urllib.request.Request(ENV_URL + path, data=json.dumps(body).encode(),
        headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code}")
V = (0, 100, 320, 330, 500, 900, 0)
S64 = [r * 16 + f for r in range(8) for f in range(8)]
MP = [[0,0,0,0],[5,10,10,-20],[5,-5,-10,0],[0,0,0,20],[5,5,10,25],[10,10,20,30],[50,50,50,50],[0,0,0,0]]
MN = [[-50,-40,-30,-30],[-40,-20,0,0],[-30,0,10,15],[-30,5,15,20],[-30,0,15,20],[-30,5,10,15],[-40,-20,0,5],[-50,-40,-30,-30]]
MB = [[-20,-10,-10,-10],[-10,0,0,0],[-10,0,5,10],[-10,5,5,10],[-10,0,10,10],[-10,10,10,10],[-10,5,0,0],[-20,-10,-10,-10]]
MR = [[0,0,0,0],[5,10,10,10],[-5,0,0,0],[-5,0,0,0],[-5,0,0,0],[-5,0,0,0],[-5,0,0,0],[0,0,0,5]]
MQ = [[-20,-10,-10,-5],[-10,0,0,0],[-10,0,5,5],[-5,0,5,5],[0,0,5,5],[-10,5,5,5],[-10,0,5,0],[-20,-10,-10,-5]]
MK = [[-30,-40,-40,-50],[-30,-40,-40,-50],[-30,-40,-40,-50],[-30,-40,-40,-50],[-20,-30,-30,-40],[-10,-20,-20,-20],[20,20,0,0],[20,30,10,0]]
EK = [[-50,-40,-30,-20],[-30,-20,-10,0],[-30,-10,20,30],[-30,-10,30,40],[-30,-10,30,40],[-30,-10,20,30],[-30,-20,-10,0],[-50,-40,-30,-20]]
MG = (None, MP, MN, MB, MR, MQ, MK)
EG = (None, MP, MN, MB, MR, MQ, EK)
def _f(tab):
    out = [None] * 7
    for t in range(1, 7):
        arr = [0] * 128
        for sq in S64:
            r, f = sq >> 4, sq & 7
            if f > 3:
                f = 7 - f
            arr[sq] = V[t] + tab[t][r][f]
        out[t] = arr
    return out
MW = _f(MG)
EW = _f(EG)
KN = (31, 33, 18, 14, -14, -18, -31, -33)
KG = (1, -1, 15, -15, 16, -16, 17, -17)
DG = (15, 17, -15, -17)
ST = (1, -1, 16, -16)
DS = DG + ST
import random as _rnd
_rnd.seed(0xC0FFEE)
Z = [[_rnd.getrandbits(64) for _ in range(128)] for _ in range(13)]
ZS = _rnd.getrandbits(64)
ZC = [_rnd.getrandbits(64) for _ in range(16)]
ZE = [_rnd.getrandbits(64) for _ in range(8)]
class Ps:
    __slots__ = ("b", "turn", "cast", "ep", "hash", "phase", "wk", "bk")
    def __init__(self):
        self.b = [0] * 128
        self.turn = 1
        self.cast = 0
        self.ep = -1
        self.hash = 0
        self.phase = 0
        self.wk = -1
        self.bk = -1
def fen(fen):
    p = Ps()
    parts = fen.split()
    rows = parts[0].split("/")
    for r, row in enumerate(rows):
        rank = 7 - r
        f = 0
        for c in row:
            if c.isdigit():
                f += int(c)
            else:
                pc = "PNBRQK".index(c.upper()) + 1
                if c.islower():
                    pc = -pc
                sq = rank * 16 + f
                p.b[sq] = pc
                p.hash ^= Z[pc + 6][sq]
                if abs(pc) == 6:
                    if pc > 0:
                        p.wk = sq
                    else:
                        p.bk = sq
                f += 1
    p.turn = 1 if parts[1] == "w" else -1
    if p.turn == -1:
        p.hash ^= ZS
    c = parts[2]
    p.cast = ("K" in c) + 2 * ("Q" in c) + 4 * ("k" in c) + 8 * ("q" in c)
    p.hash ^= ZC[p.cast]
    if parts[3] != "-":
        ep = (ord(parts[3][0]) - 97) + (int(parts[3][1]) - 1) * 16
        p.ep = ep
        p.hash ^= ZE[ep & 7]
    ph = 0
    for sq in S64:
        pc = p.b[sq]
        if pc:
            t = abs(pc)
            if t == 2 or t == 3:
                ph += 1
            elif t == 4:
                ph += 2
            elif t == 5:
                ph += 4
    p.phase = ph
    return p
def att(p, sq, by):
    b = p.b
    if by == 1:
        for d in (-15, -17):
            t = sq + d
            if not (t & 0x88) and b[t] == 1:
                return True
    else:
        for d in (15, 17):
            t = sq + d
            if not (t & 0x88) and b[t] == -1:
                return True
    for d in KN:
        t = sq + d
        if not (t & 0x88) and b[t] == by * 2:
            return True
    for d in KG:
        t = sq + d
        if not (t & 0x88) and b[t] == by * 6:
            return True
    for d in DS:
        t = sq + d
        while not (t & 0x88):
            pc = b[t]
            if pc:
                if pc == by * 5 or pc == by * (3 + (d in ST)):
                    return True
                break
            t += d
    return False
def gen(p, co=False):
    b = p.b
    turn = p.turn
    ms = []
    for sq in S64:
        pc = b[sq]
        if pc == 0 or (pc > 0) != (turn > 0):
            continue
        t = abs(pc)
        if t == 1:
            d = 16 if turn == 1 else -16
            start = 1 if turn == 1 else 6
            last = 7 if turn == 1 else 0
            one = sq + d
            if not co and not (one & 0x88) and b[one] == 0:
                ms.append((sq, one, 5 if (one >> 4) == last else 0))
                if (one >> 4) != last and (sq >> 4) == start and b[sq + 2 * d] == 0:
                    ms.append((sq, sq + 2 * d, 0))
            for dd in (d - 1, d + 1):
                to = sq + dd
                if to & 0x88:
                    continue
                v = b[to]
                if v != 0 and (v > 0) != (turn > 0):
                    if (to >> 4) == last:
                        ms.append((sq, to, 5))
                    else:
                        ms.append((sq, to, 0))
                elif to == p.ep:
                    ms.append((sq, to, 0))
        elif t == 2:
            for d in KN:
                to = sq + d
                if to & 0x88:
                    continue
                v = b[to]
                if v == 0:
                    if not co:
                        ms.append((sq, to, 0))
                elif (v > 0) != (turn > 0):
                    ms.append((sq, to, 0))
        elif t == 6:
            for d in KG:
                to = sq + d
                if to & 0x88:
                    continue
                v = b[to]
                if v == 0:
                    if not co:
                        ms.append((sq, to, 0))
                elif (v > 0) != (turn > 0):
                    ms.append((sq, to, 0))
            if not co:
                if turn == 1 and sq == 4:
                    if p.cast & 1 and b[5] == 0 and b[6] == 0 and b[7] == 4 and not att(p, 4, -1) and not att(p, 5, -1) and not att(p, 6, -1):
                        ms.append((4, 6, 0))
                    if p.cast & 2 and b[3] == 0 and b[2] == 0 and b[1] == 0 and b[0] == 4 and not att(p, 4, -1) and not att(p, 3, -1) and not att(p, 2, -1):
                        ms.append((4, 2, 0))
                elif turn == -1 and sq == 116:
                    if p.cast & 4 and b[117] == 0 and b[118] == 0 and b[119] == -4 and not att(p, 116, 1) and not att(p, 117, 1) and not att(p, 118, 1):
                        ms.append((116, 118, 0))
                    if p.cast & 8 and b[115] == 0 and b[114] == 0 and b[113] == 0 and b[112] == -4 and not att(p, 116, 1) and not att(p, 115, 1) and not att(p, 114, 1):
                        ms.append((116, 114, 0))
        else:
            dirs = DG if t == 3 else ST if t == 4 else DS
            for d in dirs:
                to = sq + d
                while not (to & 0x88):
                    v = b[to]
                    if v == 0:
                        if not co:
                            ms.append((sq, to, 0))
                    else:
                        if (v > 0) != (turn > 0):
                            ms.append((sq, to, 0))
                        break
                    to += d
    return ms
def dom(p, mv):
    frm, to, promo = mv
    b = p.b
    pc = b[frm]
    cap = b[to]
    u = (frm, to, promo, cap, p.cast, p.ep, p.hash, p.phase)
    p.hash ^= Z[pc + 6][frm]
    if cap:
        p.hash ^= Z[cap + 6][to]
    if abs(pc) == 1 and to == p.ep and cap == 0:
        epp = to - 16 if p.turn == 1 else to + 16
        cap = b[epp]
        b[epp] = 0
        p.hash ^= Z[cap + 6][epp]
        u = (frm, to, promo, cap, p.cast, p.ep, p.hash, p.phase, epp)
    if abs(pc) == 6 and abs(to - frm) == 2:
        if to > frm:
            rs, re_ = frm + 3, frm + 1
        else:
            rs, re_ = frm - 4, frm - 1
        rk = b[rs]
        b[re_] = rk
        b[rs] = 0
        p.hash ^= Z[rk + 6][rs] ^ Z[rk + 6][re_]
    if p.ep != -1:
        p.hash ^= ZE[p.ep & 7]
    p.ep = -1
    if abs(pc) == 1 and abs(to - frm) == 32:
        p.ep = (frm + to) // 2
        p.hash ^= ZE[p.ep & 7]
    oc = p.cast
    if abs(pc) == 6:
        p.cast &= ~(3 if p.turn == 1 else 12)
    if frm == 0 or to == 0:
        p.cast &= ~2
    if frm == 7 or to == 7:
        p.cast &= ~1
    if frm == 112 or to == 112:
        p.cast &= ~8
    if frm == 119 or to == 119:
        p.cast &= ~4
    if p.cast != oc:
        p.hash ^= ZC[oc] ^ ZC[p.cast]
    b[frm] = 0
    npc = (promo if promo else abs(pc)) * p.turn
    b[to] = npc
    if abs(pc) == 6:
        if p.turn == 1:
            p.wk = to
        else:
            p.bk = to
    p.hash ^= Z[npc + 6][to]
    if cap:
        t = abs(cap)
        if t == 2 or t == 3:
            p.phase -= 1
        elif t == 4:
            p.phase -= 2
        elif t == 5:
            p.phase -= 4
    p.turn = -p.turn
    p.hash ^= ZS
    return u
def und(p, mv, u):
    frm, to, promo, cap = u[0], u[1], u[2], u[3]
    b = p.b
    p.turn = -p.turn
    p.cast, p.ep, p.hash, p.phase = u[4], u[5], u[6], u[7]
    npc = b[to]
    b[to] = 0
    b[frm] = npc if not promo else (1 if p.turn == 1 else -1)
    if abs(npc) == 6:
        if p.turn == 1:
            p.wk = frm
        else:
            p.bk = frm
    if len(u) > 8:
        b[u[8]] = cap
    elif cap:
        b[to] = cap
    if abs(npc) == 6 and abs(to - frm) == 2:
        if to > frm:
            rs, re_ = frm + 3, frm + 1
        else:
            rs, re_ = frm - 4, frm - 1
        b[rs] = b[re_]
        b[re_] = 0
def ev(p):
    b = p.b
    mg = 0
    eg = 0
    mt = 0
    ph = p.phase
    if ph > 24:
        ph = 24
    for sq in S64:
        pc = b[sq]
        if pc:
            if pc > 0:
                mg += MW[pc][sq]
                eg += EW[pc][sq]
                mt += V[pc]
            else:
                msq = sq ^ 0x70
                mg -= MW[-pc][msq]
                eg -= EW[-pc][msq]
                mt -= V[-pc]
    s = (mg * ph + eg * (24 - ph)) // 24
    if ph < 8 and abs(mt) > 300:
        a, c = (p.wk, p.bk) if mt > 0 else (p.bk, p.wk)
        f, r = c & 7, c >> 4
        s += (159 - 25 * min(f, 7 - f, r, 7 - r) - 12 * max(abs((a & 7) - f), abs((a >> 4) - r))) * (1 if mt > 0 else -1)
    return s
TT = {}
KL = [[None, None] for _ in range(256)]
ND = 0
BD = 400000
MT = 100000
class SS(Exception):
    pass
def ordm(p, ms, tm, kl=None):
    def score(mv):
        frm, to, promo = mv
        if tm is not None and mv == tm:
            return 1000000
        cap = p.b[to]
        if cap:
            return 10000 + V[abs(cap)] * 10 - V[abs(p.b[frm])] // 10
        if kl is not None and mv in kl:
            return 5000
        return 0
    ms.sort(key=score, reverse=True)
    return ms
def qs(p, alpha, beta, ply):
    global ND
    ND += 1
    if ND >= BD:
        raise SS
    stand = ev(p) * p.turn
    if stand >= beta:
        return beta
    if stand > alpha:
        alpha = stand
    caps = gen(p, co=True)
    ordm(p, caps, None, None)
    for mv in caps:
        u = dom(p, mv)
        if att(p, p.wk if -p.turn == 1 else p.bk, p.turn):
            und(p, mv, u)
            continue
        s = -qs(p, -beta, -alpha, ply + 1)
        und(p, mv, u)
        if s >= beta:
            return beta
        if s > alpha:
            alpha = s
    return alpha
def srch(p, depth, alpha, beta, ply):
    global ND
    ND += 1
    if ND >= BD:
        raise SS
    if depth <= 0:
        return qs(p, alpha, beta, ply)
    chk = att(p, p.wk if p.turn == 1 else p.bk, -p.turn)
    if chk:
        depth += 1
    entry = TT.get(p.hash)
    tm = None
    if entry is not None:
        ed, eflag, escore, emove = entry
        tm = emove
        if ed >= depth:
            if eflag == 0:
                return escore
            if eflag == 1 and escore >= beta:
                return escore
            if eflag == 2 and escore <= alpha:
                return escore
    if depth >= 3 and ply > 0 and p.phase > 4 and not chk:
        oe = p.ep
        p.turn = -p.turn
        p.hash ^= ZS ^ (ZE[oe & 7] if oe != -1 else 0)
        p.ep = -1
        s = -srch(p, depth - 3 - (depth > 5), -beta, -beta + 1, ply + 1)
        p.turn = -p.turn
        p.hash ^= ZS ^ (ZE[oe & 7] if oe != -1 else 0)
        p.ep = oe
        if s >= beta:
            return beta
    ms = gen(p)
    ordm(p, ms, tm, KL[ply])
    best = -MT
    bv = None
    orig_alpha = alpha
    i = 0
    for mv in ms:
        u = dom(p, mv)
        if att(p, p.wk if -p.turn == 1 else p.bk, p.turn):
            und(p, mv, u)
            continue
        d = depth - 1
        if depth >= 3 and i >= 3 and not chk and u[3] == 0 and u[2] == 0 and mv not in KL[ply]:
            d = depth - 2
        s = -srch(p, d, -beta, -alpha, ply + 1)
        und(p, mv, u)
        i += 1
        if s > best:
            best = s
            bv = mv
        if s > alpha:
            alpha = s
        if alpha >= beta:
            if p.b[mv[1]] == 0:
                k = KL[ply]
                if k[0] != mv:
                    k[1] = k[0]
                    k[0] = mv
            break
    if best == -MT:
        if att(p, p.wk if p.turn == 1 else p.bk, -p.turn):
            return -MT + ply
        return 0
    flag = 0
    if best <= orig_alpha:
        flag = 2
    elif best >= beta:
        flag = 1
    TT[p.hash] = (depth, flag, best, bv)
    return best
def bm(p, legal_uci):
    global ND, TT, KL
    ND = 0
    TT = {}
    KL = [[None, None] for _ in range(256)]
    root = []
    for u in legal_uci:
        frm = (ord(u[0]) - 97) + (int(u[1]) - 1) * 16
        to = (ord(u[2]) - 97) + (int(u[3]) - 1) * 16
        promo = 0
        if len(u) == 5:
            promo = "nbrq".index(u[4]) + 2
        root.append(((frm, to, promo), u))
    bu = root[0][1]
    depth = 1
    try:
        while True:
            alpha = -MT
            beta = MT
            cb = None
            cs = -MT
            for mv, u in root:
                un = dom(p, mv)
                if att(p, p.wk if -p.turn == 1 else p.bk, p.turn):
                    und(p, mv, un)
                    continue
                s = -srch(p, depth - 1, -beta, -alpha, 1)
                und(p, mv, un)
                if s > cs:
                    cs = s
                    cb = u
                if s > alpha:
                    alpha = s
            if cb is not None:
                bu = cb
            root.sort(key=lambda x: 0 if x[1] == bu else 1)
            depth += 1
            if depth > 40:
                break
    except SS:
        pass
    return bu
def main():
    while True:
        g = post("/game", {})
        if g["status"] == "done":
            break
        while g["status"] == "your_move":
            p = fen(g["fen"])
            mv = bm(p, g["legal_moves"])
            g = post("/move", {"game": g["game"], "move": mv})
        print(f"game {g['game']}: {g['outcome']} by {g['reason']}", file=sys.stderr)
    print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost", file=sys.stderr)
if __name__ == "__main__":
    main()
