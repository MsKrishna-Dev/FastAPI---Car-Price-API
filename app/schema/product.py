from pydantic import BaseModel, Field, AnyUrl, field_validator, model_validator, computed_field, EmailStr
from typing import Annotated, Literal, Optional, List
from uuid import UUID
from datetime import datetime

#CREATE PYDENTIC

class Dimension(BaseModel):
    length: Annotated[float, Field(gt=0, strict=True, description="Length in cm")]
    width:Annotated[float, Field(gt=0, strict=True, description="Width in cm")]
    height:Annotated[float, Field(gt=0, strict=True, description="Height in cm")]

class Seller(BaseModel):
    id : UUID
    name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=60,
            title="Seller Name",
            description="Mane of Seller (2-60 chars).",
            examples=["MI Store", "Apple Store"],
        ),
    ]
    email : EmailStr
    website: AnyUrl

    @field_validator("email", mode="after")
    @classmethod
    def validate_seller_email_domain(cls, value: EmailStr):
        allowed_domains = {
            "mistore.in",
            "realmeofficial.in",
            "samsungindia.in",
            "lenovostore.in",
            "hpworld.in",
            "applestoreindia.in",
            "dellexclusive.in",
            "sonycenter.in",
            "oneplusstore.in",
            "asusexclusive.in",
        }        
        domain = str(value).split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError(f"Seller email domain not allowed: {domain}")

        return value

class Product(BaseModel):
    id : UUID
    sku: Annotated[
        str,
        Field(
            min_length=6,
            max_length=30,
            title="SKU",
            description="Stock Keeping Unit",
            examples=["XIAO-359GB-001"],
        ),
    ]
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=80,
            title="Product Name",
            description="Readable product name (3-80 chars).",
            examples=["Xiaomi Model Pro", "Apple Model X"],
        ),
    ]

    description: Annotated[
        str,
        Field(max_length=200, description="Short product description"),
    ]

    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="Category like mobiles/laptops/electronics/accessories",
            examples=["mobiles", "laptops"],
        ),
    ]

    brand: Annotated[
        str,
        Field(min_length=2, max_length=40, examples=["Xiaomi", "Apple"]),
    ]

    price: Annotated[float, Field(gt=0, strict=True, description="Base price (INR)")]
    currency: Literal["INR"] = "INR"

    discount_percent: Annotated[
        int,
        Field(ge=0, le=90, description="Discount in percent (0-90)"),
    ] = 0

    stock: Annotated[int, Field(ge=0, description="Available stock (>=0)")]
    is_active: Annotated[bool, Field(description="Is product active?")]

    rating: Annotated[
        float,
        Field(ge=0, le=5, strict=True, description="Rating out of 5"),
    ]
    tags: Annotated[
        Optional[List[str]],
        Field(default=None, max_length=10, description="Up to 10 tags"),
    ]
    image_urls: Annotated[
        List[AnyUrl],
        Field(..., description="At least 1 image url"),
    ]

    dimensions: Dimension
    seller: Seller

    created_at: datetime

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, value: str):
        if "-" not in value:
            raise ValueError('SKU must have "-" ')  # it will validates the entered sku must be in format. Used field_validator for this which only accept one field
        
        last = value.split("-")[-1]   #it will store last 3 digits and whether use to valid the sku must has last 3 digits only not any str or other.
        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must end with 3-digit sequence like -234") 
        
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_rules(cls, model:"Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("If stock is 0, is_active must be false")
        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discounted product must have ratings (rating =! 0)")
        return model
    
    @computed_field    
    #Basically it's like a decorator. It adds new field.
    @property
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount_percent / 100) , 2)
    
    @computed_field
    @property
    def volume(self) -> float:
        d = self.dimensions
        return round(d.length * d.width * d.height, 2)


#UPADTE PYDENTIC

class DimensionsCMUpdate(BaseModel):
    length: Optional[float] = Field(gt=0)
    width: Optional[float] = Field(gt=0)
    height: Optional[float] = Field(gt=0)


class SellerUpdate(BaseModel):
    name: Optional[str] = Field(min_length=2, max_length=60)
    email: Optional[EmailStr]
    website: Optional[AnyUrl]

    @field_validator("email", mode="after")
    @classmethod
    def validate_seller_email_domain(cls, value: EmailStr):
        allowed_domains = {
            "mistore.in",
            "realmeofficial.in",
            "samsungindia.in",
            "lenovostore.in",
            "hpworld.in",
            "applestoreindia.in",
            "dellexclusive.in",
            "sonycenter.in",
            "oneplusstore.in",
            "asusexclusive.in",
        }
        domain = str(value).split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError(f"Seller email domain not allowed: {domain}")
        return value


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=80)
    description: Optional[str] = Field(max_length=200)
    category: Optional[str]
    brand: Optional[str]

    price: Optional[float] = Field(gt=0)
    currency: Optional[Literal["INR"]]

    discount_percent: Optional[int] = Field(ge=0, le=90)
    stock: Optional[int] = Field(ge=0)
    is_active: Optional[bool]
    rating: Optional[float] = Field(ge=0, le=5)

    tags: Optional[List[str]] = Field(max_length=10)
    image_urls: Optional[List[AnyUrl]]

    dimensions_cm: Optional[DimensionsCMUpdate]
    seller: Optional[SellerUpdate]

    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls, model: "Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("If stock is 0, is_active must be false")

        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discounted product must have a rating (rating != 0)")

        return model

    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount_percent / 100), 2)

    @computed_field
    @property
    def volume_cm3(self) -> float:
        d = self.dimensions_cm
        return round(d.length * d.width * d.height, 2)

