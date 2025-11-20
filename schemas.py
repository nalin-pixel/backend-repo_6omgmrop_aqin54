"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Lead schema for VD Pulizie lead generation
class Lead(BaseModel):
    """
    Leads collected from the website
    Collection name: "lead"
    """
    name: str = Field(..., description="Nome completo del cliente")
    email: EmailStr = Field(..., description="Email del cliente")
    phone: str = Field(..., description="Telefono del cliente")
    service_type: Literal[
        "Pulizie domestiche",
        "Uffici",
        "Condomini",
        "Post-cantiere",
        "Vetrate",
        "Altro"
    ] = Field(..., description="Tipo di servizio richiesto")
    square_meters: Optional[int] = Field(None, ge=0, description="Metri quadri indicativi")
    frequency: Optional[Literal["Una tantum", "Settimanale", "Quindicinale", "Mensile"]] = Field(
        None, description="Frequenza del servizio"
    )
    message: Optional[str] = Field(None, description="Messaggio aggiuntivo")
    source: str = Field("website", description="Sorgente del contatto")
    status: Literal["nuovo", "contattato", "preventivo", "chiuso"] = Field(
        "nuovo", description="Stato del lead"
    )

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
