# parser.py
import re

SELECT_RE = re.compile(r"^SELECT\s+(.*)\s+FROM\s+([a-zA-Z_][\w]*)\s*(?:WHERE\s+(.*))?$", re.I)
LOAD_RE   = re.compile(r"^LOAD\s+([^\s]+)\s+AS\s+([a-zA-Z_]\w*)$", re.I)
COUNT_RE  = re.compile(r"^COUNT\s*\((\*|[a-zA-Z_][\w]*)\)$", re.I)
WHERE_RE  = re.compile(r"^([a-zA-Z_][\w]*)\s*(=|!=|<=|>=|<|>)\s*(.+)$")
INSERT_RE = re.compile(
    r"^INSERT\s+INTO\s+([a-zA-Z_][\w]*)\s*\(\s*([^)]+?)\s*\)\s*VALUES\s*\(\s*(.+)\s*\)$",
    re.I
)

def _strip_quotes(s: str):
    s = s.strip()
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        return s[1:-1]
    return s

def _parse_value_token(token: str):
    t = token.strip()
    # remove surrounding quotes if present
    if (t.startswith("'") and t.endswith("'")) or (t.startswith('"') and t.endswith('"')):
        return _strip_quotes(t)
    # try int then float
    try:
        return int(t)
    except ValueError:
        try:
            return float(t)
        except ValueError:
            return t

def _split_values_respecting_quotes(s: str):
    # split on commas but ignore commas inside quotes
    vals = []
    cur = ""
    in_q = False
    qchar = None
    i = 0
    while i < len(s):
        ch = s[i]
        if in_q:
            cur += ch
            if ch == qchar:
                in_q = False
                qchar = None
            i += 1
            continue
        if ch in ("'", '"'):
            in_q = True
            qchar = ch
            cur += ch
            i += 1
            continue
        if ch == ",":
            vals.append(cur.strip())
            cur = ""
            i += 1
            continue
        cur += ch
        i += 1
    if cur.strip() != "":
        vals.append(cur.strip())
    return [ _parse_value_token(v) for v in vals ]

def parse(sql: str):
    s = sql.strip().rstrip(';').strip()
    if not s:
        raise ValueError("Empty statement")

    # INSERT
    m = INSERT_RE.match(s)
    if m:
        table = m.group(1)
        cols_raw = m.group(2)
        vals_raw = m.group(3)
        cols = [c.strip() for c in cols_raw.split(',')]
        vals = _split_values_respecting_quotes(vals_raw)
        if len(cols) != len(vals):
            raise ValueError("INSERT column count doesn't match value count")
        return {"type": "insert", "table": table, "columns": cols, "values": vals}

    # LOAD
    m = LOAD_RE.match(s)
    if m:
        path = m.group(1).strip().strip('"')
        name = m.group(2)
        return {"type": "load", "path": path, "name": name}

    # SELECT
    m = SELECT_RE.match(s)
    if not m:
        raise ValueError("Unrecognized statement")
    select_part = m.group(1).strip()
    table = m.group(2)
    where_part = m.group(3)

    # COUNT()
    if COUNT_RE.match(select_part):
        cm = COUNT_RE.match(select_part)
        target = cm.group(1)
        select = {"agg": "COUNT", "target": target}
    else:
        # column list or *
        if select_part == "*":
            select = {"type": "all"}
        else:
            cols = [c.strip() for c in select_part.split(',')]
            select = {"type": "cols", "cols": cols}

    where = None
    if where_part:
        wm = WHERE_RE.match(where_part.strip())
        if not wm:
            raise ValueError("Invalid WHERE clause")
        col, op, rval = wm.group(1), wm.group(2), wm.group(3).strip()
        # strip quotes or convert numeric
        if (rval.startswith("'") and rval.endswith("'")) or (rval.startswith('"') and rval.endswith('"')):
            rval = rval[1:-1]
        else:
            try:
                rval = int(rval)
            except ValueError:
                try:
                    rval = float(rval)
                except ValueError:
                    pass
        where = {"col": col, "op": op, "val": rval}

    return {"type": "select", "table": table, "select": select, "where": where}
