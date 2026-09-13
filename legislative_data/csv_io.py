import csv
from dataclasses import asdict, fields
from pathlib import Path
from typing import Callable, TypeVar

from models import (
    Bill,
    BillSummary,
    LegislativeData,
    Legislator,
    LegislatorSummary,
    Reports,
    Vote,
    VoteResult,
    VoteType,
)

Record = TypeVar("Record", Legislator, Bill, Vote, VoteResult)


class CsvRepository:
    def __init__(self, directory: Path) -> None:
        self.directory = directory

    def load(self) -> LegislativeData:
        return LegislativeData(
            legislators=self._read("legislators.csv", Legislator, {"id": int}),
            bills=self._read("bills.csv", Bill, {"id": int, "sponsor_id": int}),
            votes=self._read("votes.csv", Vote, {"id": int, "bill_id": int}),
            vote_results=self._read(
                "vote_results.csv",
                VoteResult,
                {
                    "id": int,
                    "legislator_id": int,
                    "vote_id": int,
                    "vote_type": lambda value: VoteType(int(value)),
                },
            ),
        )

    def _read(
        self,
        filename: str,
        model: type[Record],
        converters: dict[str, Callable[[str], object]],
    ) -> list[Record]:
        path = self.directory / filename
        required = [field.name for field in fields(model)]
        records = []
        with path.open(newline="", encoding="utf-8-sig") as source:
            reader = csv.DictReader(source, strict=True)
            missing = set(required) - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
            for row in reader:
                try:
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError("row does not match the header")
                    values = {}
                    for name in required:
                        value = row[name].strip()
                        if not value:
                            raise ValueError(f"empty {name}")
                        values[name] = converters.get(name, str)(value)
                    records.append(model(**values))
                except ValueError as error:
                    raise ValueError(f"{path}:{reader.line_num}: {error}") from error
        return records


class CsvReportWriter:
    def __init__(self, directory: Path) -> None:
        self.directory = directory

    def write(self, reports: Reports) -> tuple[Path, Path]:
        self.directory.mkdir(parents=True, exist_ok=True)
        legislator_path = self.directory / "legislators-support-oppose-count.csv"
        bill_path = self.directory / "bills.csv"
        self._write(legislator_path, LegislatorSummary, reports.legislators)
        self._write(bill_path, BillSummary, reports.bills)
        return legislator_path, bill_path

    @staticmethod
    def _write(
        path: Path,
        model: type[LegislatorSummary] | type[BillSummary],
        rows: list[LegislatorSummary] | list[BillSummary],
    ) -> None:
        with path.open("w", newline="", encoding="utf-8") as destination:
            writer = csv.DictWriter(
                destination, fieldnames=[field.name for field in fields(model)]
            )
            writer.writeheader()
            writer.writerows(asdict(row) for row in rows)
