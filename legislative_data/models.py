from dataclasses import dataclass
from enum import IntEnum


class VoteType(IntEnum):
    YEA = 1
    NAY = 2


@dataclass(frozen=True)
class Legislator:
    id: int
    name: str


@dataclass(frozen=True)
class Bill:
    id: int
    title: str
    sponsor_id: int


@dataclass(frozen=True)
class Vote:
    id: int
    bill_id: int


@dataclass(frozen=True)
class VoteResult:
    id: int
    legislator_id: int
    vote_id: int
    vote_type: VoteType


@dataclass(frozen=True)
class LegislativeData:
    legislators: list[Legislator]
    bills: list[Bill]
    votes: list[Vote]
    vote_results: list[VoteResult]


@dataclass(frozen=True)
class LegislatorSummary:
    id: int
    name: str
    num_supported_bills: int
    num_opposed_bills: int


@dataclass(frozen=True)
class BillSummary:
    id: int
    title: str
    supporter_count: int
    opposer_count: int
    primary_sponsor: str


@dataclass(frozen=True)
class Reports:
    legislators: list[LegislatorSummary]
    bills: list[BillSummary]
