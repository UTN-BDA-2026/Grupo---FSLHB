import os
import sys
import argparse
from sqlalchemy import MetaData, create_engine, select, text

parser = argparse.ArgumentParser(description="Migrate all tables and data from Postgres to MariaDB.")
parser.add_argument('--wipe-target', action='store_true', help='Truncate all target tables before migration (keeps schema)')
parser.add_argument('--batch-size', type=int, default=5000, help='Rows per batch when copying data')
args = parser.parse_args()

SRC_URL = os.environ.get('SOURCE_DATABASE_URL')
TGT_URL = os.environ.get('TARGET_DATABASE_URL')

if not SRC_URL or not TGT_URL:
    print("Both SOURCE_DATABASE_URL and TARGET_DATABASE_URL env vars are required.", file=sys.stderr)
    sys.exit(1)

src_engine = create_engine(SRC_URL)
tgt_engine = create_engine(TGT_URL)

src_meta = MetaData()
tgt_meta = MetaData()

print("Reflecting source schema (Postgres)...")
src_meta.reflect(bind=src_engine)

print("Reflecting target schema (MariaDB)...")
tgt_meta.reflect(bind=tgt_engine)

target_by_lower = {t.name.lower(): t for t in tgt_meta.tables.values()}

if args.wipe_target:
    print("Truncating all tables in target (MariaDB)...")
    with tgt_engine.begin() as conn:
        try:
            conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        except Exception:
            pass

        # Truncate in reverse dependency order
        for t in reversed(tgt_meta.sorted_tables):
            if t.name.lower() == "alembic_version":
                continue
            try:
                conn.execute(text(f"TRUNCATE TABLE `{t.name}`"))
            except Exception:
                # fallback if TRUNCATE is blocked
                conn.execute(t.delete())

        try:
            conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        except Exception:
            pass

print(f"Migrating {len(src_meta.tables)} tables...")


# Solo copiar datos, NO crear tablas
with tgt_engine.begin() as tgt_conn:
    try:
        tgt_conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    except Exception:
        pass

    for src_table in src_meta.sorted_tables:
        table_name = src_table.name
        if table_name.lower() == "alembic_version":
            print("Skipping table: alembic_version")
            continue

        tgt_table = tgt_meta.tables.get(table_name)
        if tgt_table is None:
            tgt_table = target_by_lower.get(table_name.lower())
        if tgt_table is None:
            print(f"Migrating table: {table_name}")
            print("  [SKIP] Target table not found in MariaDB (create schema first).")
            continue

        print(f"Migrating table: {table_name}")

        # Copy only columns that exist in the target
        tgt_col_names = {c.name for c in tgt_table.columns}
        src_col_names = [c.name for c in src_table.columns if c.name in tgt_col_names]

        inserted_total = 0
        try:
            with src_engine.connect() as src_conn:
                result = src_conn.execution_options(stream_results=True).execute(select(src_table))
                while True:
                    chunk = result.mappings().fetchmany(args.batch_size)
                    if not chunk:
                        break
                    rows = []
                    for r in chunk:
                        d = dict(r)
                        rows.append({k: d.get(k) for k in src_col_names})
                    if rows:
                        tgt_conn.execute(tgt_table.insert(), rows)
                        inserted_total += len(rows)
            print(f"  Inserted {inserted_total} rows.")
        except Exception as e:
            print(f"  [ERROR] Data copy failed for {table_name}: {e}")

    try:
        tgt_conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    except Exception:
        pass

print("Migration complete.")
