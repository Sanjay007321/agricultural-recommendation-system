#!/usr/bin/env python
import json

# Complete crops data with all varieties
crops_data = {
  "crops": [
    {
      "name": "Rice",
      "tamil_name": "Rice",
      "season": ["Kharif"],
      "duration_days": 120,
      "soil_types": ["Clay", "Loamy", "Alluvial"],
      "ph_range": [5.5, 7.0],
      "temperature_range": [20, 35],
      "rainfall_mm": [1000, 2000],
      "nitrogen_required": 120,
      "phosphorus_required": 60,
      "potassium_required": 40,
      "avg_yield_quintal_per_acre": 20,
      "avg_price_per_quintal": 2200,
      "seed_cost_per_acre": 800,
      "labor_cost_per_acre": 8000,
      "suitable_lands": ["Low-lying areas", "Water-logged regions", "Alluvial plains", "River deltas"],
      "varieties": [
        {"name": "IR-8", "duration": "120-125", "yield_quintal_acre": 22, "price_per_quintal": 2200, "characteristics": "High yielding semi-dwarf", "water_requirement": "High (1000-2000mm)", "best_for": "Irrigated plains"},
        {"name": "BPT5204", "duration": "125-130", "yield_quintal_acre": 23, "price_per_quintal": 2400, "characteristics": "Long grain aromatic", "water_requirement": "High (1200-1800mm)", "best_for": "Quality markets"}
      ]
    },
    {
      "name": "Wheat",
      "tamil_name": "Wheat",
      "season": ["Rabi"],
      "duration_days": 130,
      "soil_types": ["Loamy", "Clay Loam", "Alluvial"],
      "ph_range": [6.0, 7.5],
      "temperature_range": [10, 25],
      "rainfall_mm": [400, 750],
      "nitrogen_required": 120,
      "phosphorus_required": 60,
      "potassium_required": 40,
      "avg_yield_quintal_per_acre": 18,
      "avg_price_per_quintal": 2300,
      "seed_cost_per_acre": 1200,
      "labor_cost_per_acre": 6000,
      "suitable_lands": ["Well-drained areas", "Leveled fields", "Loamy plains", "Semi-arid regions"],
      "varieties": [
        {"name": "HD-2967", "duration": "125-135", "yield_quintal_acre": 22, "price_per_quintal": 2400, "characteristics": "High yielding dwarf", "water_requirement": "500-600mm", "best_for": "Northern plains"},
        {"name": "DBW-17", "duration": "130-140", "yield_quintal_acre": 25, "price_per_quintal": 2450, "characteristics": "Strong gluten", "water_requirement": "450-550mm", "best_for": "Central south regions"}
      ]
    },
    {
      "name": "Maize",
      "tamil_name": "Maize",
      "season": ["Kharif", "Rabi"],
      "duration_days": 100,
      "soil_types": ["Loamy", "Sandy Loam", "Alluvial"],
      "ph_range": [5.5, 7.5],
      "temperature_range": [18, 32],
      "rainfall_mm": [500, 1000],
      "nitrogen_required": 150,
      "phosphorus_required": 60,
      "potassium_required": 40,
      "avg_yield_quintal_per_acre": 25,
      "avg_price_per_quintal": 1900,
      "seed_cost_per_acre": 1500,
      "labor_cost_per_acre": 5000,
      "suitable_lands": ["Well-drained uplands", "Fertile black soil", "Sloping lands"],
      "varieties": [
        {"name": "HM-4", "duration": "95-105", "yield_quintal_acre": 28, "price_per_quintal": 2100, "characteristics": "Hybrid silage high biomass", "water_requirement": "600-800mm", "best_for": "Fodder production"},
        {"name": "HQPM-1", "duration": "100-110", "yield_quintal_acre": 32, "price_per_quintal": 2300, "characteristics": "Quality protein maize", "water_requirement": "700-900mm", "best_for": "Poultry feed"}
      ]
    },
    {
      "name": "Soybean",
      "tamil_name": "Soybean",
      "season": ["Kharif"],
      "duration_days": 110,
      "soil_types": ["Black Soil", "Loamy", "Clay Loam"],
      "ph_range": [6.0, 7.5],
      "temperature_range": [20, 30],
      "rainfall_mm": [600, 1000],
      "nitrogen_required": 25,
      "phosphorus_required": 60,
      "potassium_required": 40,
      "avg_yield_quintal_per_acre": 12,
      "avg_price_per_quintal": 4200,
      "seed_cost_per_acre": 2000,
      "labor_cost_per_acre": 5000,
      "suitable_lands": ["Black soil regions", "Alluvial soil areas", "Well-drained uplands"],
      "varieties": [
        {"name": "JS-9305", "duration": "105-110", "yield_quintal_acre": 14, "price_per_quintal": 4500, "characteristics": "High protein disease resistant", "water_requirement": "650-750mm", "best_for": "Central India"},
        {"name": "JS-335", "duration": "100-105", "yield_quintal_acre": 13, "price_per_quintal": 4300, "characteristics": "Short duration early maturity", "water_requirement": "600-700mm", "best_for": "Double cropping"}
      ]
    },
    {
      "name": "Cotton",
      "tamil_name": "Cotton",
      "season": ["Kharif"],
      "duration_days": 180,
      "soil_types": ["Black Soil", "Alluvial", "Red Soil"],
      "ph_range": [6.0, 8.0],
      "temperature_range": [21, 35],
      "rainfall_mm": [600, 1200],
      "nitrogen_required": 150,
      "phosphorus_required": 60,
      "potassium_required": 60,
      "avg_yield_quintal_per_acre": 8,
      "avg_price_per_quintal": 6500,
      "seed_cost_per_acre": 2500,
      "labor_cost_per_acre": 10000,
      "suitable_lands": ["Black soil areas", "Red soil regions", "Well-drained areas", "High temperature zones"],
      "varieties": [
        {"name": "MCU-5", "duration": "175-185", "yield_quintal_acre": 9, "price_per_quintal": 7000, "characteristics": "Long staple high strength", "water_requirement": "750-900mm", "best_for": "Premium market"},
        {"name": "Bt-Cotton", "duration": "170-180", "yield_quintal_acre": 10, "price_per_quintal": 6800, "characteristics": "Insect resistant", "water_requirement": "700-850mm", "best_for": "Large-scale farming"}
      ]
    },
    {
      "name": "Sugarcane",
      "tamil_name": "Sugarcane",
      "season": ["Kharif", "Rabi"],
      "duration_days": 365,
      "soil_types": ["Loamy", "Clay Loam", "Alluvial"],
      "ph_range": [6.0, 8.0],
      "temperature_range": [20, 35],
      "rainfall_mm": [1500, 2500],
      "nitrogen_required": 250,
      "phosphorus_required": 100,
      "potassium_required": 100,
      "avg_yield_quintal_per_acre": 350,
      "avg_price_per_quintal": 350,
      "seed_cost_per_acre": 8000,
      "labor_cost_per_acre": 15000,
      "suitable_lands": ["Fertile alluvial plains", "High rainfall areas", "Well-irrigated fertile lands", "River valley regions"],
      "varieties": [
        {"name": "Co-86032", "duration": "360-365", "yield_quintal_acre": 380, "price_per_quintal": 360, "characteristics": "High sugar content disease resistant", "water_requirement": "1800-2200mm", "best_for": "Sugar mills"},
        {"name": "Co-94008", "duration": "360-365", "yield_quintal_acre": 350, "price_per_quintal": 340, "characteristics": "Medium duration good recovery", "water_requirement": "1600-2000mm", "best_for": "Rainfed with irrigation"}
      ]
    },
    {
      "name": "Groundnut",
      "tamil_name": "Groundnut",
      "season": ["Kharif", "Rabi"],
      "duration_days": 120,
      "soil_types": ["Sandy Loam", "Red Soil", "Loamy"],
      "ph_range": [5.5, 7.0],
      "temperature_range": [25, 35],
      "rainfall_mm": [500, 1000],
      "nitrogen_required": 20,
      "phosphorus_required": 60,
      "potassium_required": 40,
      "avg_yield_quintal_per_acre": 10,
      "avg_price_per_quintal": 5500,
      "seed_cost_per_acre": 3500,
      "labor_cost_per_acre": 6000,
      "suitable_lands": ["Sandy loam areas", "Red soil zones", "Well-drained uplands", "Rainfed areas"],
      "varieties": [
        {"name": "TAG-24", "duration": "115-120", "yield_quintal_acre": 11, "price_per_quintal": 5800, "characteristics": "Bold kernel high shelling", "water_requirement": "600-750mm", "best_for": "Market sale"},
        {"name": "Kadiri-6", "duration": "100-110", "yield_quintal_acre": 10, "price_per_quintal": 5600, "characteristics": "Early maturing", "water_requirement": "500-600mm", "best_for": "Summer season"}
      ]
    },
    {
      "name": "Mustard",
      "tamil_name": "Mustard",
      "season": ["Rabi"],
      "duration_days": 110,
      "soil_types": ["Loamy", "Sandy Loam", "Alluvial"],
      "ph_range": [6.0, 7.5],
      "temperature_range": [10, 25],
      "rainfall_mm": [250, 500],
      "nitrogen_required": 80,
      "phosphorus_required": 40,
      "potassium_required": 20,
      "avg_yield_quintal_per_acre": 8,
      "avg_price_per_quintal": 5200,
      "seed_cost_per_acre": 400,
      "labor_cost_per_acre": 4000,
      "suitable_lands": ["Semi-arid regions", "Rainfed areas", "Marginal lands", "Light soil areas"],
      "varieties": [
        {"name": "Yellow Sarson", "duration": "100-110", "yield_quintal_acre": 8, "price_per_quintal": 5000, "characteristics": "Low erucic acid", "water_requirement": "350-450mm", "best_for": "Oil industry"},
        {"name": "Black Mustard", "duration": "110-120", "yield_quintal_acre": 7, "price_per_quintal": 5500, "characteristics": "Spice use traditional", "water_requirement": "300-400mm", "best_for": "Spice industry"}
      ]
    },
    {
      "name": "Chickpea",
      "tamil_name": "Chickpea",
      "season": ["Rabi"],
      "duration_days": 100,
      "soil_types": ["Loamy", "Clay Loam", "Black Soil"],
      "ph_range": [6.0, 8.0],
      "temperature_range": [15, 30],
      "rainfall_mm": [300, 500],
      "nitrogen_required": 20,
      "phosphorus_required": 40,
      "potassium_required": 20,
      "avg_yield_quintal_per_acre": 8,
      "avg_price_per_quintal": 5000,
      "seed_cost_per_acre": 2000,
      "labor_cost_per_acre": 4000,
      "suitable_lands": ["Black soil areas", "Clay loam soils", "Rainfed areas", "Marginal lands"],
      "varieties": [
        {"name": "Jaki-9218", "duration": "100-105", "yield_quintal_acre": 9, "price_per_quintal": 5200, "characteristics": "Bold seeds pest resistant", "water_requirement": "400-500mm", "best_for": "Premium market"},
        {"name": "Pusa-362", "duration": "95-100", "yield_quintal_acre": 8, "price_per_quintal": 4900, "characteristics": "Wilt resistant", "water_requirement": "350-450mm", "best_for": "Disease-prone areas"}
      ]
    },
    {
      "name": "Potato",
      "tamil_name": "Potato",
      "season": ["Rabi"],
      "duration_days": 90,
      "soil_types": ["Sandy Loam", "Loamy", "Alluvial"],
      "ph_range": [5.5, 7.0],
      "temperature_range": [15, 25],
      "rainfall_mm": [400, 600],
      "nitrogen_required": 180,
      "phosphorus_required": 80,
      "potassium_required": 100,
      "avg_yield_quintal_per_acre": 100,
      "avg_price_per_quintal": 1200,
      "seed_cost_per_acre": 15000,
      "labor_cost_per_acre": 8000,
      "suitable_lands": ["Cool climate areas", "High altitude regions", "Well-drained loamy soil", "Northern plains"],
      "varieties": [
        {"name": "Kufri Badshah", "duration": "85-90", "yield_quintal_acre": 110, "price_per_quintal": 1300, "characteristics": "High yield medium maturity", "water_requirement": "500-550mm", "best_for": "Commercial cultivation"},
        {"name": "Kufri Himalini", "duration": "80-85", "yield_quintal_acre": 105, "price_per_quintal": 1250, "characteristics": "Late blight resistant", "water_requirement": "450-500mm", "best_for": "Hilly areas"}
      ]
    },
    {
      "name": "Onion",
      "tamil_name": "Onion",
      "season": ["Kharif", "Rabi"],
      "duration_days": 120,
      "soil_types": ["Loamy", "Sandy Loam", "Clay Loam"],
      "ph_range": [6.0, 7.5],
      "temperature_range": [15, 30],
      "rainfall_mm": [400, 600],
      "nitrogen_required": 100,
      "phosphorus_required": 60,
      "potassium_required": 60,
      "avg_yield_quintal_per_acre": 80,
      "avg_price_per_quintal": 1500,
      "seed_cost_per_acre": 2000,
      "labor_cost_per_acre": 10000,
      "suitable_lands": ["Well-drained fertile soil", "Alluvial soil areas", "Slightly elevated fields"],
      "varieties": [
        {"name": "Allium Cepa", "duration": "120-130", "yield_quintal_acre": 90, "price_per_quintal": 1600, "characteristics": "Medium storage pungent", "water_requirement": "500-600mm", "best_for": "Local markets"},
        {"name": "Bombay Red", "duration": "110-120", "yield_quintal_acre": 85, "price_per_quintal": 1700, "characteristics": "Red colored good storage", "water_requirement": "450-550mm", "best_for": "Export markets"}
      ]
    },
    {
      "name": "Tomato",
      "tamil_name": "Tomato",
      "season": ["Kharif", "Rabi", "Zaid"],
      "duration_days": 90,
      "soil_types": ["Loamy", "Sandy Loam", "Clay Loam"],
      "ph_range": [6.0, 7.5],
      "temperature_range": [20, 30],
      "rainfall_mm": [400, 600],
      "nitrogen_required": 120,
      "phosphorus_required": 80,
      "potassium_required": 80,
      "avg_yield_quintal_per_acre": 120,
      "avg_price_per_quintal": 1000,
      "seed_cost_per_acre": 3000,
      "labor_cost_per_acre": 12000,
      "suitable_lands": ["Well-drained soil", "Fertile loamy areas", "Slightly elevated fields", "Protected cultivation"],
      "varieties": [
        {"name": "Pusa Ruby", "duration": "85-90", "yield_quintal_acre": 130, "price_per_quintal": 1100, "characteristics": "Deep red disease resistant", "water_requirement": "500-600mm", "best_for": "Urban markets"},
        {"name": "Arka Vikas", "duration": "80-85", "yield_quintal_acre": 125, "price_per_quintal": 1050, "characteristics": "High lycopene good taste", "water_requirement": "450-550mm", "best_for": "Premium pricing"}
      ]
    },
    {
      "name": "Turmeric",
      "tamil_name": "Turmeric",
      "season": ["Kharif"],
      "duration_days": 270,
      "soil_types": ["Loamy", "Clay Loam", "Red Soil"],
      "ph_range": [5.5, 7.5],
      "temperature_range": [20, 35],
      "rainfall_mm": [1000, 2000],
      "nitrogen_required": 100,
      "phosphorus_required": 50,
      "potassium_required": 100,
      "avg_yield_quintal_per_acre": 80,
      "avg_price_per_quintal": 7500,
      "seed_cost_per_acre": 15000,
      "labor_cost_per_acre": 15000,
      "suitable_lands": ["High rainfall areas", "Well-draining Red soil", "Ghat regions", "High humidity zones"],
      "varieties": [
        {"name": "Megha Turmeric", "duration": "260-270", "yield_quintal_acre": 90, "price_per_quintal": 8000, "characteristics": "High curcumin content disease resistant", "water_requirement": "1200-1800mm", "best_for": "Processing industry"},
        {"name": "Salem Turmeric", "duration": "270-280", "yield_quintal_acre": 80, "price_per_quintal": 7800, "characteristics": "Medium fineness traditional", "water_requirement": "1000-1500mm", "best_for": "South India"}
      ]
    },
    {
      "name": "Chilli",
      "tamil_name": "Chilli",
      "season": ["Kharif", "Rabi"],
      "duration_days": 150,
      "soil_types": ["Loamy", "Sandy Loam", "Black Soil"],
      "ph_range": [6.0, 7.5],
      "temperature_range": [20, 35],
      "rainfall_mm": [600, 1200],
      "nitrogen_required": 100,
      "phosphorus_required": 50,
      "potassium_required": 50,
      "avg_yield_quintal_per_acre": 25,
      "avg_price_per_quintal": 12000,
      "seed_cost_per_acre": 1500,
      "labor_cost_per_acre": 10000,
      "suitable_lands": ["Well-drained loamy soil", "Sunflower growing regions", "Medium rainfall areas"],
      "varieties": [
        {"name": "Byadagi", "duration": "140-150", "yield_quintal_acre": 28, "price_per_quintal": 13500, "characteristics": "Low pungency high color", "water_requirement": "700-800mm", "best_for": "Paprika industry"},
        {"name": "Guntur Sannam", "duration": "150-160", "yield_quintal_acre": 25, "price_per_quintal": 12000, "characteristics": "Pungent medium-long pod", "water_requirement": "800-1000mm", "best_for": "Spice industry"}
      ]
    },
    {
      "name": "Sunflower",
      "tamil_name": "Sunflower",
      "season": ["Kharif", "Rabi"],
      "duration_days": 100,
      "soil_types": ["Loamy", "Black Soil", "Alluvial"],
      "ph_range": [6.0, 7.5],
      "temperature_range": [20, 30],
      "rainfall_mm": [500, 800],
      "nitrogen_required": 80,
      "phosphorus_required": 60,
      "potassium_required": 40,
      "avg_yield_quintal_per_acre": 8,
      "avg_price_per_quintal": 6000,
      "seed_cost_per_acre": 1200,
      "labor_cost_per_acre": 5000,
      "suitable_lands": ["Well-drained upland areas", "Black soil regions", "Semi-arid zones", "Marginal lands"],
      "varieties": [
        {"name": "KBSH-1", "duration": "95-100", "yield_quintal_acre": 9, "price_per_quintal": 6200, "characteristics": "High oil content drought tolerant", "water_requirement": "600-700mm", "best_for": "Oil extraction"},
        {"name": "Morden-6", "duration": "100-105", "yield_quintal_acre": 8, "price_per_quintal": 6000, "characteristics": "Compact plant intercropping suitable", "water_requirement": "500-600mm", "best_for": "Soil conservation"}
      ]
    }
  ],
  "soil_types": [
    "Alluvial",
    "Black Soil",
    "Red Soil",
    "Laterite Soil",
    "Sandy",
    "Sandy Loam",
    "Loamy",
    "Clay",
    "Clay Loam"
  ],
  "seasons": [
    "Kharif",
    "Rabi",
    "Zaid"
  ]
}

# Write to file
with open('app/data/crops.json', 'w', encoding='utf-8') as f:
    json.dump(crops_data, f, indent=2, ensure_ascii=True)

print("Complete crops.json created successfully with all 15 crops and varieties")
