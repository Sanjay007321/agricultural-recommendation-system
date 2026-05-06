import { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { dataAPI } from "../services/api";
import agricultureBg from "../components/Agriculture-in-India-1.jpeg";
import Logo from "../components/Logo";
import { motion } from "framer-motion";
import { ArrowRight, Loader2, CheckCircle2 } from "lucide-react";
const Register = () => {
  const [formData, setFormData] = useState({
    full_name: "",
    mobile: "",
    aadhar_number: "",
    password: "",
    confirmPassword: "",
    state: "",
    district: "",
    village: "",
    land_size_acres: "",
  });
  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [showStateSuggestions, setShowStateSuggestions] = useState(false);
  const [showDistrictSuggestions, setShowDistrictSuggestions] = useState(false);
  const [filteredStates, setFilteredStates] = useState([]);
  const [filteredDistricts, setFilteredDistricts] = useState([]);
  const stateInputRef = useRef(null);
  const districtInputRef = useRef(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [farmerId, setFarmerId] = useState("");
  const { register } = useAuth();
  const navigate = useNavigate();

  const validateStateAndDistrict = (stateName, districtName) => {
    if (!stateName || !districtName) return false;

    console.log("Validating state:", stateName, "district:", districtName);
    console.log("Available states count:", states.length);

    // Find the state in the loaded states array (case-insensitive)
    const foundState = states.find(
      (s) => s.name.toLowerCase().trim() === stateName.toLowerCase().trim(),
    );

    if (!foundState) {
      console.log("State not found:", stateName);
      console.log(
        "Available states:",
        states.map((s) => s.name),
      );
      return false;
    }

    console.log("Found state:", foundState.name);
    console.log("Available districts in state:", foundState.districts);

    // Check if district exists in the state's districts (case-insensitive)
    // Also allow partial matches to be more user-friendly
    const foundDistrict = foundState.districts.some(
      (d) => d.toLowerCase().trim() === districtName.toLowerCase().trim(),
    );

    if (!foundDistrict) {
      console.log(
        "District not found in state:",
        districtName,
        "in",
        stateName,
      );
      console.log("Available districts:", foundState.districts);
      return false;
    }

    console.log("Validation passed");
    return true;
  };

  useEffect(() => {
    console.log("=== REGISTRATION COMPONENT MOUNTED ===");
    console.log("Initial states:", states);
    console.log("Initial districts:", districts);
    loadStates();
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const loadStates = async () => {
    try {
      console.log("Loading states...");
      const response = await dataAPI.getStates();
      console.log("States API response:", response);
      console.log("States data:", response.data);
      console.log("States count:", response.data.length);
      setStates(response.data);
      console.log("States state updated, count:", response.data.length);
    } catch (err) {
      console.error("Failed to load states:", err);
      console.error("Error details:", err.response?.data || err.message);
    }
  };

  const handleStateChange = (value) => {
    console.log("=== HANDLE STATE CHANGE ===");
    console.log("Input value:", value);
    console.log("Current states:", states);
    console.log("Current states count:", states.length);

    setFormData({ ...formData, state: value });
    setError("");

    // Filter states based on input
    if (value.trim()) {
      const filtered = states.filter((state) =>
        state.name.toLowerCase().includes(value.toLowerCase()),
      );
      console.log("Filtered states:", filtered);
      setFilteredStates(filtered);
      setShowStateSuggestions(true);
    } else {
      setShowStateSuggestions(false);
    }

    // Reset districts when state changes
    setFormData((prev) => ({ ...prev, district: "" }));
    setDistricts([]);
  };

  const handleSelectState = (stateName) => {
    console.log("=== HANDLE SELECT STATE ===");
    console.log("Selected state:", stateName);
    console.log("Available states:", states);

    setFormData({ ...formData, state: stateName, district: "" });
    setShowStateSuggestions(false);
    setError("");

    // Find the selected state
    const selectedState = states.find(
      (s) => s.name.toLowerCase().trim() === stateName.toLowerCase().trim(),
    );

    console.log("Found state object:", selectedState);

    if (selectedState) {
      const stateDistricts = selectedState.districts || [];
      console.log("Districts for selected state:", stateDistricts);
      setDistricts(stateDistricts);
      setFilteredDistricts([...stateDistricts]);
      setShowDistrictSuggestions(true);
    } else {
      console.log("State not found in data");
      setDistricts([]);
      setFilteredDistricts([]);
    }
  };

  const handleDistrictChange = (value) => {
    console.log("=== HANDLE DISTRICT CHANGE ===");
    console.log("Input value:", value);
    console.log("Current form state:", formData.state);
    console.log("Available districts:", districts);
    console.log("Districts count:", districts.length);

    setFormData({ ...formData, district: value });
    setError("");

    // Filter districts based on input
    if (value.trim() && formData.state && districts.length > 0) {
      const filtered = districts.filter((district) =>
        district.toLowerCase().includes(value.toLowerCase()),
      );
      console.log("Filtered districts:", filtered);
      setFilteredDistricts(filtered);
      setShowDistrictSuggestions(true);
    } else if (value.trim() && !formData.state) {
      // Show hint if user tries to type district before selecting state
      setError("Please select a state first before typing the district name");
      setShowDistrictSuggestions(false);
    } else if (value.trim() === "" && formData.state && districts.length > 0) {
      // Show all districts when input is cleared but state is selected
      setFilteredDistricts([...districts]);
      setShowDistrictSuggestions(true);
    } else {
      setShowDistrictSuggestions(false);
    }
  };

  const handleSelectDistrict = (districtName) => {
    setFormData({ ...formData, district: districtName });
    setShowDistrictSuggestions(false);
    setError("");
  };

  const handleClickOutside = (event) => {
    if (
      stateInputRef.current &&
      !stateInputRef.current.contains(event.target)
    ) {
      setShowStateSuggestions(false);
    }
    if (
      districtInputRef.current &&
      !districtInputRef.current.contains(event.target)
    ) {
      setShowDistrictSuggestions(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log("=== REGISTRATION ATTEMPT ===");
    console.log("Form Data:", {
      full_name: formData.full_name.trim(),
      mobile: formData.mobile.trim(),
      aadhar_number: formData.aadhar_number,
      password: formData.password,
      state: formData.state.trim(),
      district: formData.district.trim(),
      village: formData.village ? formData.village.trim() : null,
      land_size_acres: formData.land_size_acres
        ? parseFloat(formData.land_size_acres)
        : null,
    });

    // Validate form data
    if (!formData.full_name.trim()) {
      setError("Full name is required");
      return;
    }

    if (!formData.mobile.trim()) {
      setError("Mobile number is required");
      return;
    }

    if (formData.mobile.length !== 10 || isNaN(formData.mobile)) {
      setError("Mobile number must be 10 digits");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    // Validate Aadhar number if provided
    if (formData.aadhar_number && formData.aadhar_number.length !== 12) {
      setError("Aadhar number must be 12 digits");
      return;
    }

    if (!formData.state.trim()) {
      setError("State is required");
      return;
    }

    if (!formData.district.trim()) {
      setError("District is required");
      return;
    }

    // Validate that state and district are valid
    const isValidLocation = validateStateAndDistrict(
      formData.state.trim(),
      formData.district.trim(),
    );
    console.log("State/District validation result:", isValidLocation);
    if (!isValidLocation) {
      setError(
        "Please select a valid state and district from the suggestions. Start typing, then click on the matching option from the dropdown list. You must select from the suggestions, not just type freely.",
      );
      return;
    }

    setLoading(true);
    setError("");

    const registerData = {
      full_name: formData.full_name.trim(),
      mobile: formData.mobile.trim(),
      aadhar_number: formData.aadhar_number || null,
      password: formData.password,
      state: formData.state.trim(),
      district: formData.district.trim(),
      village: formData.village ? formData.village.trim() : null,
      land_size_acres: formData.land_size_acres
        ? parseFloat(formData.land_size_acres)
        : null,
    };

    console.log("Sending registration data:", registerData);

    try {
      const result = await register(registerData);
      console.log("Registration result:", result);

      if (result.success) {
        setFarmerId(result.farmer_id);
        setTimeout(() => navigate("/dashboard"), 2000);
      } else {
        // Check for specific error messages from backend
        if (result.error.includes("Mobile number already registered")) {
          setError(
            "This mobile number is already registered. Please try logging in instead or use a different mobile number.",
          );
        } else if (result.error.includes("Aadhar number already registered")) {
          setError(
            "This Aadhar number is already registered. Please try logging in instead or use a different Aadhar number.",
          );
        } else {
          setError(result.error || "Registration failed. Please try again.");
        }
      }
    } catch (err) {
      console.error("Registration error:", err);
      // Check for specific error messages
      if (
        err.message &&
        err.message.includes("Mobile number already registered")
      ) {
        setError(
          "This mobile number is already registered. Please try logging in instead or use a different mobile number.",
        );
      } else if (
        err.message &&
        err.message.includes("Aadhar number already registered")
      ) {
        setError(
          "This Aadhar number is already registered. Please try logging in instead or use a different Aadhar number.",
        );
      } else {
        setError(
          "An unexpected error occurred. Please try again with a different mobile number if the problem persists.",
        );
      }
    }

    setLoading(false);
  };

  if (farmerId) {
    return (
      <div className="min-h-screen relative flex items-center justify-center p-4 overflow-hidden">
        <div className="absolute inset-0 bg-primary-900">
          <div className="absolute inset-0 opacity-20 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCI+Cjwvc3ZnPg==')]"></div>
        </div>
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass rounded-3xl p-10 max-w-md w-full text-center border border-white/20 shadow-2xl relative z-10"
        >
          <motion.div 
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", delay: 0.2 }}
            className="w-24 h-24 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner border border-white/30"
          >
            <CheckCircle2 className="w-12 h-12 text-white" />
          </motion.div>
          <h2 className="text-3xl font-bold text-white mb-2 tracking-tight">
            Registration Successful!
          </h2>
          <p className="text-primary-100 mb-6 font-medium">Your unique Farmer ID is:</p>
          <div className="bg-white/20 backdrop-blur-md border border-white/40 rounded-2xl p-5 mb-6 shadow-inner">
            <p className="text-4xl font-extrabold text-white tracking-widest drop-shadow-md">{farmerId}</p>
          </div>
          <p className="text-sm text-primary-200 font-medium">
            Please save this ID for future reference
          </p>
          <div className="mt-8 flex justify-center">
            <Loader2 className="w-6 h-6 text-primary-200 animate-spin" />
          </div>
          <p className="text-sm text-primary-200 mt-3 font-medium">
            Redirecting to dashboard...
          </p>
        </motion.div>
      </div>
    );
  }

  return (
    <div
      className="min-h-screen flex items-center justify-center p-4 relative py-12"
      style={{
        backgroundImage: `url(${agricultureBg})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundAttachment: "fixed",
      }}
    >
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-3xl relative z-10"
      >
        <div className="text-center mb-8">
          <motion.div 
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ duration: 0.7, type: "spring", bounce: 0.5 }}
            className="w-20 h-20 bg-white/90 backdrop-blur-md rounded-full flex items-center justify-center mx-auto mb-4 shadow-2xl border-[3px] border-white/50"
          >
            <Logo className="w-12 h-12" fill="#16a34a" />
          </motion.div>
          <h1 className="text-4xl font-extrabold text-white drop-shadow-lg tracking-tight">
            ARS System
          </h1>
          <p className="text-primary-100 mt-2 font-medium tracking-wide">Join the Smart Farming Community</p>
        </div>

        <div className="glass rounded-[2.5rem] p-10 shadow-2xl relative overflow-hidden border border-white/60">
          <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-primary-400 via-primary-500 to-primary-600"></div>
          
          <h2 className="text-2xl font-bold text-gray-800 mb-8 text-center flex items-center justify-center gap-2">
            Create Account
          </h2>

          {error && (
            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="bg-red-50/90 backdrop-blur-sm border border-red-200 text-red-600 px-4 py-3 rounded-xl mb-6 shadow-sm">
              <span className="font-medium">{error}</span>
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Full Name *
                </label>
                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      [e.target.name]: e.target.value,
                    })
                  }
                  placeholder="Enter your full name"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Mobile Number *
                </label>
                <input
                  type="text"
                  name="mobile"
                  value={formData.mobile}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      [e.target.name]: e.target.value,
                    })
                  }
                  placeholder="10-digit mobile number"
                  className="input-field"
                  required
                />
                <p className="text-xs text-gray-500 mt-1">
                  Each mobile number can only be used once for registration
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Aadhar Number (Optional)
                </label>
                <input
                  type="text"
                  name="aadhar_number"
                  value={formData.aadhar_number}
                  onChange={(e) => {
                    // Only allow digits and limit to 12 characters
                    const value = e.target.value
                      .replace(/[^0-9]/g, "")
                      .slice(0, 12);
                    setFormData({ ...formData, [e.target.name]: value });
                  }}
                  placeholder="12-digit Aadhar number"
                  className="input-field"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Optional for registration, but recommended for verification
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Password *
                </label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      [e.target.name]: e.target.value,
                    })
                  }
                  placeholder="Minimum 6 characters"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Confirm Password *
                </label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      [e.target.name]: e.target.value,
                    })
                  }
                  placeholder="Re-enter password"
                  className="input-field"
                  required
                />
              </div>

              <div className="relative">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  State *
                </label>
                <p className="text-xs text-gray-500 mb-1">
                  Start typing (e.g., 'Tamil Nadu') then click the matching
                  suggestion from the dropdown
                </p>
                <div ref={stateInputRef} className="relative">
                  <input
                    type="text"
                    value={formData.state}
                    onChange={(e) => handleStateChange(e.target.value)}
                    onBlur={() => {
                      // Validate state selection when user leaves the field (case-insensitive)
                      if (
                        formData.state.trim() &&
                        !states.some(
                          (s) =>
                            s.name.toLowerCase().trim() ===
                            formData.state.toLowerCase().trim(),
                        )
                      ) {
                        setError(
                          "Please select a valid state from the suggestions. Start typing and click on the suggestion that appears in the dropdown list.",
                        );
                      }
                    }}
                    onFocus={() => {
                      console.log("=== STATE INPUT FOCUSED ===");
                      console.log("Current state value:", formData.state);
                      console.log("Available states:", states.length);

                      if (formData.state) {
                        const filtered = states.filter((state) =>
                          state.name
                            .toLowerCase()
                            .includes(formData.state.toLowerCase()),
                        );
                        console.log("Filtered states on focus:", filtered);
                        setFilteredStates(filtered);
                        setShowStateSuggestions(true);
                      }
                    }}
                    className="input-field w-full"
                    placeholder="Type state name and select from suggestions"
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
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  District *
                </label>
                <p className="text-xs text-gray-500 mb-1">
                  Select state first, then start typing and select district from
                  dropdown
                </p>
                <div ref={districtInputRef} className="relative">
                  <input
                    type="text"
                    value={formData.district}
                    onChange={(e) => handleDistrictChange(e.target.value)}
                    onBlur={() => {
                      // Validate district selection when user leaves the field (case-insensitive)
                      if (
                        formData.district.trim() &&
                        formData.state.trim() &&
                        districts.length > 0
                      ) {
                        const isValidDistrict = districts.some(
                          (d) =>
                            d.toLowerCase().trim() ===
                            formData.district.toLowerCase().trim(),
                        );
                        if (!isValidDistrict) {
                          setError(
                            'Please select a valid district from the suggestions. Start typing "Erode" and click on the suggestion that appears in the dropdown list.',
                          );
                        }
                      }
                    }}
                    onFocus={() => {
                      console.log("=== DISTRICT INPUT FOCUSED ===");
                      console.log("Current state:", formData.state);
                      console.log("Available districts:", districts.length);
                      console.log("Districts data:", districts);

                      if (formData.state && districts.length > 0) {
                        setFilteredDistricts([...districts]);
                        setShowDistrictSuggestions(true);
                        console.log("Showing district suggestions");
                      }
                    }}
                    className="input-field w-full"
                    placeholder="Type or click to see all districts"
                    required
                    disabled={!formData.state || districts.length === 0}
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
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Village (Optional)
                </label>
                <input
                  type="text"
                  name="village"
                  value={formData.village}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      [e.target.name]: e.target.value,
                    })
                  }
                  placeholder="Enter village name"
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Land Size (Acres)
                </label>
                <input
                  type="number"
                  name="land_size_acres"
                  value={formData.land_size_acres}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      [e.target.name]: e.target.value,
                    })
                  }
                  placeholder="Total land in acres"
                  className="input-field"
                  step="0.1"
                  min="0"
                />
              </div>
            </div>

            <motion.button
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={loading}
              className="md:col-span-2 w-full bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-700 hover:to-primary-600 text-white py-4 rounded-xl flex items-center justify-center space-x-2 shadow-lg shadow-primary-500/30 overflow-hidden relative group font-bold text-lg mt-4"
            >
              {loading ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : (
                <>
                  <span className="relative z-10">Create Account</span>
                  <ArrowRight className="w-5 h-5 relative z-10 transform group-hover:translate-x-1 transition-transform" />
                  <div className="absolute inset-0 bg-white/10 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                </>
              )}
            </motion.button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-gray-600 font-medium">
              Already have an account?{" "}
              <Link
                to="/login"
                className="text-primary-600 font-bold hover:text-primary-700 transition-colors ml-1 hover:underline"
              >
                Login here
              </Link>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Register;
