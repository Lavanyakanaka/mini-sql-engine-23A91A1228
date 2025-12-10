# engine.py
import csv

class MiniSQLEngine:
    def __init__(self):
        # self.tables stores lists of rows (each row is dict column->value)
        self.tables = {}

    # LOAD CSV — returns an object with .rows so repl.print(len(tbl.rows)) works
    def load_csv(self, filename, table_name):
        try:
            with open(filename, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file '{filename}' not found.")

        # coerce empty strings to None? keep as-is for now
        self.tables[table_name] = rows
        # return a simple object carrying reference to rows
        return type("LoadedTable", (), {"rows": rows})

    # INSERT: append a new row (columns: list[str], values: list[coerced values])
    def insert(self, table_name, columns, values):
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' not loaded.")
        if len(columns) != len(values):
            raise ValueError("Column count and value count do not match.")

        # build row dict using existing columns as keys. If table has no rows yet,
        # we will allow inserting and future SELECT * uses inserted keys.
        new_row = {}
        for c, v in zip(columns, values):
            new_row[c] = v

        # If table already has rows with other columns, ensure missing columns present as None
        existing = self.tables[table_name]
        if existing:
            existing_cols = set(existing[0].keys())
            for col in existing_cols:
                if col not in new_row:
                    new_row[col] = None
            # also ensure new keys appear in existing rows with None
            new_keys = set(new_row.keys()) - existing_cols
            for row in existing:
                for nk in new_keys:
                    row.setdefault(nk, None)

        self.tables[table_name].append(new_row)
        return {"status": "OK", "inserted": 1}

    # SELECT: select_dict follows parser's structure; where is same as parser
    def select(self, table_name, select_dict, where):
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' not loaded.")
        rows = self.tables[table_name]

        # WHERE filter
        if where:
            col = where["col"]
            op = where["op"]
            val = where["val"]
            if not rows:
                filtered = []
            else:
                if col not in rows[0]:
                    raise ValueError(f"Unknown column in WHERE: {col}")

                def cmp(x, op, y):
                    # attempt numeric conversion if y is number
                    try:
                        if isinstance(y, (int, float)):
                            x = float(x)
                    except:
                        pass
                    if op == "=": return x == y
                    if op == "!=": return x != y
                    if op == ">": return x > y
                    if op == "<": return x < y
                    if op == ">=": return x >= y
                    if op == "<=": return x <= y
                    raise ValueError("Invalid operator")
                filtered = [r for r in rows if cmp(r.get(col), op, val)]
            rows = filtered

        # COUNT aggregation
        if "agg" in select_dict and select_dict["agg"] == "COUNT":
            target = select_dict["target"]
            if target == "*":
                return (["count"], [[len(rows)]])
            else:
                if not rows or target not in rows[0]:
                    raise ValueError(f"Unknown column in COUNT(): {target}")
                cnt = sum(1 for r in rows if r.get(target) not in (None, "", "NULL"))
                return (["count"], [[cnt]])

        # SELECT *
        if select_dict.get("type") == "all":
            if not rows:
                return ([], [])
            headers = list(rows[0].keys())
            data = [[r.get(h) for h in headers] for r in rows]
            return (headers, data)

        # SELECT specific columns
        if select_dict.get("type") == "cols":
            cols = select_dict["cols"]
            # verify columns exist (if table empty, allow insert-only columns)
            if rows:
                for c in cols:
                    if c not in rows[0]:
                        raise ValueError(f"Unknown column in SELECT: {c}")
            headers = cols
            data = [[r.get(c) for c in cols] for r in rows]
            return (headers, data)

        raise ValueError("Unsupported SELECT specification")
