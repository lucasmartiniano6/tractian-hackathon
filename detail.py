from pydantic import BaseModel, Field

class TechnicalDetail(BaseModel):
    name: str = Field(..., description="Name of the machine")
    manufacturer: str = Field(..., description="Manufacturer of the machine")
    model: str = Field(..., description="Model of the machine")

    identification: str
    localization: str
    power: str
    voltage: str
    frequence: str
    rotation: str
    ip_rating: str = Field(..., description="IP Rating of the machine")
    operating_temperature : str = Field(..., description="Operating Ambient Temperature")

    current_state: str = Field(..., description="Description of the currente state of the machine based on the given images")
    additional_info: str = Field(..., description="Any additional information about the machine that might be useful.")