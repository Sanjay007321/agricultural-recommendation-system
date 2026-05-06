from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# ============== Auth Schemas ==============

class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    mobile: str = Field(..., min_length=10, max_length=15)
    aadhar_number: Optional[str] = Field(None, min_length=12, max_length=12)
    password: str = Field(..., min_length=6)
    state: str
    district: str
    village: Optional[str] = None
    land_size_acres: Optional[float] = None
    primary_crops: Optional[List[str]] = None
    
    @validator('mobile')
    def validate_mobile(cls, v):
        if not v.isdigit():
            raise ValueError('Mobile number must contain only digits')
        return v
    
    @validator('aadhar_number')
    def validate_aadhar(cls, v):
        if v and not v.isdigit():
            raise ValueError('Aadhar number must contain only digits')
        if v and len(v) != 12:
            raise ValueError('Aadhar number must be 12 digits')
        return v

class UserLogin(BaseModel):
    mobile: str
    password: str

class UserResponse(BaseModel):
    id: int
    farmer_id: str
    full_name: str
    mobile: str
    aadhar_number: Optional[str]
    state: str
    district: str
    village: Optional[str]
    land_size_acres: Optional[float]
    primary_crops: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    farmer_id: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    farmer_id: Optional[str] = None

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    village: Optional[str] = None
    land_size_acres: Optional[float] = None
    primary_crops: Optional[List[str]] = None

# ============== Analysis Schemas ==============

class AnalysisInput(BaseModel):
    land_area_acres: float = Field(..., gt=0)
    soil_type: str
    soil_ph: float = Field(..., ge=0, le=14)
    nitrogen: float = Field(..., ge=0)  # kg/ha
    phosphorus: float = Field(..., ge=0)  # kg/ha
    potassium: float = Field(..., ge=0)  # kg/ha
    state: str
    district: str
    season: str  # Kharif, Rabi, Zaid
    rainfall_mm: float = Field(..., ge=0)
    temperature_c: float
    humidity_percent: Optional[float] = Field(default=60, ge=0, le=100)
    budget_inr: float = Field(..., gt=0)
    crop_preference: Optional[str] = "auto"  # "auto" or specific crop name
    crop_variety: Optional[str] = None  # Specific variety name, if selected
    nearest_mandi: Optional[str] = None
    sowing_date: Optional[str] = None  # YYYY-MM-DD format

class CropRecommendation(BaseModel):
    recommended_crop: str
    recommended_variety: Optional[str] = None
    confidence: float
    suitable_lands: Optional[List[str]] = None
    alternatives: List[dict]
    reasoning: str
    variety_details: Optional[dict] = None

class YieldPrediction(BaseModel):
    expected_yield_per_acre: float
    total_yield_quintal: float
    confidence_range: List[float]

class PricePrediction(BaseModel):
    current_price_per_quintal: float
    predicted_price_at_harvest: float
    price_trend: str
    forecast_30_days: List[float]

class FertilizerItem(BaseModel):
    name: str
    quantity_kg_per_acre: float
    cost_inr: float
    timing: str

class FertilizerRecommendation(BaseModel):
    recommendations: List[FertilizerItem]
    total_cost: float

class PesticideItem(BaseModel):
    name: str
    dosage: str
    timing: str
    cost_inr: float

class DiseaseRisk(BaseModel):
    disease_risk_level: str
    likely_diseases: List[str]
    pesticides: List[PesticideItem]
    total_cost: float

class HarvestPrediction(BaseModel):
    sowing_date: str
    expected_harvest_start: str
    expected_harvest_end: str
    days_to_harvest: int
    harvest_tips: List[str]

class IrrigationScheduleItem(BaseModel):
    stage: str
    days_after_sowing: str
    depth_mm: float
    frequency: str
    notes: str

class IrrigationPlanning(BaseModel):
    irrigation_required_mm: float
    total_water_needed_mm: float
    rainfall_mm: float
    irrigation_method: str
    irrigation_schedule: List[IrrigationScheduleItem]
    water_management_tips: List[str]
    estimated_cost_per_acre: float
    efficiency_percentage: float

class YieldImprovementTips(BaseModel):
    tips: List[str]

class GovernmentScheme(BaseModel):
    name: str
    benefit: str
    eligibility: str
    apply_link: Optional[str] = None

class LogisticsCost(BaseModel):
    transport_to_mandi: float
    loading_unloading: float
    mandi_fees: float
    storage_if_needed: float
    total_logistics: float

class LogisticsRecommendation(BaseModel):
    transport_mode: str
    estimated_cost: float
    nearest_mandi: str
    storage_advice: List[str]
    transport_tips: List[str]

class CostBreakdown(BaseModel):
    seeds: float
    fertilizers: float
    pesticides: float
    labor: float
    irrigation: float
    logistics: float
    miscellaneous: float
    total_cost: float

class RevenueBreakdown(BaseModel):
    total_yield_quintal: float
    price_per_quintal: float
    gross_revenue: float

class ProfitAnalysis(BaseModel):
    revenue: RevenueBreakdown
    costs: CostBreakdown
    net_profit: float
    profit_per_acre: float
    roi_percentage: float
    comparison_with_alternatives: List[dict]

class FullAnalysisResponse(BaseModel):
    analysis_id: str
    farmer_id: str
    crop_recommendation: CropRecommendation
    yield_prediction: YieldPrediction
    price_prediction: PricePrediction
    fertilizer_recommendation: FertilizerRecommendation
    disease_risk: DiseaseRisk
    harvest_prediction: HarvestPrediction
    irrigation_planning: IrrigationPlanning
    yield_improvement_tips: List[str]
    government_schemes: List[GovernmentScheme]
    logistics_cost: LogisticsCost
    logistics_recommendation: LogisticsRecommendation  # New field
    profit_analysis: ProfitAnalysis
    created_at: str

class AnalysisHistoryItem(BaseModel):
    analysis_id: str
    crop: str
    profit: float
    created_at: str

# ============== Reference Data Schemas ==============

class CropInfo(BaseModel):
    name: str
    hindi_name: str
    season: List[str]
    duration_days: int
    soil_types: List[str]
    ph_range: List[float]
    temperature_range: List[float]
    rainfall_mm: List[float]
    avg_yield_quintal_per_acre: float
    
class StateInfo(BaseModel):
    name: str
    code: str
    districts: List[str]
