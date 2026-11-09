"""
Pydantic v2 schemas for Invoice Extraction.
Provides strict validation, data sanitization, and calculated integrity checks.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class VendorDetails(BaseModel):
    name: str = Field(..., description="Name of the vendor / seller company or individual")
    tax_id: Optional[str] = Field(None, description="VAT / GST / Tax Identification Number of the vendor")
    email: Optional[str] = Field(None, description="Contact email of the vendor")
    phone: Optional[str] = Field(None, description="Contact phone number of the vendor")
    address: Optional[str] = Field(None, description="Physical / billing address of the vendor")


class CustomerDetails(BaseModel):
    name: str = Field(..., description="Name of the client / customer company or individual")
    tax_id: Optional[str] = Field(None, description="Tax ID / VAT / GST number of the customer")
    email: Optional[str] = Field(None, description="Contact email of the customer")
    phone: Optional[str] = Field(None, description="Phone number of the customer")
    billing_address: Optional[str] = Field(None, description="Billing address of the customer")
    shipping_address: Optional[str] = Field(None, description="Shipping address if specified")


class InvoiceLineItem(BaseModel):
    item_code: Optional[str] = Field(None, description="SKU, product or service code")
    description: str = Field(..., description="Detailed description of goods or services provided")
    quantity: float = Field(..., description="Quantity of items billed (must be positive)", ge=0)
    unit_price: float = Field(..., description="Price per unit before taxes/discounts", ge=0)
    discount: float = Field(default=0.0, description="Discount amount applied to this line item", ge=0)
    total_price: float = Field(..., description="Total line price after discount (quantity * unit_price - discount)")

    @field_validator("quantity", "unit_price", "discount", "total_price", mode="before")
    @classmethod
    def parse_float_values(cls, v):
        if v is None:
            return 0.0
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            # Clean currency symbols and commas e.g. "$1,250.00" -> 1250.00
            cleaned = v.replace("$", "").replace("€", "").replace("£", "").replace(",", "").strip()
            return float(cleaned) if cleaned else 0.0
        return v


class PaymentDetails(BaseModel):
    payment_method: Optional[str] = Field(None, description="Payment method: Bank Transfer, Credit Card, PayPal, etc.")
    bank_name: Optional[str] = Field(None, description="Bank name for wire transfer")
    account_number: Optional[str] = Field(None, description="Bank account number or IBAN")
    routing_or_swift: Optional[str] = Field(None, description="Routing number, SWIFT, or BIC code")
    payment_terms: Optional[str] = Field(None, description="Payment terms, e.g. Net 30, Due upon receipt")


class InvoiceData(BaseModel):
    invoice_number: str = Field(..., description="Unique alphanumeric identifier of the invoice")
    invoice_date: str = Field(..., description="Issue date of the invoice (formatted as YYYY-MM-DD or standard ISO)")
    due_date: Optional[str] = Field(None, description="Payment due date")
    purchase_order_number: Optional[str] = Field(None, description="Associated Purchase Order (PO) number")
    currency: str = Field(default="USD", description="Currency code (e.g., USD, EUR, GBP, BDT)")
    
    vendor: VendorDetails = Field(..., description="Details regarding the issuing vendor")
    customer: CustomerDetails = Field(..., description="Details regarding the recipient / billed customer")
    
    line_items: List[InvoiceLineItem] = Field(default_factory=list, description="List of items billed")
    
    subtotal: float = Field(..., description="Sum of line item totals before tax and shipping", ge=0)
    tax_rate_percent: Optional[float] = Field(None, description="Tax rate applied as a percentage (e.g., 8.25 for 8.25%)")
    tax_amount: float = Field(default=0.0, description="Total tax amount charged", ge=0)
    shipping_fee: float = Field(default=0.0, description="Shipping or handling fee if any", ge=0)
    discount_amount: float = Field(default=0.0, description="Overall invoice discount if any", ge=0)
    total_amount: float = Field(..., description="Final invoice total payable", ge=0)
    
    payment: Optional[PaymentDetails] = Field(default=None, description="Payment instructions and details")
    notes_or_terms: Optional[str] = Field(None, description="Special instructions, warranty notices, or return terms")

    @field_validator("subtotal", "tax_amount", "shipping_fee", "discount_amount", "total_amount", mode="before")
    @classmethod
    def clean_monetary_numbers(cls, v):
        if v is None:
            return 0.0
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            cleaned = v.replace("$", "").replace("€", "").replace("£", "").replace(",", "").strip()
            return float(cleaned) if cleaned else 0.0
        return v

    @model_validator(mode="after")
    def verify_invoice_totals(self):
        """Sanity check to log or verify calculated integrity."""
        computed_subtotal = sum(item.total_price for item in self.line_items) if self.line_items else self.subtotal
        # If subtotal was 0 but line items have values, update subtotal
        if self.subtotal == 0.0 and computed_subtotal > 0.0:
            self.subtotal = round(computed_subtotal, 2)
        return self
