def rels(k):
    r = dict()
    for i in range(len(k)-1):
        if k[i+1] > k[i]-1:
            r[i + k[i]-1] = i
    return r

def P(i, k):
    return (i, i + k[i]-1)

def I(i, k, e):
    if i==0:
        return (0,0)
    j = i-1
    while(j > 0):
        if j in e:
            return (e[j]+1,i)
        j -= 1
    return (0, i)

def cok(x, y):
    if x[0] <= y[0]:
        return None
    return (y[0], x[0]-1)

def ker(x, y):
    if x[1] <= y[1]:
        return None
    return (y[1]+1, x[1])

def inj_res(x, inj):
    L = []
    c = x
    while(c != None):
        L.append(c[1])
        c = cok(c, inj[c[1]])
    return L

def projdim_of_inj(inj, proj):
    dims = [0]*len(inj)
    for i in range(len(inj)):
        d = -1
        c = inj[i]
        while(c != None):
            d += 1
            c = ker(proj[c[0]], c)
        dims[i]=d
    return dims

def isAG(proj, pd, inj):
    for p in proj:
        injres = inj_res(p, inj)
        if not all(pd[d] <= i for d,i in zip(injres, range(len(injres)))):
            return False
    return True

def latex(n, rels):
    lines = []
    lines.append(r'\begin{center}' + '\n')
    lines.append(r'  \begin{tikzcd}' + '\n')
    s = '    '
    for i in range(n-1):
        s += str(i) + ' ' + r'\arrow{r}[name=a' + str(i) + r']{} & '
    s += str(n-1)
    lines.append(s + '\n')

    for rel in rels:
        lines.append('    ' + r'\arrow[from=a' + str(rel[1]) + r', to=a' + str(rel[0]) + r', bend left=80, no head, dashed]{r}{}' + '\n')

    lines.append(r'  \end{tikzcd}' + '\n')
    lines.append(r'\end{center}' + '\n')
    lines.append('\n')
    
    return lines

def kupisch_series(n, I=1):
    if n>1:
        for i in range(2, I+2):
            for p in kupisch_series(n-1, i):
                yield p + [I]
    else:
        yield [I]


def search_algebras(N):
    lines = []
    for n in range(2, N+1):
        for k in kupisch_series(n):
            #k = kupisch(inc)
            relations = rels(k)
            inj = [I(i,k,relations) for i in range(len(k))]
            proj = [P(i,k) for i in range(len(k))]

            pd = projdim_of_inj(inj, proj)

            s = set(relations.values())
            e = set(relations.keys())
            s = s.union(e)

            has_enough_relations = s == set(range(n-1))

            if has_enough_relations and not isAG(proj, pd, inj):
                lines += latex(len(k), list(relations.items()))
                print(k)
        print(n, '/', N)
    return lines
with open("diagram.tex", mode="wt") as f:
    f.writelines(search_algebras(8))
print('sucess')