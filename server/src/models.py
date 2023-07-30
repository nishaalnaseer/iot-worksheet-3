# application models
from pydantic import BaseModel
from enum import Enum

class Report(BaseModel):
    """A data class containing data of the current moment"""
    time: int
    accel_x: int
    accel_y: int
    accel_z: int
    temp: int
    light_level: int
    touch_pin0: bool
    touch_pin1: bool
    touch_pin2: bool


class ReportType(str, Enum):
    PINS = "PINS",
    TEMPS = "TEMPS",
    LIGHT = "LIGHT"
