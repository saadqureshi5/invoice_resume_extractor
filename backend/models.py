from pydantic import BaseModel, Field
from typing import List, Optional

# --- Invoice Models ---

class LineItem(BaseModel):
    description: str = Field(description="Description of the item or service")
    quantity: float = Field(default=1.0, description="Quantity of the item")
    unit_price: float = Field(default=0.0, description="Price per single unit")
    total: float = Field(default=0.0, description="Total price for this line item")

class InvoiceSchema(BaseModel):
    vendor_name: str = Field(description="Name of the company or person issuing the invoice")
    invoice_number: Optional[str] = Field(default=None, description="Unique invoice identifier")
    date: Optional[str] = Field(default=None, description="Date the invoice was issued")
    due_date: Optional[str] = Field(default=None, description="Payment due date")
    line_items: List[LineItem] = Field(default_factory=list, description="List of items or services billed")
    subtotal: Optional[float] = Field(default=None, description="Total before taxes and discounts")
    tax: Optional[float] = Field(default=None, description="Tax amount applied")
    total_amount: float = Field(description="Final total amount to be paid")

# --- Resume Models ---

class ContactInfo(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")

class Experience(BaseModel):
    role: str = Field(description="Job title or role")
    company: str = Field(description="Name of the employer")
    start_date: Optional[str] = Field(default=None, description="Start date of employment")
    end_date: Optional[str] = Field(default=None, description="End date of employment. Can be 'Present'")
    description: List[str] = Field(default_factory=list, description="List of achievements and responsibilities")

class Education(BaseModel):
    degree: str = Field(description="Degree or qualification obtained")
    institution: str = Field(description="Name of the school or university")
    year: Optional[str] = Field(default=None, description="Year of graduation or attendance period")

class ResumeSchema(BaseModel):
    contact_info: ContactInfo = Field(description="Candidate's contact information")
    summary: Optional[str] = Field(default=None, description="Professional summary or objective")
    experience: List[Experience] = Field(default_factory=list, description="Work history")
    education: List[Education] = Field(default_factory=list, description="Educational background")
    skills: List[str] = Field(default_factory=list, description="List of skills")
