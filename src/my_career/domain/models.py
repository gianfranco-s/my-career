"""Models used to load the full resume"""

from dataclasses import dataclass
from typing import Protocol



@dataclass
class Location:
    countryCode: str
    region: str | None = None
    city: str | None = None


@dataclass
class SocialMediaProfile:
    network: str
    url: str
    username: str | None = None


@dataclass
class ResumeBasics:
    name: str
    label: str
    image: str
    email: str
    phone: str
    url: str
    summary: str
    location: Location
    profiles: list[SocialMediaProfile]


@dataclass
class WorkExperience:
    name: str
    position: str
    startDate: str
    summary: str
    isRemote: bool
    location: Location
    highlights: list[str]
    techHighlights: list[str]
    url: str | None = None
    endDate: str | None = None


@dataclass    
class Education:
    institution: str
    area: str
    startDate: str
    url: str | None = None
    studyType: str | None = None
    endDate: str | None = None


@dataclass    
class Certificate:
    name: str
    date: str
    issuer: str
    url: str


@dataclass    
class Language:
    language: str
    fluency: str


@dataclass    
class PersonalInterest:
    name: str
    summary: str
    keywords: str | None = None


@dataclass    
class Project:
    name: str
    startDate: str
    description: str
    highlights: list[str]
    endDate: str | None = None
    url: str | None = None


@dataclass    
class Skill:
    name: str
    keywords: list[str]
    level: str | None = None


@dataclass
class FullResume:
    basics: ResumeBasics
    work: list[WorkExperience]
    education: list[Education]
    certificates: list[Certificate]
    languages: list[Language]
    interests: list[PersonalInterest]
    skills: list[Skill]
    projects: list[Project] | None = None
    # publications: list[Publication] | None = None  # Not implemented
    # references: list[Reference] | None = None  # Not implemented
    # awards: list[Award] | None = None  # Not implemented
    # volunteer: list[Volunteer] | None = None  # Not implemented


class BaseResumeSection(Protocol):
    """
    These are the classes included in FullResume
    such as WorkExperience or Project
    """
    pass