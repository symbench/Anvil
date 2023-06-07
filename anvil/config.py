from pathlib import Path
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


class MinMaxParameter(BaseModel):
    min: float = Field(..., description="The minimum value for the parameter")

    max: float = Field(..., description="The maximum value for the parameter")


class OptimizerConfig(BaseModel):
    method: Literal["BayesOpt"] = Field(
        default="BayesOpt",
    )

    aquisition: Literal["LCB"] = Field(
        default="LCB",
    )


class AnvilConfig(BaseModel):
    """The configuration object from Anvil"""

    seed_cad: str = Field(..., description="The seed CAD file to use")

    cad_param: Dict[str, int] = Field(
        ..., description="The configurable parameters for the CAD file"
    )

    simulator: Literal["OpenFOAM"] = Field(
        default="OpenFOAM", description="The simulator to use for Anvil"
    )

    simulator_config: Dict[str, Any] = Field(
        ..., description="The simulator configuration for Anvil"
    )

    design_space: Dict[str, MinMaxParameter] = Field(
        ..., description="The design space for Anvil"
    )

    mode: Literal["data_generation", "optimization"] = Field(
        default="data_generation",
        description="The mode of operation for Anvil. Either data_generation or optimization",
    )

    sampling_method: Literal["random"] = Field(
        default="random",
        description="The sampling method to use for data generation",
    )

    budget: int = Field(
        default=8,
        description="The simulation budget for optimization or data generation",
    )

    optimizer: Optional[OptimizerConfig] = Field(
        default=None, description="The optimizer configuration for optimization"
    )

    @classmethod
    def from_file(cls, file_loc: str):
        file_loc = Path(file_loc).resolve()

        with open(file_loc, "r") as f:
            data = f.read()

        return cls.parse_raw(data)

    class Config:
        allow_population_by_field_name = True
        allow_extra = False
        allow_mutation = False
        arbitrary_types_allowed = True
