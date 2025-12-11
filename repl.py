# repl.py
from parser import parse
from engine import MiniSQLEngine

def pretty_print(headers, rows):
    if not rows:
        print("No results")
        return
    widths = [max(len(str(h)), *(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    fmt = " | ".join("{:%d}" % w for w in widths)
    print(fmt.format(*headers))
    print("-" * (sum(widths) + 3 * (len(headers) - 1)))
    for r in rows:
        print(fmt.format(*[str(x) for x in r]))

def main():
    engine = MiniSQLEngine()
    print("Mini SQL Engine Ready. Type your SQL queries. Type EXIT to quit.\n")

    while True:
        query = input("SQL> ").strip()
        if query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not query:
            continue

        try:
            parsed = parse(query)

            if parsed["type"] == "load":
                tbl = engine.load_csv(parsed["path"], parsed["name"])
                print(f"Loaded '{parsed['name']}' ({len(tbl.rows)} rows)")
                continue

            if parsed["type"] == "insert":
                res = engine.insert(parsed["table"], parsed["columns"], parsed["values"])
                print(f"OK: inserted {res.get('inserted', 1)} row(s)")
                continue

            if parsed["type"] == "select":
                headers, rows = engine.select(parsed["table"], parsed["select"], parsed["where"])
                pretty_print(headers, rows)
                print(f"{len(rows)} row(s)\n")
                continue

        except Exception as e:
            print("ERROR:", e)

if __name__ == "__main__":
    main()
# repl.py
from parser import parse
from engine import MiniSQLEngine


def pretty_print(headers, rows):
    if not rows:
        print("No results")
        return

    # compute column widths
    widths = [
        max(len(str(h)), *(len(str(r[i])) for r in rows))
        for i, h in enumerate(headers)
    ]

    fmt = " | ".join("{:%d}" % w for w in widths)

    print(fmt.format(*headers))
    print("-" * (sum(widths) + 3 * (len(headers) - 1)))

    for r in rows:
        print(fmt.format(*[str(x) for x in r]))


def main():
    engine = MiniSQLEngine()
    print("Mini SQL Engine Ready. Type your SQL queries. Type EXIT to quit.\n")

    while True:
        query = input("SQL> ").strip()

        if query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not query:
            continue

        try:
            parsed = parse(query)

            # LOAD
            if parsed["type"] == "load":
                tbl = engine.load_csv(parsed["path"], parsed["name"])
                print(f"Loaded '{parsed['name']}' ({len(tbl.rows)} rows)")
                continue

            # SELECT
            if parsed["type"] == "select":
                headers, rows = engine.select(
                    parsed["table"],
                    parsed["select"],
                    parsed["where"]
                )
                pretty_print(headers, rows)
                print(f"{len(rows)} row(s)\n")
                continue

        except Exception as e:
            print("ERROR:", e)


if __name__ == "__main__":
    main()