# parser.py
import re

SELECT_RE = re.compile(r"^SELECT\s+(.*)\s+FROM\s+([a-zA-Z_][\w]*)\s*(?:WHERE\s+(.*))?$", re.I)
LOAD_RE   = re.compile(r"^LOAD\s+([^\s]+)\s+AS\s+([a-zA-Z_]\w*)$", re.I)
COUNT_RE  = re.compile(r"^COUNT\s*\((\*|[a-zA-Z_][\w]*)\)$", re.I)
WHERE_RE  = re.compile(r"^([a-zA-Z_][\w]*)\s*(=|!=|<=|>=|<|>)\s*(.+)$")
INSERT_RE = re.compile(
    r"^INSERT\s+INTO\s+([a-zA-Z_][\w]*)\s*\(\s*([^)]+?)\s*\)\s*VALUES\s*\(\s*(.+)\s*\)$",
    re.I
)

def _strip_quotes(s: str):
    s = s.strip()
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        return s[1:-1]
    return s

def _parse_value_token(token: str):
    t = token.strip()
    # remove surrounding quotes if present
    if (t.startswith("'") and t.endswith("'")) or (t.startswith('"') and t.endswith('"')):
        return _strip_quotes(t)
    # try int then float
    try:
        return int(t)
    except ValueError:
        try:
            return float(t)
        except ValueError:
            return t

def _split_values_respecting_quotes(s: str):
    # split on commas but ignore commas inside quotes
    vals = []
    cur = ""
    in_q = False
    qchar = None
    i = 0
    while i < len(s):
        ch = s[i]
        if in_q:
            cur += ch
            if ch == qchar:
                in_q = False
                qchar = None
            i += 1
            continue
        if ch in ("'", '"'):
            in_q = True
            qchar = ch
            cur += ch
            i += 1
            continue
        if ch == ",":
            vals.append(cur.strip())
            cur = ""
            i += 1
            continue
        cur += ch
        i += 1
    if cur.strip() != "":
        vals.append(cur.strip())
    return [ _parse_value_token(v) for v in vals ]

def parse(sql: str):
    s = sql.strip().rstrip(';').strip()
    if not s:
        raise ValueError("Empty statement")

    # INSERT
    m = INSERT_RE.match(s)
    if m:
        table = m.group(1)
        cols_raw = m.group(2)
        vals_raw = m.group(3)
        cols = [c.strip() for c in cols_raw.split(',')]
        vals = _split_values_respecting_quotes(vals_raw)
        if len(cols) != len(vals):
            raise ValueError("INSERT column count doesn't match value count")
        return {"type": "insert", "table": table, "columns": cols, "values": vals}

    # LOAD
    m = LOAD_RE.match(s)
    if m:
        path = m.group(1).strip().strip('"')
        name = m.group(2)
        return {"type": "load", "path": path, "name": name}

    # SELECT
    m = SELECT_RE.match(s)
    if not m:
        raise ValueError("Unrecognized statement")
    select_part = m.group(1).strip()
    table = m.group(2)
    where_part = m.group(3)

    # COUNT()
    if COUNT_RE.match(select_part):
        cm = COUNT_RE.match(select_part)
        target = cm.group(1)
        select = {"agg": "COUNT", "target": target}
    else:
        # column list or *
        if select_part == "*":
            select = {"type": "all"}
        else:
            cols = [c.strip() for c in select_part.split(',')]
            select = {"type": "cols", "cols": cols}

    where = None
    if where_part:
        wm = WHERE_RE.match(where_part.strip())
        if not wm:
            raise ValueError("Invalid WHERE clause")
        col, op, rval = wm.group(1), wm.group(2), wm.group(3).strip()
        # strip quotes or convert numeric
        if (rval.startswith("'") and rval.endswith("'")) or (rval.startswith('"') and rval.endswith('"')):
            rval = rval[1:-1]
        else:
            try:
                rval = int(rval)
            except ValueError:
                try:
                    rval = float(rval)
                except ValueError:
                    pass
        where = {"col": col, "op": op, "val": rval}

    return {"type": "select", "table": table, "select": select, "where": where}
