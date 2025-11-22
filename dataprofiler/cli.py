import argparse
import pandas as pd
from .ingestion import load_data
from .profiling import profile_data
from .reports import build_report, export_html, export_json


def main():
    p = argparse.ArgumentParser(prog="dataprofiler")
    p.add_argument("path")
    p.add_argument("--out", dest="out", default=None)
    p.add_argument("--title", dest="title", default="Data Profile")
    p.add_argument("--json", dest="json_path", default=None)
    args = p.parse_args()
    ing = load_data(args.path)
    df = pd.DataFrame(ing.rows)
    prof = profile_data(df)
    html = build_report(prof, output_dir=args.out, title=args.title)
    if args.out:
        export_html(html, args.out + "/report.html")
    if args.json_path:
        export_json(prof, args.json_path)


if __name__ == "__main__":
    main()