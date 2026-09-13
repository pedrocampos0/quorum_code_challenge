from dataclasses import dataclass
from typing import TypeVar

from models import (
    Bill,
    BillSummary,
    LegislativeData,
    Legislator,
    LegislatorSummary,
    Reports,
    Vote,
    VoteType,
)

Record = TypeVar("Record", Legislator, Bill, Vote)


@dataclass
class VoteCounts:
    supported: int = 0
    opposed: int = 0

    def add(self, vote_type: VoteType) -> None:
        if vote_type == VoteType.YEA:
            self.supported += 1
        elif vote_type == VoteType.NAY:
            self.opposed += 1
        else:
            raise ValueError(f"Unsupported vote type: {vote_type}")


class LegislativeAnalyzer:
    def __init__(self, data: LegislativeData) -> None:
        self.data = data

    def analyze(self) -> Reports:
        legislators = self._index(self.data.legislators)
        bills = self._index(self.data.bills)
        votes = self._index(self.data.votes)
        voted_bills: set[int] = set()
        for vote in votes.values():
            if vote.bill_id not in bills:
                raise ValueError(f"Vote {vote.id}: unknown bill {vote.bill_id}")
            if vote.bill_id in voted_bills:
                raise ValueError(f"Bill {vote.bill_id}: more than one vote")
            voted_bills.add(vote.bill_id)

        legislator_counts = {legislator_id: VoteCounts() for legislator_id in legislators}
        bill_counts = {bill_id: VoteCounts() for bill_id in bills}
        result_ids: set[int] = set()
        seen_casts: set[tuple[int, int]] = set()
        for result in self.data.vote_results:
            if result.id in result_ids:
                raise ValueError(f"Duplicate VoteResult ID: {result.id}")
            result_ids.add(result.id)
            if result.legislator_id not in legislators:
                raise ValueError(
                    f"Vote result {result.id}: unknown legislator {result.legislator_id}"
                )
            if result.vote_id not in votes:
                raise ValueError(f"Vote result {result.id}: unknown vote {result.vote_id}")
            cast = (result.legislator_id, result.vote_id)
            if cast in seen_casts:
                raise ValueError(f"Duplicate vote for legislator/vote {cast}")
            seen_casts.add(cast)
            bill_id = votes[result.vote_id].bill_id
            legislator_counts[result.legislator_id].add(result.vote_type)
            bill_counts[bill_id].add(result.vote_type)

        legislator_summaries = []
        for legislator in legislators.values():
            counts = legislator_counts[legislator.id]
            legislator_summaries.append(
                LegislatorSummary(
                    legislator.id,
                    legislator.name,
                    counts.supported,
                    counts.opposed,
                )
            )

        bill_summaries = []
        for bill in bills.values():
            counts = bill_counts[bill.id]
            sponsor = legislators.get(bill.sponsor_id)
            bill_summaries.append(
                BillSummary(
                    bill.id,
                    bill.title,
                    counts.supported,
                    counts.opposed,
                    sponsor.name if sponsor else "Unknown",
                )
            )

        return Reports(legislator_summaries, bill_summaries)

    @staticmethod
    def _index(records: list[Record]) -> dict[int, Record]:
        index = {}
        for record in records:
            if record.id in index:
                raise ValueError(f"Duplicate {type(record).__name__} ID: {record.id}")
            index[record.id] = record
        return index
