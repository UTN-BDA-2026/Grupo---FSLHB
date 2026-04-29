import os
import sys

from sqlalchemy import MetaData, create_engine, func, select


def main() -> int:
    src_url = os.environ.get("SOURCE_DATABASE_URL")
    tgt_url = os.environ.get("TARGET_DATABASE_URL")

    if not src_url or not tgt_url:
        print(
            "Both SOURCE_DATABASE_URL and TARGET_DATABASE_URL env vars are required.",
            file=sys.stderr,
        )
        return 1

    src_engine = create_engine(src_url)
    tgt_engine = create_engine(tgt_url)

    src_meta = MetaData()
    tgt_meta = MetaData()

    print("Reflecting source (Postgres)...")
    src_meta.reflect(bind=src_engine)

    print("Reflecting target (MariaDB)...")
    tgt_meta.reflect(bind=tgt_engine)

    src_tables = {t.name.lower(): t for t in src_meta.tables.values()}
    tgt_tables = {t.name.lower(): t for t in tgt_meta.tables.values()}

    common = sorted(set(src_tables) & set(tgt_tables))

    mismatches: list[tuple[str, int, int]] = []

    with src_engine.connect() as src_conn, tgt_engine.connect() as tgt_conn:
        for key in common:
            name = src_tables[key].name
            if key == "alembic_version":
                continue

            src_table = src_tables[key]
            tgt_table = tgt_tables[key]

            src_count = src_conn.execute(select(func.count()).select_from(src_table)).scalar_one()
            tgt_count = tgt_conn.execute(select(func.count()).select_from(tgt_table)).scalar_one()

            if src_count != tgt_count:
                mismatches.append((name, int(src_count), int(tgt_count)))

    if mismatches:
        print("\nMISMATCHES:")
        for name, src_count, tgt_count in mismatches:
            print(f"- {name}: postgres={src_count} mariadb={tgt_count}")
        return 2

    print("\nOK: All common tables match row counts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
