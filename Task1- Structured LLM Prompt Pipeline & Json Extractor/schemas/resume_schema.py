"""
Pydantic v2 schemas for Resume / CV Extraction.
Provides comprehensive validation for candidate profiles, career histories,
education, technical competencies, and project portfolios.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class ContactInfo(BaseModel):
    full_name: str = Field(..., description="Full legal or professional name of the candidate")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number with country code if provided")
    location: Optional[str] = Field(None, description="City, State / Region, Country")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    github_url: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio_url: Optional[str] = Field(None, description="Personal website or portfolio URL")


class EducationEntry(BaseModel):
    institution: str = Field(..., description="University, College, or School name")
    degree: str = Field(..., description="Degree type (e.g., Bachelor of Science, Master, High School Diploma)")
    field_of_study: Optional[str] = Field(None, description="Major, specialization, or concentration (e.g., Computer Science)")
    start_year: Optional[str] = Field(None, description="Start year or date")
    graduation_year: Optional[str] = Field(None, description="Graduation year or expected graduation date")
    gpa: Optional[str] = Field(None, description="GPA or grade score if mentioned")
    honors: List[str] = Field(default_factory=list, description="Academic honors, Dean's list, or awards")


class WorkExperienceEntry(BaseModel):
    company: str = Field(..., description="Name of the employing organization")
    role_title: str = Field(..., description="Job title or designation")
    location: Optional[str] = Field(None, description="Office location or Remote status")
    start_date: Optional[str] = Field(None, description="Employment start date (e.g. 'Jan 2021', '2021-01')")
    end_date: Optional[str] = Field(None, description="Employment end date or 'Present' / 'Current'")
    is_current: bool = Field(default=False, description="Whether this is the current active role")
    responsibilities: List[str] = Field(default_factory=list, description="Key duties and day-to-day responsibilities")
    key_achievements: List[str] = Field(default_factory=list, description="Quantified achievements, impact, or outcomes")
    technologies_used: List[str] = Field(default_factory=list, description="Tools, libraries, platforms, or languages used")

    @field_validator("is_current", mode="before")
    @classmethod
    def evaluate_current_status(cls, v, info):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower().strip() in ("true", "yes", "current", "present")
        return False


class ProjectEntry(BaseModel):
    title: str = Field(..., description="Project name or system title")
    description: str = Field(..., description="Overview and objective of the project")
    role: Optional[str] = Field(None, description="Role within the project (e.g. Lead Developer, Contributor)")
    technologies: List[str] = Field(default_factory=list, description="Technologies and frameworks used in the project")
    github_or_live_url: Optional[str] = Field(None, description="URL to repository or live demo")


class CertificationEntry(BaseModel):
    name: str = Field(..., description="Name of the certificate or credential")
    issuing_organization: str = Field(..., description="Issuing body (e.g. AWS, Google Cloud, Coursera, Scrum Alliance)")
    issue_date: Optional[str] = Field(None, description="Date credential was obtained")
    credential_id_or_url: Optional[str] = Field(None, description="Credential ID or verification URL")


class SkillGroup(BaseModel):
    category: str = Field(..., description="Skill category, e.g., 'Programming Languages', 'Frameworks & Libraries', 'Cloud & DevOps', 'Databases'")
    skills: List[str] = Field(default_factory=list, description="List of skills belonging to this category")


class ResumeData(BaseModel):
    candidate: ContactInfo = Field(..., description="Candidate contact and identification details")
    professional_summary: Optional[str] = Field(None, description="Brief professional profile or summary statement")
    total_years_experience: Optional[float] = Field(None, description="Estimated total years of professional experience", ge=0)
    work_experience: List[WorkExperienceEntry] = Field(default_factory=list, description="Chronological work history")
    education: List[EducationEntry] = Field(default_factory=list, description="Formal educational qualifications")
    skills: List[SkillGroup] = Field(default_factory=list, description="Categorized technical and domain skill groups")
    projects: List[ProjectEntry] = Field(default_factory=list, description="Significant projects, open source, or portfolio works")
    certifications: List[CertificationEntry] = Field(default_factory=list, description="Professional certifications and licenses")
    languages: List[str] = Field(default_factory=list, description="Human/natural languages spoken (e.g., English, Spanish, Bengali)")

    @field_validator("total_years_experience", mode="before")
    @classmethod
    def parse_years(cls, v):
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            # Try to extract numbers from strings like "5+ years", "3.5 yrs"
            import re
            m = re.search(r"(\d+(\.\d+)?)", v)
            if m:
                return float(m.group(1))
        return None
