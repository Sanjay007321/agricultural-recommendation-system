import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { analysisAPI, dataAPI } from '../services/api';
import { motion } from 'framer-motion';
import { MapPin, Sprout, TestTube, Map, ArrowRight, Loader2, Upload, Camera, Image as ImageIcon } from 'lucide-react';

const GetRecommendation = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [crops, setCrops] = useState([
    { 
      name: "Rice", 
      tamil_name: "அரிசி",
      varieties: [
        { name: "IR-8", duration: "120-125 days", yield_quintal_acre: 22, price_per_quintal: 2200, characteristics: "High yielding semi-dwarf", water_requirement: "High", best_for: "Irrigated plains" },
        { name: "BPT-5204", duration: "125-130 days", yield_quintal_acre: 23, price_per_quintal: 2400, characteristics: "Long grain aromatic", water_requirement: "High", best_for: "Quality markets" }
      ],
      suitable_lands: ["Low-lying areas", "Water-logged regions", "Alluvial plains", "River deltas"]
    },
    { 
      name: "Wheat", 
      tamil_name: "விள்ளை",
      varieties: [
        { name: "HD-2967", duration: "130-135 days", yield_quintal_acre: 18, price_per_quintal: 2300, characteristics: "Bold seeded high yielding", water_requirement: "Medium", best_for: "Northern plains" },
        { name: "PBW-343", duration: "140-145 days", yield_quintal_acre: 20, price_per_quintal: 2400, characteristics: "Early maturity", water_requirement: "Medium-Low", best_for: "Timely sown areas" }
      ],
      suitable_lands: ["Well-drained areas", "Leveled fields", "Loamy plains", "Semi-arid regions"]
    },
    { name: "Maize", tamil_name: "மக்கள்", varieties: [], suitable_lands: ["Hilly regions", "Rainfed areas"] },
    { name: "Soybean", tamil_name: "சோய்வேன்", varieties: [], suitable_lands: ["Black soil regions", "Well-drained fields"] },
    { name: "Cotton", tamil_name: "கப்பூ", varieties: [], suitable_lands: ["Black cotton soil", "Dry regions"] },
    { name: "Sugarcane", tamil_name: "சுகார்", varieties: [], suitable_lands: ["Fertile plains", "High rainfall areas"] },
    { name: "Groundnut", tamil_name: "முன்றூ", varieties: [], suitable_lands: ["Sandy loam", "Coastal regions"] },
    { name: "Mustard", tamil_name: "சரசு", varieties: [], suitable_lands: ["Loamy soil", "Cool climate regions"] },
    { name: "Chickpea", tamil_name: "சன்னி", varieties: [], suitable_lands: ["Black soil", "Dry farming areas"] },
    { name: "Potato", tamil_name: "உருளைக்கிழங்கு", varieties: [], suitable_lands: ["Cool climates", "Well-drained sandy loam"] },
    { name: "Onion", tamil_name: "வெங்காயம்", varieties: [], suitable_lands: ["Well-drained loamy soil", "Moderate rainfall"] },
    { name: "Tomato", tamil_name: "தக்காளி", varieties: [], suitable_lands: ["Warm climate", "Well-drained soil"] },
    { name: "Turmeric", tamil_name: "மஞ்சள்", varieties: [], suitable_lands: ["Hot humid regions", "Well-drained fertile soil"] },
    { name: "Chilli", tamil_name: "மிளகாய்", varieties: [], suitable_lands: ["Warm tropical climate", "Well-drained soil"] },
    { name: "Sunflower", tamil_name: "சூரியகாந்தி", varieties: [], suitable_lands: ["Sunny locations", "Well-drained soil"] }
  ]);
  const [showStateSuggestions, setShowStateSuggestions] = useState(false);
  const [showDistrictSuggestions, setShowDistrictSuggestions] = useState(false);
  const [showMandiSuggestions, setShowMandiSuggestions] = useState(false);
  const [filteredStates, setFilteredStates] = useState([]);
  const [filteredDistricts, setFilteredDistricts] = useState([]);
  const [filteredMandis, setFilteredMandis] = useState([]);
  const stateInputRef = useRef(null);
  const districtInputRef = useRef(null);
  const mandiInputRef = useRef(null);

  const [formData, setFormData] = useState({
    land_area_acres: user?.land_size_acres || '',
    soil_type: '',
    soil_ph: '6.5',
    nitrogen: '150',
    phosphorus: '50',
    potassium: '100',
    state: user?.state || '',
    district: user?.district || '',
    season: '',
    rainfall_mm: '800',
    temperature_c: '28',
    humidity_percent: '60',
    budget_inr: '',
    crop_preference: 'auto',
    crop_variety: '',
    nearest_mandi: '',
    sowing_date: '',
  });

  const [selectedCropDetails, setSelectedCropDetails] = useState(null);
  const [cropVarieties, setCropVarieties] = useState([]);
  
  // Soil image analysis state
  const [soilImage, setSoilImage] = useState(null);
  const [soilImagePreview, setSoilImagePreview] = useState(null);
  const [analyzingSoil, setAnalyzingSoil] = useState(false);
  const [soilAnalysisResult, setSoilAnalysisResult] = useState(null);

  const soilTypes = [
    'Alluvial', 'Black Soil', 'Red Soil', 'Laterite Soil',
    'Sandy', 'Sandy Loam', 'Loamy', 'Clay', 'Clay Loam'
  ];

  const seasons = ['Kharif(June to October)', 'Rabi(October to March)', 'Zaid(March to June)'];

  useEffect(() => {
    loadData();
  }, []);

  const handleStateChange = (value) => {
    setFormData({ ...formData, state: value });
    setError('');
    
    // Filter states based on input
    if (value.trim()) {
      const filtered = states.filter(state => 
        state.name.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredStates(filtered);
      setShowStateSuggestions(true);
    } else {
      setShowStateSuggestions(false);
    }
    
    // Reset districts when state changes
    setFormData(prev => ({ ...prev, district: '' }));
    setDistricts([]);
  };
  
  const handleDistrictChange = (value) => {
    setFormData({ ...formData, district: value });
    setError('');
    
    // Filter districts based on input
    if (value.trim() && formData.state) {
      const selectedState = states.find(s => s.name === formData.state);
      if (selectedState) {
        const filtered = selectedState.districts.filter(district => 
          district.toLowerCase().includes(value.toLowerCase())
        );
        setFilteredDistricts(filtered);
        setShowDistrictSuggestions(true);
      }
    } else {
      setShowDistrictSuggestions(false);
    }
  };
  
  const handleSelectState = (stateName) => {
    setFormData({ ...formData, state: stateName });
    setShowStateSuggestions(false);
    setError(''); // Clear error when user selects a valid state
    
    // Load districts for selected state
    const selectedState = states.find(s => s.name === stateName);
    setDistricts(selectedState?.districts || []);
    setFormData(prev => ({ ...prev, district: '' }));
  };
  
  const handleSelectDistrict = (districtName) => {
    setFormData({ ...formData, district: districtName });
    setShowDistrictSuggestions(false);
    setError(''); // Clear error when user selects a valid district
  };
  
  const handleClickOutside = (event) => {
    if (stateInputRef.current && !stateInputRef.current.contains(event.target)) {
      setShowStateSuggestions(false);
    }
    if (districtInputRef.current && !districtInputRef.current.contains(event.target)) {
      setShowDistrictSuggestions(false);
    }
    if (mandiInputRef.current && !mandiInputRef.current.contains(event.target)) {
      setShowMandiSuggestions(false);
    }
  };
  
  // Major mandis in India
  const majorMandis = [
    "Ahmednagar APMC",
    "Amritsar APMC",
    "Bangalore APMC",
    "Bhopal APMC",
    "Chandigarh APMC",
    "Chennai APMC",
    "Coimbatore APMC",
    "Delhi APMC",
    "Guntur APMC",
    "Guwahati APMC",
    "Hyderabad APMC",
    "Indore APMC",
    "Jaipur APMC",
    "Jalandhar APMC",
    "Kolkata APMC",
    "Lucknow APMC",
    "Mumbai APMC",
    "Nagpur APMC",
    "Nashik APMC",
    "Patna APMC",
    "Pune APMC",
    "Raipur APMC",
    "Ranchi APMC",
    "Surat APMC",
    "Vadodara APMC",
    "Varanasi APMC"
  ];
  
  const handleMandiChange = (value) => {
    setFormData({ ...formData, nearest_mandi: value });
    setError('');
    
    // Filter mandis based on input
    if (value.trim()) {
      const filtered = majorMandis.filter(mandi => 
        mandi.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredMandis(filtered);
      setShowMandiSuggestions(true);
    } else {
      setShowMandiSuggestions(false);
    }
  };
  
  const handleSelectMandi = (mandiName) => {
    setFormData({ ...formData, nearest_mandi: mandiName });
    setShowMandiSuggestions(false);
    setError('');
  };
  
  const handleMandiFocus = () => {
    if (formData.nearest_mandi) {
      const filtered = majorMandis.filter(mandi => 
        mandi.toLowerCase().includes(formData.nearest_mandi.toLowerCase())
      );
      setFilteredMandis(filtered);
      setShowMandiSuggestions(true);
    }
  };
  
  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const loadData = async () => {
    try {
      const [statesRes, cropsRes] = await Promise.all([
        dataAPI.getStates(),
        dataAPI.getCrops()
      ]);
      setStates(statesRes.data);
      
      // Only update crops if API returns data with varieties and suitable_lands
      if (cropsRes.data && cropsRes.data.crops && cropsRes.data.crops.length > 0) {
        // Ensure all crops have varieties and suitable_lands arrays
        const enrichedCrops = cropsRes.data.crops.map(crop => ({
          ...crop,
          varieties: crop.varieties || [],
          suitable_lands: crop.suitable_lands || []
        }));
        setCrops(enrichedCrops);
      }

      if (user?.state) {
        const selectedState = statesRes.data.find(s => s.name === user.state);
        setDistricts(selectedState?.districts || []);
        // Update form data to include user's district if not already set
        if (!formData.district && user.district) {
          setFormData(prev => ({ ...prev, district: user.district }));
        }
      }
    } catch (err) {
      console.error('Failed to load data from API, using fallback data');
      // Keep the fallback crops and try to load states only
      try {
        const statesRes = await dataAPI.getStates();
        setStates(statesRes.data);
        
        if (user?.state) {
          const selectedState = statesRes.data.find(s => s.name === user.state);
          setDistricts(selectedState?.districts || []);
          if (!formData.district && user.district) {
            setFormData(prev => ({ ...prev, district: user.district }));
          }
        }
      } catch (statesErr) {
        console.error('Failed to load states:', statesErr);
      }
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    // Don't handle state and district here as they are handled by auto-suggest functions
    if (name !== 'state' && name !== 'district') {
      setFormData({ ...formData, [name]: value });
      setError('');
      
      // If crop preference changed, update crop details and varieties
      if (name === 'crop_preference' && value !== 'auto') {
        const selectedCrop = crops.find(c => c.name === value);
        if (selectedCrop) {
          setSelectedCropDetails(selectedCrop);
          // Ensure varieties array exists
          const varieties = selectedCrop.varieties || [];
          setCropVarieties(varieties);
          console.log(`Selected crop: ${value}, Varieties found:`, varieties);
          // Reset variety selection when crop changes
          setFormData(prev => ({ ...prev, crop_variety: '' }));
        } else {
          console.warn(`Crop "${value}" not found in crops list`);
        }
      }
    }
  };

  // Soil image analysis functions
  const handleSoilImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file');
      return;
    }
    
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('Image size must be less than 10MB');
      return;
    }
    
    setSoilImage(file);
    
    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setSoilImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
    
    // Analyze soil image
    await analyzeSoilImage(file);
  };

  const analyzeSoilImage = async (file) => {
    setAnalyzingSoil(true);
    setError('');
    
    try {
      const formDataImg = new FormData();
      formDataImg.append('image', file);
      
      // Get token from localStorage - use 'access_token' key (set by AuthContext)
      const token = localStorage.getItem('access_token');
      console.log('Soil analysis - Token:', token ? 'Present' : 'Missing');
      
      if (!token) {
        setError('Authentication required. Please login again.');
        setAnalyzingSoil(false);
        return;
      }
      
      // Call backend API for soil image analysis
      const response = await fetch('http://localhost:8001/api/soil/analyze-image', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formDataImg
      });
      
      console.log('Soil analysis response status:', response.status);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Backend error:', errorData);
        throw new Error(`Analysis failed: ${errorData.detail || 'Unknown error'}`);
      }
      
      const result = await response.json();
      console.log('Soil analysis result:', result);
      
      if (result.success && result.data) {
        setSoilAnalysisResult(result.data);
        
        // Auto-fill form with analyzed results - format to 2 decimal places
        setFormData(prev => ({
          ...prev,
          soil_type: result.data.soil_type || prev.soil_type,
          soil_ph: parseFloat(result.data.soil_ph || 0).toFixed(2),
          nitrogen: parseFloat(result.data.nitrogen || 0).toFixed(2),
          phosphorus: parseFloat(result.data.phosphorus || 0).toFixed(2),
          potassium: parseFloat(result.data.potassium || 0).toFixed(2)
        }));
        
        alert('✅ Soil image analyzed successfully! Form auto-filled with results.');
      } else {
        throw new Error('Invalid response format from server');
      }
    } catch (err) {
      console.error('Soil image analysis error:', err);
      setError(`Failed to analyze soil image: ${err.message}. Please fill manually.`);
    } finally {
      setAnalyzingSoil(false);
    }
  };

  const removeSoilImage = () => {
    setSoilImage(null);
    setSoilImagePreview(null);
    setSoilAnalysisResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // More lenient validation - check if state and district are not empty
    if (!formData.state.trim()) {
      setError('Please select a state');
      return;
    }
    
    if (!formData.district.trim()) {
      setError('Please select a district');
      return;
    }
    
    // Check if the selected state and district exist in our data
    const selectedState = states.find(s => s.name.toLowerCase() === formData.state.toLowerCase().trim());
    
    if (!selectedState) {
      setError('Please select a valid state from the suggestions');
      return;
    }
    
    const isValidDistrict = selectedState.districts.some(d => 
      d.toLowerCase() === formData.district.toLowerCase().trim()
    );
    
    if (!isValidDistrict) {
      setError('Please select a valid district from the suggestions');
      return;
    }
    
    setLoading(true);
    setError('');

    try {
      const analysisData = {
        ...formData,
        land_area_acres: parseFloat(formData.land_area_acres),
        // Preserve 2 decimal precision for soil values
        soil_ph: parseFloat(parseFloat(formData.soil_ph).toFixed(2)),
        nitrogen: parseFloat(parseFloat(formData.nitrogen).toFixed(2)),
        phosphorus: parseFloat(parseFloat(formData.phosphorus).toFixed(2)),
        potassium: parseFloat(parseFloat(formData.potassium).toFixed(2)),
        rainfall_mm: parseFloat(formData.rainfall_mm),
        temperature_c: parseFloat(formData.temperature_c),
        humidity_percent: parseFloat(formData.humidity_percent),
        budget_inr: parseFloat(formData.budget_inr),
      };

      const response = await analysisAPI.analyze(analysisData);
      navigate(`/results/${response.data.analysis_id}`, { state: { results: response.data } });
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    }

    setLoading(false);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto pb-12"
    >
      <div className="mb-10 text-center">
        <h1 className="text-4xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-primary-700 to-primary-500 tracking-tight">Get Recommendation</h1>
        <p className="text-gray-500 mt-3 font-medium text-lg">Provide your land and crop details for precision recommendations</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Land Details */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
          className="glass rounded-3xl p-8 shadow-sm"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-8 flex items-center border-b border-black/5 pb-4">
            <span className="bg-primary-100 text-primary-600 p-2.5 rounded-2xl mr-4 shadow-sm">
              <Sprout className="w-6 h-6" />
            </span>
            Land Details
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Land Area (Acres) *</label>
              <input
                type="number"
                name="land_area_acres"
                value={formData.land_area_acres}
                onChange={handleChange}
                className="input-field"
                step="0.1"
                min="0.1"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Soil Type *</label>
              <select name="soil_type" value={formData.soil_type} onChange={handleChange} className="input-field" required>
                <option value="">Select Soil Type</option>
                {soilTypes.map(soil => (
                  <option key={soil} value={soil}>{soil}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Soil pH *</label>
              <input
                type="number"
                name="soil_ph"
                value={formData.soil_ph}
                onChange={handleChange}
                className="input-field"
                step="0.01"  // Allow 2 decimal places (e.g., 7.45)
                min="0"
                max="14"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Budget (Rs.) *</label>
              <input
                type="number"
                name="budget_inr"
                value={formData.budget_inr}
                onChange={handleChange}
                className="input-field"
                min="1000"
                required
              />
            </div>
          </div>
        </motion.div>

        {/* Soil Nutrients */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
          className="glass rounded-3xl p-8 shadow-sm"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-8 flex items-center border-b border-black/5 pb-4">
            <span className="bg-orange-100 text-orange-600 p-2.5 rounded-2xl mr-4 shadow-sm">
              <TestTube className="w-6 h-6" />
            </span>
            Soil Nutrients (kg/ha)
          </h2>
          
          {/* Soil Image Upload Section */}
          <div className="mb-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-800 flex items-center">
                <ImageIcon className="w-5 h-5 mr-2 text-blue-600" />
                AI Soil Analysis from Image
              </h3>
              {soilAnalysisResult && (
                <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
                  ✓ Analyzed
                </span>
              )}
            </div>
            
            <p className="text-sm text-gray-600 mb-4">
              Upload a soil image to automatically detect soil type and NPK values 
            </p>
            
            {!soilImage ? (
              <label className="block w-full">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleSoilImageUpload}
                  className="hidden"
                />
                <div className="border-2 border-dashed border-blue-300 rounded-xl p-8 text-center hover:border-blue-500 transition-colors cursor-pointer bg-white">
                  <Upload className="w-12 h-12 mx-auto text-blue-400 mb-3" />
                  <p className="text-sm font-medium text-gray-700 mb-1">Click to upload soil image</p>
                  <p className="text-xs text-gray-500">JPG, PNG (Max 10MB)</p>
                </div>
              </label>
            ) : (
              <div className="bg-white rounded-xl p-4 border border-blue-200">
                <div className="flex items-start space-x-4">
                  {soilImagePreview && (
                    <img 
                      src={soilImagePreview} 
                      alt="Soil sample" 
                      className="w-24 h-24 object-cover rounded-lg border border-gray-300"
                    />
                  )}
                  <div className="flex-1">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <p className="font-medium text-gray-800">{soilImage.name}</p>
                        <p className="text-xs text-gray-500">{(soilImage.size / 1024 / 1024).toFixed(2)} MB</p>
                      </div>
                      <button
                        onClick={removeSoilImage}
                        className="text-red-500 hover:text-red-700 text-sm font-medium"
                      >
                        Remove
                      </button>
                    </div>
                    
                    {analyzingSoil ? (
                      <div className="flex items-center text-blue-600">
                        <Loader2 className="w-4 h-4 animate-spin mr-2" />
                        <span className="text-sm">Analyzing soil image...</span>
                      </div>
                    ) : soilAnalysisResult ? (
                      <div className="mt-3 bg-green-50 rounded-lg p-3 border border-green-200">
                        <p className="text-xs font-semibold text-green-800 mb-2">Analysis Results:</p>
                        <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs">
                          <div className="bg-white p-2 rounded border border-green-200">
                            <p className="text-gray-500">Type</p>
                            <p className="font-semibold text-gray-800">{soilAnalysisResult.soil_type}</p>
                          </div>
                          <div className="bg-white p-2 rounded border border-green-200">
                            <p className="text-gray-500">pH</p>
                            <p className="font-semibold text-gray-800">{soilAnalysisResult.soil_ph}</p>
                          </div>
                          <div className="bg-white p-2 rounded border border-green-200">
                            <p className="text-gray-500">Nitrogen</p>
                            <p className="font-semibold text-gray-800">{soilAnalysisResult.nitrogen} kg/ha</p>
                          </div>
                          <div className="bg-white p-2 rounded border border-green-200">
                            <p className="text-gray-500">Phosphorus</p>
                            <p className="font-semibold text-gray-800">{soilAnalysisResult.phosphorus} kg/ha</p>
                          </div>
                          <div className="bg-white p-2 rounded border border-green-200">
                            <p className="text-gray-500">Potassium</p>
                            <p className="font-semibold text-gray-800">{soilAnalysisResult.potassium} kg/ha</p>
                          </div>
                        </div>
                        <p className="text-xs text-gray-500 mt-2">
                          Values auto-filled in form below ✓
                        </p>
                      </div>
                    ) : null}
                  </div>
                </div>
              </div>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nitrogen (N)</label>
              <input
                type="number"
                name="nitrogen"
                value={formData.nitrogen}
                onChange={handleChange}
                className="input-field"
                step="0.01"  // Allow 2 decimal places
                min="0"
                max="500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Phosphorus (P)</label>
              <input
                type="number"
                name="phosphorus"
                value={formData.phosphorus}
                onChange={handleChange}
                className="input-field"
                step="0.01"  // Allow 2 decimal places
                min="0"
                max="300"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Potassium (K)</label>
              <input
                type="number"
                name="potassium"
                value={formData.potassium}
                onChange={handleChange}
                className="input-field"
                step="0.01"  // Allow 2 decimal places
                min="0"
                max="600"
              />
            </div>
          </div>
        </motion.div>

        {/* Location & Climate */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
          className="glass rounded-3xl p-8 shadow-sm"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-8 flex items-center border-b border-black/5 pb-4">
            <span className="bg-blue-100 text-blue-600 p-2.5 rounded-2xl mr-4 shadow-sm">
              <Map className="w-6 h-6" />
            </span>
            Location & Climate
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="relative">
              <label className="block text-sm font-medium text-gray-700 mb-1">State *</label>
              <p className="text-xs text-gray-500 mb-1">Start typing and select from the dropdown list</p>
              <div ref={stateInputRef} className="relative">
                <input
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={(e) => handleStateChange(e.target.value)}
                  onBlur={() => {
                    // Validate state selection when user leaves the field
                    if (formData.state.trim() && !states.some(s => s.name.toLowerCase() === formData.state.toLowerCase().trim())) {
                      setError('Please select a valid state from the suggestions');
                    }
                  }}
                  onFocus={() => {
                    if (formData.state) {
                      const filtered = states.filter(state => 
                        state.name.toLowerCase().includes(formData.state.toLowerCase())
                      );
                      setFilteredStates(filtered);
                      setShowStateSuggestions(true);
                    }
                  }}
                  className="input-field w-full"
                  placeholder="Type to search state"
                  required
                />
                {showStateSuggestions && filteredStates.length > 0 && (
                  <div className="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    {filteredStates.map((state) => (
                      <div
                        key={state.code}
                        className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                        onClick={() => handleSelectState(state.name)}
                      >
                        {state.name}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
            <div className="relative">
              <label className="block text-sm font-medium text-gray-700 mb-1">District *</label>
              <p className="text-xs text-gray-500 mb-1">Select state first, then start typing and select district from dropdown</p>
              <div ref={districtInputRef} className="relative">
                <input
                  type="text"
                  name="district"
                  value={formData.district}
                  onChange={(e) => handleDistrictChange(e.target.value)}
                  onBlur={() => {
                    // Validate district selection when user leaves the field
                    if (formData.district.trim() && formData.state.trim() && districts.length > 0) {
                      const isValidDistrict = districts.some(d => 
                        d.toLowerCase() === formData.district.toLowerCase().trim()
                      );
                      if (!isValidDistrict) {
                        setError('Please select a valid district from the suggestions');
                      }
                    }
                  }}
                  onFocus={() => {
                    if (formData.district && formData.state && districts.length > 0) {
                      const filtered = districts.filter(district => 
                        district.toLowerCase().includes(formData.district.toLowerCase())
                      );
                      setFilteredDistricts(filtered);
                      setShowDistrictSuggestions(true);
                    }
                  }}
                  className="input-field w-full"
                  placeholder="Type to search district"
                  required
                  disabled={!formData.state}
                />
                {showDistrictSuggestions && filteredDistricts.length > 0 && (
                  <div className="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    {filteredDistricts.map((district) => (
                      <div
                        key={district}
                        className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                        onClick={() => handleSelectDistrict(district)}
                      >
                        {district}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Season *</label>
              <select name="season" value={formData.season} onChange={handleChange} className="input-field" required>
                <option value="">Select Season</option>
                {seasons.map(season => (
                  <option key={season} value={season}>{season}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Expected Rainfall (mm)</label>
              <input
                type="number"
                name="rainfall_mm"
                value={formData.rainfall_mm}
                onChange={handleChange}
                className="input-field"
                min="0"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Temperature (C)</label>
              <input
                type="number"
                name="temperature_c"
                value={formData.temperature_c}
                onChange={handleChange}
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Humidity (%)</label>
              <input
                type="number"
                name="humidity_percent"
                value={formData.humidity_percent}
                onChange={handleChange}
                className="input-field"
                min="0"
                max="100"
              />
            </div>
          </div>
        </motion.div>

        {/* Crop Preference */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
          className="glass rounded-3xl p-8 shadow-sm"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-8 flex items-center border-b border-black/5 pb-4">
            <span className="bg-purple-100 text-purple-600 p-2.5 rounded-2xl mr-4 shadow-sm">
              <MapPin className="w-6 h-6" />
            </span>
            Crop Preference
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Crop Selection</label>
              <select name="crop_preference" value={formData.crop_preference} onChange={handleChange} className="input-field">
                <option value="auto">Auto Recommend (Best Crop)</option>
                {crops.map(crop => (
                  <option key={crop.name} value={crop.name}>{crop.name} ({crop.tamil_name})</option>
                ))}
              </select>
            </div>
            
            {/* Crop Varieties - Show when a specific crop is selected */}
            {formData.crop_preference !== 'auto' && cropVarieties.length > 0 && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Variety <span className="text-gray-500 text-xs">(Optional)</span></label>
                <select 
                  name="crop_variety" 
                  value={formData.crop_variety} 
                  onChange={handleChange} 
                  className="input-field"
                >
                  <option value="">Auto Select Best Variety</option>
                  {cropVarieties.map(variety => (
                    <option key={variety.name} value={variety.name}>
                      {variety.name} - {variety.duration} days
                    </option>
                  ))}
                </select>
              </div>
            )}
            
            <div className="relative">
              <label className="block text-sm font-medium text-gray-700 mb-1">Nearest Mandi</label>
              <p className="text-xs text-gray-500 mb-1">Start typing to see major mandi suggestions</p>
              <div ref={mandiInputRef} className="relative">
                <input
                  type="text"
                  name="nearest_mandi"
                  value={formData.nearest_mandi}
                  onChange={(e) => handleMandiChange(e.target.value)}
                  onFocus={handleMandiFocus}
                  className="input-field w-full"
                  placeholder="e.g., Pune APMC"
                />
                {showMandiSuggestions && filteredMandis.length > 0 && (
                  <div className="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    {filteredMandis.map((mandi, index) => (
                      <div
                        key={index}
                        className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                        onClick={() => handleSelectMandi(mandi)}
                      >
                        {mandi}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Expected Sowing Date</label>
              <input
                type="date"
                name="sowing_date"
                value={formData.sowing_date}
                onChange={handleChange}
                className="input-field"
              />
            </div>
          </div>

          {/* Land Suitability Information */}
          {selectedCropDetails && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-base font-semibold text-gray-800 mb-4">Suitable Lands for {selectedCropDetails.name}</h3>
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="flex items-start">
                  <svg className="w-5 h-5 text-blue-600 mr-3 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zm-11-1a1 1 0 11-2 0 1 1 0 012 0z" clipRule="evenodd" />
                  </svg>
                  <div className="flex-1">
                    <p className="text-sm text-gray-700 mb-2">
                      <span className="font-semibold">Suitable Lands:</span>
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {selectedCropDetails.suitable_lands && selectedCropDetails.suitable_lands.length > 0 ? (
                        selectedCropDetails.suitable_lands.map((land, idx) => (
                          <span key={idx} className="inline-block bg-blue-200 text-blue-800 px-3 py-1 rounded-full text-xs font-medium">
                            {land}
                          </span>
                        ))
                      ) : (
                        <p className="text-xs text-gray-600">No specific land information available</p>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Variety Details */}
              {formData.crop_variety && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <h4 className="font-semibold text-gray-800 mb-3">Selected Variety: {formData.crop_variety}</h4>
                  {cropVarieties.find(v => v.name === formData.crop_variety) && (
                    <div className="bg-green-50 rounded-lg p-4 space-y-3">
                      {(() => {
                        const variety = cropVarieties.find(v => v.name === formData.crop_variety);
                        return (
                          <>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                              <div className="bg-white p-3 rounded border border-green-200">
                                <p className="text-xs text-gray-500">Duration</p>
                                <p className="font-semibold text-gray-800">{variety.duration} days</p>
                              </div>
                              <div className="bg-white p-3 rounded border border-green-200">
                                <p className="text-xs text-gray-500">Expected Yield</p>
                                <p className="font-semibold text-gray-800">{variety.yield_quintal_acre} q/acre</p>
                              </div>
                              <div className="bg-white p-3 rounded border border-green-200">
                                <p className="text-xs text-gray-500">Expected Price</p>
                                <p className="font-semibold text-gray-800">₹{variety.price_per_quintal}</p>
                              </div>
                              <div className="bg-white p-3 rounded border border-green-200">
                                <p className="text-xs text-gray-500">Water Need</p>
                                <p className="font-semibold text-gray-800">{variety.water_requirement}</p>
                              </div>
                            </div>
                            <div className="bg-white p-3 rounded border border-green-200">
                              <p className="text-xs text-gray-500 mb-1">Characteristics</p>
                              <p className="text-sm text-gray-700">{variety.characteristics}</p>
                            </div>
                            <div className="bg-white p-3 rounded border border-green-200">
                              <p className="text-xs text-gray-500 mb-1">Best For</p>
                              <p className="text-sm text-gray-700">{variety.best_for}</p>
                            </div>
                          </>
                        );
                      })()}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </motion.div>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-700 hover:to-primary-600 text-white py-5 text-xl font-bold flex items-center justify-center space-x-3 rounded-2xl shadow-xl shadow-primary-500/30 overflow-hidden relative group"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin h-6 w-6 text-white" />
              <span>Analyzing Details...</span>
            </>
          ) : (
            <>
              <span className="relative z-10 tracking-wide">Get Analysis & Recommendations</span>
              <ArrowRight className="w-6 h-6 relative z-10 transform group-hover:translate-x-2 transition-transform" />
              <div className="absolute inset-0 bg-white/10 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-in-out"></div>
            </>
          )}
        </motion.button>
      </form>
    </motion.div>
  );
};

export default GetRecommendation;
