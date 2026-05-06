from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json

from app.database import get_db
from app.models.schemas import (
    AnalysisInput, FullAnalysisResponse, AnalysisHistoryItem
)
from app.services.auth_service import get_current_user
from app.models.user import User
from app.models.history import AnalysisHistory
from app.services.crop_service import get_crop_recommendation
from app.services.price_service import predict_price
from app.services.yield_service import predict_yield
from app.services.fertilizer_service import get_fertilizer_recommendation
from app.services.disease_service import get_disease_risk
from app.services.scheme_service import get_eligible_schemes
from app.services.logistics_service import calculate_logistics_cost
from app.services.profit_service import calculate_profit
from app.services.climate_service import get_climate_dashboard_data
from app.services.irrigation_service import get_irrigation_planning

router = APIRouter(prefix="/api", tags=["Analysis"])

def generate_analysis_id() -> str:
    """Generate unique analysis ID: ANL-YYYYMMDD-XXXXX"""
    date_str = datetime.now().strftime("%Y%m%d")
    timestamp = datetime.now().strftime("%H%M%S")
    return f"ANL-{date_str}-{timestamp}"

@router.post("/analyze", response_model=FullAnalysisResponse)
def analyze_crop(
    input_data: AnalysisInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Main analysis endpoint - Returns comprehensive crop analysis"""
    
    # Generate analysis ID
    analysis_id = generate_analysis_id()
    
    # 1. Get crop recommendation
    crop_rec = get_crop_recommendation(input_data)
    selected_crop = crop_rec["recommended_crop"]
    
    # If user specified a crop preference (not "auto"), use that
    if input_data.crop_preference and input_data.crop_preference.lower() != "auto":
        selected_crop = input_data.crop_preference
    
    # 2. Predict yield
    yield_pred = predict_yield(selected_crop, input_data)
    
    # 3. Predict price
    price_pred = predict_price(selected_crop, input_data)
    
    # 4. Get fertilizer recommendation
    fertilizer_rec = get_fertilizer_recommendation(selected_crop, input_data)
    
    # 5. Get disease risk and pesticide recommendation
    disease_risk = get_disease_risk(selected_crop, input_data)
    
    # 6. Calculate harvest time
    sowing_date = input_data.sowing_date or datetime.now().strftime("%Y-%m-%d")
    harvest_pred = {
        "sowing_date": sowing_date,
        "expected_harvest_start": "",
        "expected_harvest_end": "",
        "days_to_harvest": 0,
        "harvest_tips": []
    }
    
    # Calculate harvest dates based on crop
    crop_durations = {
        "Rice": 120, "Wheat": 130, "Maize": 100, "Soybean": 110,
        "Cotton": 180, "Sugarcane": 365, "Groundnut": 120, "Mustard": 110,
        "Chickpea": 100, "Potato": 90, "Onion": 120, "Tomato": 90
    }
    duration = crop_durations.get(selected_crop, 120)
    
    from datetime import timedelta
    sowing = datetime.strptime(sowing_date, "%Y-%m-%d")
    harvest_start = sowing + timedelta(days=duration - 10)
    harvest_end = sowing + timedelta(days=duration + 10)
    
    harvest_pred = {
        "sowing_date": sowing_date,
        "expected_harvest_start": harvest_start.strftime("%Y-%m-%d"),
        "expected_harvest_end": harvest_end.strftime("%Y-%m-%d"),
        "days_to_harvest": duration,
        "harvest_tips": [
            f"Harvest when {selected_crop} reaches maturity",
            "Check moisture content before harvesting",
            "Harvest in dry weather conditions",
            "Store in clean, dry containers"
        ]
    }
    
    # 7. Yield improvement tips
    yield_tips = [
        f"Use certified seeds for {selected_crop} to improve germination by 10-15%",
        "Apply micronutrients (Zinc Sulphate) for better yield",
        "Maintain proper plant spacing for optimal growth",
        "Irrigate at critical growth stages",
        "Monitor for pests regularly and take preventive action"
    ]
    
    # 8. Get eligible government schemes
    schemes = get_eligible_schemes(current_user, input_data)
    
    # 9. Get irrigation planning
    irrigation = get_irrigation_planning(selected_crop, input_data)
    
    # 10. Calculate logistics cost
    logistics = calculate_logistics_cost(
        selected_crop, 
        yield_pred["total_yield_quintal"],
        input_data
    )
    
    # 11. Calculate profit analysis (with actual irrigation costs)
    profit = calculate_profit(
        selected_crop,
        yield_pred,
        price_pred,
        fertilizer_rec,
        disease_risk,
        logistics,
        input_data,
        irrigation
    )
    
    # 12. Logistics Recommendation
    logistics_rec = {
        "transport_mode": "Mini Truck (Tata Ace)" if input_data.land_area_acres < 2 else "Heavy Truck (10-Wheeler)",
        "estimated_cost": logistics["total_logistics"],
        "nearest_mandi": input_data.nearest_mandi or "Local Market",
        "storage_advice": [
            f"Store {selected_crop} in a cool, dry place to prevent spoilage",
            "Use grain bags with inner liners for moisture protection",
            "Ensure the storage area is well-ventilated and pest-controlled"
        ],
        "transport_tips": [
            "Use waterproof tarpaulin cover to protect the harvest during transit",
            "Load and unload carefully to minimize physical damage to the crop",
            "Prefer night or early morning transport for perishable crops to maintain freshness"
        ]
    }
    
    # Build response
    response = FullAnalysisResponse(
        analysis_id=analysis_id,
        farmer_id=current_user.farmer_id,
        crop_recommendation={
            "recommended_crop": crop_rec.get("recommended_crop"),
            "recommended_variety": crop_rec.get("recommended_variety"),
            "confidence": crop_rec.get("confidence"),
            "suitable_lands": crop_rec.get("suitable_lands", []),
            "alternatives": crop_rec.get("alternatives", []),
            "reasoning": crop_rec.get("reasoning"),
            "variety_details": crop_rec.get("variety_details")
        },
        yield_prediction={
            "expected_yield_per_acre": yield_pred["expected_per_acre"],
            "total_yield_quintal": yield_pred["total_yield_quintal"],
            "confidence_range": yield_pred["confidence_range"]
        },
        price_prediction={
            "current_price_per_quintal": price_pred["current_price"],
            "predicted_price_at_harvest": price_pred["predicted_price"],
            "price_trend": price_pred["trend"],
            "forecast_30_days": price_pred["forecast"]
        },
        fertilizer_recommendation={
            "recommendations": fertilizer_rec["recommendations"],
            "total_cost": fertilizer_rec["total_cost"]
        },
        disease_risk={
            "disease_risk_level": disease_risk["risk_level"],
            "likely_diseases": disease_risk["diseases"],
            "pesticides": disease_risk["pesticides"],
            "total_cost": disease_risk["total_cost"]
        },
        harvest_prediction=harvest_pred,
        irrigation_planning={
            "irrigation_required_mm": irrigation["irrigation_required_mm"],
            "total_water_needed_mm": irrigation["total_water_needed_mm"],
            "rainfall_mm": irrigation["rainfall_mm"],
            "irrigation_method": irrigation["irrigation_method"],
            "irrigation_schedule": irrigation["irrigation_schedule"],
            "water_management_tips": irrigation["water_management_tips"],
            "estimated_cost_per_acre": irrigation["estimated_cost_per_acre"],
            "efficiency_percentage": irrigation["efficiency_percentage"]
        },
        yield_improvement_tips=yield_tips,
        government_schemes=schemes,
        logistics_cost=logistics,
        logistics_recommendation=logistics_rec,  # Include the new field
        profit_analysis=profit,
        created_at=datetime.now().isoformat()
    )
    
    # Save to history
    history = AnalysisHistory(
        user_id=current_user.id,
        analysis_id=analysis_id,
        input_data=json.dumps(input_data.dict()),
        results=json.dumps(response.dict())
    )
    db.add(history)
    db.commit()
    
    return response

@router.get("/history")
def get_analysis_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's analysis history"""
    history = db.query(AnalysisHistory).filter(
        AnalysisHistory.user_id == current_user.id
    ).order_by(AnalysisHistory.created_at.desc()).all()
    
    result = []
    for h in history:
        results = json.loads(h.results)
        result.append({
            "analysis_id": h.analysis_id,
            "crop": results.get("crop_recommendation", {}).get("recommended_crop", "N/A"),
            "profit": results.get("profit_analysis", {}).get("net_profit", 0),
            "created_at": h.created_at.isoformat() if h.created_at else ""
        })
    
    return result

@router.get("/history/{analysis_id}")
def get_analysis_detail(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific analysis details"""
    history = db.query(AnalysisHistory).filter(
        AnalysisHistory.analysis_id == analysis_id,
        AnalysisHistory.user_id == current_user.id
    ).first()
    
    if not history:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return json.loads(history.results)

@router.get("/crops")
def get_crops_list():
    """Get list of all supported crops"""
    import os
    # Data files are in app/data directory
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "app", "data", "crops.json")
    with open(data_path, "r", encoding="utf-8") as f:
        crops = json.load(f)
    return crops

@router.get("/schemes")
def get_all_schemes():
    """Get list of all government schemes"""
    import os
    # Data files are in app/data directory
    # Use absolute path to avoid working directory issues
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));
    data_path = os.path.join(backend_dir, "app", "data", "schemes.json")
    with open(data_path, "r") as f:
        schemes = json.load(f)
    return schemes

@router.get("/states")
def get_states():
    """Get list of Indian states with districts"""
    from app.config import settings
    
    # Comprehensive list of all Indian states and districts
    state_districts = {
        # Andhra Pradesh
        "Andhra Pradesh": [
            "Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna", 
            "Kurnool", "Prakasam", "Srikakulam", "Sri Potti Sri Ramulu Nellore", 
            "Vishakhapatnam", "Vizianagaram", "West Godavari", "YSR Kadapa"
        ],
        
        # Arunachal Pradesh
        "Arunachal Pradesh": [
            "Anjaw", "Changlang", "Dibang Valley", "East Kameng", "East Siang", 
            "Kamle", "Kra Daadi", "Kurung Kumey", "Lepa Rada", "Lohit", 
            "Longding", "Lower Dibang Valley", "Lower Siang", "Lower Subansiri", 
            "Namsai", "Pakke Kessang", "Papum Pare", "Shi Yomi", "Siang", 
            "Tawang", "Tirap", "Upper Siang", "Upper Subansiri", "West Kameng", "West Siang"
        ],
        
        # Assam
        "Assam": [
            "Baksa", "Barpeta", "Biswanath", "Bongaigaon", "Cachar", 
            "Charaideo", "Chirang", "Darrang", "Dhemaji", "Dhubri", 
            "Dibrugarh", "Goalpara", "Golaghat", "Hailakandi", "Hojai", 
            "Jorhat", "Kamrup", "Kamrup Metropolitan", "Karbi Anglong", "Karimganj", 
            "Kokrajhar", "Lakhimpur", "Majuli", "Morigaon", "Nagaon", 
            "Nalbari", "Sivasagar", "Sonitpur", "South Salmara Mankachar", "Tinsukia", 
            "Udalguri", "West Karbi Anglong"
        ],
        
        # Bihar
        "Bihar": [
            "Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", 
            "Bhagalpur", "Bhojpur", "Buxar", "Darbhanga", "East Champaran", 
            "Gaya", "Gopalganj", "Jamui", "Jehanabad", "Kaimur", 
            "Katihar", "Khagaria", "Kishanganj", "Lakhisarai", "Madhepura", 
            "Madhubani", "Munger", "Muzaffarpur", "Nalanda", "Nawada", 
            "Patna", "Purnia", "Rohtas", "Saharsa", "Samastipur", 
            "Saran", "Sheikhpura", "Sheohar", "Sitamarhi", "Siwan", 
            "Supaul", "Vaishali", "West Champaran"
        ],
        
        # Chhattisgarh
        "Chhattisgarh": [
            "Balod", "Baloda Bazar", "Balrampur", "Bastar", "Bemetara", 
            "Bijapur", "Bilaspur", "Dantewada", "Dhamtari", "Durg", 
            "Gariaband", "Gaurela Pendra Marwahi", "Janjgir Champa", "Jashpur", "Kanker", 
            "Kondagaon", "Korba", "Koriya", "Mahasamund", "Mungeli", 
            "Narayanpur", "Raigarh", "Raipur", "Rajnandgaon", "Sukma", 
            "Surajpur", "Surguja"
        ],
        
        # Goa
        "Goa": [
            "North Goa", "South Goa"
        ],
        
        # Gujarat
        "Gujarat": [
            "Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha", 
            "Bharuch", "Bhavnagar", "Botad", "Chhota Udepur", "Dahod", 
            "Dang", "Devbhoomi Dwarka", "Gandhinagar", "Gir Somnath", "Jamnagar", 
            "Junagadh", "Kheda", "Kutch", "Mahisagar", "Mehsana", 
            "Morbi", "Narmada", "Navsari", "Panchmahal", "Patan", 
            "Porbandar", "Rajkot", "Sabarkantha", "Surat", "Surendranagar", 
            "Tapi", "Vadodara", "Valsad"
        ],
        
        # Haryana
        "Haryana": [
            "Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad", 
            "Gurugram", "Hisar", "Jhajjar", "Jind", "Kaithal", 
            "Karnal", "Kurukshetra", "Mahendragarh", "Nuh", "Palwal", 
            "Panchkula", "Panipat", "Rewari", "Rohtak", "Sirsa", 
            "Sonipat", "Yamunanagar"
        ],
        
        # Himachal Pradesh
        "Himachal Pradesh": [
            "Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kinnaur", 
            "Kullu", "Lahaul Spiti", "Mandi", "Shimla", "Sirmaur", 
            "Solan", "Una"
        ],
        
        # Jharkhand
        "Jharkhand": [
            "Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka", 
            "East Singhbhum", "Garhwa", "Giridih", "Godda", "Gumla", 
            "Hazaribagh", "Jamtara", "Khunti", "Koderma", "Latehar", 
            "Lohardaga", "Pakur", "Palamu", "Ramgarh", "Ranchi", 
            "Sahibganj", "Seraikela Kharsawan", "Simdega", "West Singhbhum"
        ],
        
        # Karnataka
        "Karnataka": [
            "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban", 
            "Bidar", "Chamarajanagar", "Chikkaballapur", "Chikkamagaluru", "Chitradurga", 
            "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan", 
            "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal", 
            "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga", 
            "Tumakuru", "Udupi", "Uttara Kannada", "Vijayapura", "Yadgir"
        ],
        
        # Kerala
        "Kerala": [
            "Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod", 
            "Kollam", "Kottayam", "Kozhikode", "Malappuram", "Palakkad", 
            "Pathanamthitta", "Thiruvananthapuram", "Thrissur", "Wayanad"
        ],
        
        # Madhya Pradesh
        "Madhya Pradesh": [
            "Agar Malwa", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat", 
            "Barwani", "Betul", "Bhind", "Bhopal", "Burhanpur", 
            "Chhatarpur", "Chhindwara", "Damoh", "Datia", "Dewas", 
            "Dhar", "Dindori", "Guna", "Gwalior", "Harda", 
            "Hoshangabad", "Indore", "Jabalpur", "Jhabua", "Katni", 
            "Khandwa", "Khargone", "Mandla", "Mandsaur", "Morena", 
            "Narsinghpur", "Neemuch", "Niwari", "Panna", "Raisen", 
            "Rajgarh", "Ratlam", "Rewa", "Sagar", "Satna", 
            "Sehore", "Seoni", "Shahdol", "Shajapur", "Sheopur", 
            "Shivpuri", "Sidhi", "Singrauli", "Tikamgarh", "Ujjain", 
            "Umaria", "Vidisha"
        ],
        
        # Maharashtra
        "Maharashtra": [
            "Ahmednagar", "Akola", "Amravati", "Aurangabad", "Beed", 
            "Bhandara", "Buldhana", "Chandrapur", "Dhule", "Gadchiroli", 
            "Gondia", "Hingoli", "Jalgaon", "Jalna", "Kolhapur", 
            "Latur", "Mumbai City", "Mumbai Suburban", "Nagpur", "Nanded", 
            "Nandurbar", "Nashik", "Osmanabad", "Palghar", "Parbhani", 
            "Pune", "Raigad", "Ratnagiri", "Sangli", "Satara", 
            "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim", 
            "Yavatmal"
        ],
        
        # Manipur
        "Manipur": [
            "Bishnupur", "Chandel", "Churachandpur", "Imphal East", "Imphal West", 
            "Jiribam", "Kakching", "Kamjong", "Kangpokpi", "Noney", 
            "Pherzawl", "Senapati", "Tamenglong", "Tengnoupal", "Thoubal", 
            "Ukhrul"
        ],
        
        # Meghalaya
        "Meghalaya": [
            "East Garo Hills", "East Jaintia Hills", "East Khasi Hills", "North Garo Hills", 
            "Ri Bhoi", "South Garo Hills", "South West Garo Hills", "South West Khasi Hills", 
            "West Garo Hills", "West Jaintia Hills", "West Khasi Hills"
        ],
        
        # Mizoram
        "Mizoram": [
            "Aizawl", "Champhai", "Hnahthial", "Khawzawl", "Kolasib", 
            "Lawngtlai", "Lunglei", "Mamit", "Saiha", "Saitual", 
            "Serchhip"
        ],
        
        # Nagaland
        "Nagaland": [
            "Dimapur", "Kiphire", "Kohima", "Longleng", "Mokokchung", 
            "Mon", "Peren", "Phek", "Tuensang", "Wokha", 
            "Zunheboto"
        ],
        
        # Odisha
        "Odisha": [
            "Angul", "Balangir", "Balasore", "Bargarh", "Bhadrak", 
            "Boudh", "Cuttack", "Deogarh", "Dhenkanal", "Gajapati", 
            "Ganjam", "Jagatsinghpur", "Jajpur", "Jharsuguda", "Kalahandi", 
            "Kandhamal", "Kendrapara", "Kendujhar", "Khordha", "Koraput", 
            "Malkangiri", "Mayurbhanj", "Nabarangpur", "Nayagarh", "Nuapada", 
            "Puri", "Rayagada", "Sambalpur", "Subarnapur", "Sundergarh"
        ],
        
        # Punjab
        "Punjab": [
            "Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib", 
            "Fazilka", "Ferozepur", "Gurdaspur", "Hoshiarpur", "Jalandhar", 
            "Kapurthala", "Ludhiana", "Mansa", "Moga", "Pathankot", 
            "Patiala", "Rupnagar", "Sangrur", "Shaheed Bhagat Singh Nagar", "Sri Muktsar Sahib", 
            "Tarn Taran"
        ],
        
        # Rajasthan
        "Rajasthan": [
            "Ajmer", "Alwar", "Banswara", "Baran", "Barmer", 
            "Bharatpur", "Bhilwara", "Bikaner", "Bundi", "Chittorgarh", 
            "Churu", "Dausa", "Dholpur", "Dungarpur", "Hanumangarh", 
            "Jaipur", "Jaisalmer", "Jalore", "Jhalawar", "Jhunjhunu", 
            "Jodhpur", "Karauli", "Kota", "Nagaur", "Pali", 
            "Pratapgarh", "Rajsamand", "Sawai Madhopur", "Sikar", "Sirohi", 
            "Tonk", "Udaipur"
        ],
        
        # Sikkim
        "Sikkim": [
            "East Sikkim", "North Sikkim", "South Sikkim", "West Sikkim"
        ],
        
        # Tamil Nadu
        "Tamil Nadu": [
            "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore", 
            "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kancheepuram", 
            "Karur", "Krishnagiri", "Madurai", "Nagapattinam", "Namakkal", 
            "Nilgiris", "Perambalur", "Pudukkottai", "Ramanathapuram", "Salem", 
            "Sivaganga", "Tenkasi", "Thanjavur", "Theni", "Thoothukudi", 
            "Tiruchirappalli", "Tirunelveli", "Tirupathur", "Tiruppur", "Tiruvallur", 
            "Tiruvannamalai", "Tiruvarur", "Vellore", "Viluppuram", "Virudhunagar"
        ],
        
        # Telangana
        "Telangana": [
            "Adilabad", "Bhadradri Kothagudem", "Hyderabad", "Jagtial", "Jangaon", 
            "Jayashankar Bhupalapally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar", "Khammam", 
            "Komaram Bheem", "Mahabubabad", "Mahabubnagar", "Mancherial", "Medak", 
            "Medchal Malkajgiri", "Mulugu", "Nagarkurnool", "Nalgonda", "Narayanpet", 
            "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla", "Ranga Reddy", 
            "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", "Wanaparthy", 
            "Warangal Rural", "Warangal Urban", "Yadadri Bhuvanagiri"
        ],
        
        # Tripura
        "Tripura": [
            "Dhalai", "Gomati", "Khowai", "North Tripura", 
            "Sepahijala", "South Tripura", "Unakoti", "West Tripura"
        ],
        
        # Uttar Pradesh
        "Uttar Pradesh": [
            "Agra", "Aligarh", "Ambedkar Nagar", "Amethi", "Amroha", 
            "Auraiya", "Ayodhya", "Azamgarh", "Baghpat", "Bahraich", 
            "Ballia", "Balrampur", "Banda", "Barabanki", "Bareilly", 
            "Basti", "Bhadohi", "Bijnor", "Budaun", "Bulandshahr", 
            "Chandauli", "Chitrakoot", "Deoria", "Etah", "Etawah", 
            "Farrukhabad", "Fatehpur", "Firozabad", "Gautam Buddha Nagar", "Ghaziabad", 
            "Ghazipur", "Gonda", "Gorakhpur", "Hamirpur", "Hapur", 
            "Hardoi", "Hathras", "Jalaun", "Jaunpur", "Jhansi", 
            "Kannauj", "Kanpur Dehat", "Kanpur Nagar", "Kasganj", "Kaushambi", 
            "Kheri", "Kushinagar", "Lalitpur", "Lucknow", "Maharajganj", 
            "Mahoba", "Mainpuri", "Mathura", "Mau", "Meerut", 
            "Mirzapur", "Moradabad", "Muzaffarnagar", "Pilibhit", "Pratapgarh", 
            "Prayagraj", "Raebareli", "Rampur", "Saharanpur", "Sambhal", 
            "Sant Kabir Nagar", "Shahjahanpur", "Shamli", "Shravasti", "Siddharthnagar", 
            "Sitapur", "Sonbhadra", "Sultanpur", "Unnao", "Varanasi"
        ],
        
        # Uttarakhand
        "Uttarakhand": [
            "Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", 
            "Haridwar", "Nainital", "Pauri Garhwal", "Pithoragarh", "Rudraprayag", 
            "Tehri Garhwal", "Udham Singh Nagar", "Uttarkashi"
        ],
        
        # West Bengal
        "West Bengal": [
            "Alipurduar", "Bankura", "Birbhum", "Cooch Behar", "Dakshin Dinajpur", 
            "Darjeeling", "Hooghly", "Howrah", "Jalpaiguri", "Jhargram", 
            "Kalimpong", "Kolkata", "Malda", "Murshidabad", "Nadia", 
            "North 24 Parganas", "Paschim Bardhaman", "Paschim Medinipur", "Purba Bardhaman", 
            "Purba Medinipur", "Purulia", "South 24 Parganas", "Uttar Dinajpur"
        ],
        
        # Union Territories
        "Delhi": [
            "Central Delhi", "East Delhi", "New Delhi", "North Delhi", 
            "North East Delhi", "North West Delhi", "Shahdara", "South Delhi", 
            "South East Delhi", "South West Delhi", "West Delhi"
        ],
        
        "Jammu and Kashmir": [
            "Anantnag", "Bandipora", "Baramulla", "Budgam", "Doda", 
            "Ganderbal", "Jammu", "Kathua", "Kishtwar", "Kulgam", 
            "Kupwara", "Poonch", "Pulwama", "Rajouri", "Ramban", 
            "Reasi", "Samba", "Shopian", "Srinagar", "Udhampur"
        ],
        
        "Ladakh": [
            "Kargil", "Leh"
        ],
        
        "Puducherry": [
            "Karaikal", "Mahe", "Puducherry", "Yanam"
        ],
        
        "Chandigarh": [
            "Chandigarh"
        ],
        
        "Dadra and Nagar Haveli and Daman and Diu": [
            "Dadra and Nagar Haveli", "Daman", "Diu"
        ],
        
        "Lakshadweep": [
            "Lakshadweep"
        ],
        
        "Andaman and Nicobar Islands": [
            "Nicobar", "North and Middle Andaman", "South Andaman"
        ]
    }
    
    result = []
    for state, code in settings.STATE_CODES.items():
        result.append({
            "name": state,
            "code": code,
            "districts": state_districts.get(state, [f"{state} District 1", f"{state} District 2"])
        })
    
    return result

@router.get("/climate-dashboard")
def get_climate_dashboard(
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive climate data for dashboard display - UPDATED"""
    """Get comprehensive climate data for dashboard display"""
    try:
        print(f"Climate dashboard request for user: {current_user.farmer_id}")
        print(f"User state: {current_user.state}, district: {current_user.district}")
        
        # Create user data for climate analysis
        user_data = {
            "land_size": current_user.land_size_acres or 1.0,
            "irrigation_type": "rainfed",  # Default assumption
            "soil_type": "alluvial",  # Default assumption
            "state": current_user.state,
            "district": current_user.district
        }
        
        print("Calling get_climate_dashboard_data...")
        climate_data = get_climate_dashboard_data(
            current_user.state, 
            current_user.district, 
            user_data
        )
        print("get_climate_dashboard_data returned successfully")
        
        print(f"Climate data keys: {list(climate_data.keys())}")
        print(f"Current weather keys: {list(climate_data['current_weather'].keys())}")
        print(f"Current weather source: {climate_data['current_weather']['source']}")
        print(f"Soil moisture 0-1cm: {climate_data['current_weather'].get('soil_moisture_0_1cm', 'NOT FOUND')}")
        print(f"Wind speed 10m: {climate_data['current_weather'].get('wind_speed_10m', 'NOT FOUND')}")
        print(f"Wind speed (old key): {climate_data['current_weather'].get('wind_speed', 'NOT FOUND')}")
        print(f"Weather analysis present: {'weather_analysis' in climate_data}")
                                
        # The climate_data already contains all the weather parameters we need
        # No need to update since get_climate_dashboard_data returns the complete data
        pass
                                
        return climate_data
    except Exception as e:
        print(f"Error in climate dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching climate data: {str(e)}")
