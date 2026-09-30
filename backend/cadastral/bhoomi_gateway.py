"""Farmer-guided access to Karnataka Bhoomi RTC records.

This is a safe gateway to the official manual lookup workflow, not an API
client. It neither scrapes the portal nor infers ownership or parcel geometry.
"""

from __future__ import annotations

from typing import Iterable


RTC_URL = "https://landrecords.karnataka.gov.in/service2/RTC.aspx"
DISTRICT_PAGE = "https://chitradurga.nic.in/en/tehsil/"
CENSUS_SOURCE = "https://censusindia.gov.in/nada/index.php/catalog/602/download/2056/DH_2011_2912_PART_A_DCHB_CHITRADURGA.pdf"

_DIGITS = set("0123456789")


def _identifier(value: object, label: str) -> str:
    text = str(value if value is not None else "").strip()
    if not text or len(text) > 32 or not all(ch in _DIGITS | {"/", "-", ".", "A", "B", "a", "b"} for ch in text):
        raise ValueError(f"{label} must be a short survey identifier")
    return text


def get_bhoomi_rtc_context(
    survey_number: str = "3",
    hissa_numbers: Iterable[str] = ("2", "4"),
) -> dict:
    """Build a transparent manual-lookup payload for a farmer-confirmed parcel.

    Survey and hissa values are passed through as farmer assertions. They are
    not checked against RTC records and do not prove ownership or boundaries.
    """
    survey = _identifier(survey_number, "Survey number")
    hissas = []
    for value in hissa_numbers:
        hissa = _identifier(value, "Hissa number")
        if hissa not in hissas:
            hissas.append(hissa)
    if not hissas:
        raise ValueError("At least one hissa number is required")

    return {
        "status": "manual_verification_required",
        "portal": {
            "name": "Karnataka Bhoomi RTC/Pahani",
            "url": RTC_URL,
            "direct_record_link": False,
            "note": "Open the portal and make the selections there. This link does not prefill or verify a private RTC record.",
        },
        "location": {
            "state": "Karnataka",
            "district": {"name": "Chitradurga", "code": None, "code_status": "not_verified"},
            "taluk": {"name": "Molakalmuru", "code": None, "code_status": "not_verified"},
            "hobli": {"name": None, "code": None, "status": "not_verified_from_an_authoritative_public_source"},
            "village": {
                "name": "Hosanagalapura",
                "census_2011_code": "605160",
                "census_code_scope": "2011 statistical village identifier; not a Bhoomi revenue-selection code",
            },
        },
        "farmer_asserted_identifiers": {
            "survey_number": survey,
            "hissa_numbers": hissas,
            "verification_status": "not_verified_against_rtc",
        },
        "lookup_steps": [
            "Open Karnataka Bhoomi RTC/Pahani.",
            "Select the revenue district, taluk, hobli, and village shown by Bhoomi; confirm the displayed place names with the Tahsildar office if they differ from this pilot label.",
            f"Look up Survey No. {survey} in the portal.",
            "Check each requested hissa separately and compare the official RTC/Pahani entry with the farmer's records.",
        ],
        "limitations": [
            "The portal requires interactive user verification; this service does not bypass CAPTCHA, login, or other access controls.",
            "No owner name, extent, tenure, parcel polygon, or boundary is fetched or inferred.",
            "The survey and hissa values above are farmer-provided assertions until checked in an official RTC/Pahani record.",
            "The Census village code identifies a locality in the 2011 census and must not be used as a revenue selection code.",
        ],
        "sources": [
            {
                "label": "Karnataka Bhoomi RTC/Pahani portal",
                "url": RTC_URL,
                "scope": "Official user-facing lookup portal; direct prefilled private record access is not provided here.",
            },
            {
                "label": "Government of Karnataka: Chitradurga district tehsils",
                "url": DISTRICT_PAGE,
                "scope": "Confirms Molakalmuru as a Chitradurga taluk; does not publish Bhoomi selection codes or the village hobli mapping.",
            },
            {
                "label": "Census of India 2011: Chitradurga District Census Handbook",
                "url": CENSUS_SOURCE,
                "scope": "Lists Hosanagalapura with census location code 605160; this is not a cadastral identifier.",
            },
        ],
    }


__all__ = ["get_bhoomi_rtc_context", "RTC_URL"]
