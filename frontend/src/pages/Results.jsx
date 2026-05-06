import { useState, useEffect } from "react";
import { useParams, useLocation, Link } from "react-router-dom";
import { analysisAPI } from "../services/api";
import { motion, AnimatePresence } from "framer-motion";
import { generatePDF } from "../utils/reportGenerator";
import { Leaf, TrendingUp, IndianRupee, Target, ChevronRight, Droplets, ArrowRight, Truck, Package, Info, Download, FileText } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const Results = () => {
  const { analysisId } = useParams();
  const location = useLocation();
  const [results, setResults] = useState(location.state?.results || null);
  const [loading, setLoading] = useState(!results);
  const [downloading, setDownloading] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    if (!results) {
      loadResults();
    }
  }, [analysisId]);

  const loadResults = async () => {
    try {
      const response = await analysisAPI.getAnalysisDetail(analysisId);
      setResults(response.data);
    } catch (err) {
      console.error("Failed to load results");
    }
    setLoading(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-[70vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500 shadow-glow"></div>
      </div>
    );
  }

  if (!results) {
    return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col items-center justify-center h-[70vh]">
        <div className="glass p-10 rounded-3xl shadow-soft text-center border border-white/50 max-w-sm mx-auto">
          <Leaf className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Analysis Not Found</h2>
          <p className="text-gray-500 mb-6 font-medium">We couldn't find the results you're looking for.</p>
          <Link to="/analyze" className="btn-primary flex items-center justify-center gap-2 shadow-lg shadow-primary-500/30">
            Start New Analysis <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </motion.div>
    );
  }

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "fertilizer", label: "Fertilizer" },
    { id: "irrigation", label: "Irrigation Planning" },
    { id: "disease", label: "Disease & Pesticide" },
    { id: "logistics", label: "Logistics Recommended" },
    { id: "schemes", label: "Govt Schemes" },
    { id: "profit", label: "Profit Analysis" },
  ];

  const priceData =
    results.price_prediction?.forecast_30_days?.map((price, i) => ({
      day: `Week ${i + 1}`,
      price: price,
    })) || [];

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
      className="space-y-8 pb-12"
    >
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-200/50 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-800 tracking-tight flex items-center gap-3">
            <Target className="w-8 h-8 text-primary-500" />
            Analysis Results
          </h1>
          <p className="text-gray-500 mt-2 font-medium flex items-center gap-2">
            <span className="bg-white border border-gray-200 text-gray-600 px-3 py-1 rounded-lg text-sm tracking-wide shadow-sm">ID: {results.analysis_id?.substring(0,8)}...</span>
          </p>
        </div>
        <Link to="/analyze" className="btn-primary shadow-lg shadow-primary-500/30 flex items-center gap-2 group px-6">
          <span>New Analysis</span>
          <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
        </Link>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <motion.div whileHover={{ y: -5 }} className="glass rounded-3xl p-6 bg-gradient-to-br from-primary-500 to-primary-600 text-white shadow-lg shadow-primary-500/30 relative overflow-hidden">
          <Leaf className="absolute -right-4 -bottom-4 w-24 h-24 opacity-20" />
          <p className="text-primary-100 text-sm font-medium tracking-wide">Recommended Crop</p>
          <p className="text-3xl font-bold mt-2 relative z-10">
            {results.crop_recommendation?.recommended_crop}
          </p>
          <p className="text-primary-100 text-sm mt-3 font-medium bg-white/20 inline-block px-3 py-1 rounded-full backdrop-blur-md">
            Confidence: {(results.crop_recommendation?.confidence * 100).toFixed(0)}%
          </p>
        </motion.div>
        
        <motion.div whileHover={{ y: -5 }} className="glass rounded-3xl p-6 bg-gradient-to-br from-blue-500 to-cyan-500 text-white shadow-lg shadow-blue-500/30 relative overflow-hidden">
          <Droplets className="absolute -right-4 -bottom-4 w-24 h-24 opacity-20" />
          <p className="text-blue-100 text-sm font-medium tracking-wide">Expected Yield</p>
          <p className="text-3xl font-bold mt-2 relative z-10">
            {results.yield_prediction?.total_yield_quintal} Q
          </p>
          <p className="text-blue-100 text-sm mt-3 font-medium bg-white/20 inline-block px-3 py-1 rounded-full backdrop-blur-md">
            {results.yield_prediction?.expected_yield_per_acre} Q/acre
          </p>
        </motion.div>
        
        <motion.div whileHover={{ y: -5 }} className="glass rounded-3xl p-6 bg-gradient-to-br from-orange-400 to-red-500 text-white shadow-lg shadow-orange-500/30 relative overflow-hidden">
          <TrendingUp className="absolute -right-4 -bottom-4 w-24 h-24 opacity-20" />
          <p className="text-orange-100 text-sm font-medium tracking-wide">Predicted Price</p>
          <p className="text-3xl font-bold mt-2 relative z-10">
            Rs. {results.price_prediction?.predicted_price_at_harvest?.toLocaleString("en-IN")}
          </p>
          <p className="text-sm mt-3 font-medium bg-white/20 inline-block px-3 py-1 rounded-full backdrop-blur-md flex items-center gap-1 w-fit">
            {results.price_prediction?.price_trend === "increasing" ? <TrendingUp className="w-4 h-4" /> : null}
            {results.price_prediction?.price_trend}
          </p>
        </motion.div>
        
        <motion.div whileHover={{ y: -5 }} className="glass rounded-3xl p-6 bg-gradient-to-br from-emerald-500 to-green-600 text-white shadow-lg shadow-emerald-500/30 relative overflow-hidden">
          <IndianRupee className="absolute -right-4 -bottom-4 w-24 h-24 opacity-20" />
          <p className="text-emerald-100 text-sm font-medium tracking-wide">Net Profit</p>
          <p className="text-3xl font-bold mt-2 relative z-10">
            Rs. {results.profit_analysis?.net_profit?.toLocaleString("en-IN")}
          </p>
          <p className="text-emerald-100 text-sm mt-3 font-medium bg-white/20 inline-block px-3 py-1 rounded-full backdrop-blur-md">
            ROI: {results.profit_analysis?.roi_percentage}%
          </p>
        </motion.div>
      </div>

      {/* Tabs */}
      <div className="glass rounded-2xl p-2 flex flex-wrap gap-2 shadow-sm border border-white/50 w-full overflow-x-auto custom-scrollbar">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`relative py-3 px-6 text-sm font-bold rounded-xl transition-all duration-300 whitespace-nowrap ${
              activeTab === tab.id
                ? "text-primary-700"
                : "text-gray-500 hover:text-gray-800 hover:bg-white/40"
            }`}
          >
            {activeTab === tab.id && (
               <motion.div layoutId="activetab" className="absolute inset-0 bg-white shadow-sm rounded-xl border border-gray-100" />
            )}
            <span className="relative z-10">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        <motion.div 
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
          className="glass rounded-3xl p-8 border border-white/60 shadow-soft"
        >
        {activeTab === "overview" && (
          <div className="space-y-6">
            <div>
              <h3 className="font-semibold text-gray-800 mb-3">
                Crop Recommendation
              </h3>
              <p className="text-gray-600 mb-4">
                {results.crop_recommendation?.reasoning}
              </p>
              <div className="flex flex-wrap gap-2">
                <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium">
                  {results.crop_recommendation?.recommended_crop}
                </span>
                {results.crop_recommendation?.alternatives?.map((alt, i) => (
                  <span
                    key={i}
                    className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm"
                  >
                    {alt.crop} ({(alt.confidence * 100).toFixed(0)}%)
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-semibold text-gray-800 mb-3">
                Price Forecast (30 Days)
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={priceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`Rs. ${value}`, "Price"]} />
                    <Line
                      type="monotone"
                      dataKey="price"
                      stroke="#16a34a"
                      strokeWidth={2}
                      dot={{ fill: "#16a34a" }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div>
              <h3 className="font-semibold text-gray-800 mb-3">
                Harvest Timeline
              </h3>
              <div className="bg-primary-50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-600">Sowing Date</span>
                  <span className="font-medium">
                    {results.harvest_prediction?.sowing_date}
                  </span>
                </div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-600">Expected Harvest</span>
                  <span className="font-medium">
                    {results.harvest_prediction?.expected_harvest_start} to{" "}
                    {results.harvest_prediction?.expected_harvest_end}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Days to Harvest</span>
                  <span className="font-medium">
                    {results.harvest_prediction?.days_to_harvest} days
                  </span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="font-semibold text-gray-800 mb-3">
                Yield Improvement Tips
              </h3>
              <ul className="space-y-2">
                {results.yield_improvement_tips?.map((tip, i) => (
                  <li key={i} className="flex items-start space-x-2">
                    <svg
                      className="w-5 h-5 text-primary-600 mt-0.5 flex-shrink-0"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    <span className="text-gray-600">{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {activeTab === "fertilizer" && (
          <div>
            <h3 className="font-semibold text-gray-800 mb-4">
              Fertilizer Recommendations
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-500">
                      Fertilizer
                    </th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-500">
                      Quantity (kg/acre)
                    </th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-500">
                      Cost (Rs.)
                    </th>
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-500">
                      Timing
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {results.fertilizer_recommendation?.recommendations?.map(
                    (fert, i) => (
                      <tr key={i} className="border-b">
                        <td className="py-3 px-4 font-medium">{fert.name}</td>
                        <td className="py-3 px-4">
                          {fert.quantity_kg_per_acre}
                        </td>
                        <td className="py-3 px-4">Rs. {fert.cost_inr}</td>
                        <td className="py-3 px-4 text-gray-600">
                          {fert.timing}
                        </td>
                      </tr>
                    ),
                  )}
                </tbody>
                <tfoot>
                  <tr className="bg-gray-50">
                    <td colSpan="2" className="py-3 px-4 font-semibold">
                      Total Cost
                    </td>
                    <td
                      colSpan="2"
                      className="py-3 px-4 font-semibold text-primary-600"
                    >
                      Rs.{" "}
                      {results.fertilizer_recommendation?.total_cost?.toLocaleString(
                        "en-IN",
                      )}
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
        )}

        {activeTab === "irrigation" && (
          <div className="space-y-6">
            {/* Summary Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 rounded-lg p-4">
                <p className="text-gray-600 text-sm">Irrigation Method</p>
                <p className="text-lg font-bold text-blue-600 mt-2">
                  {results.irrigation_planning?.irrigation_method}
                </p>
              </div>
              <div className="bg-cyan-50 rounded-lg p-4">
                <p className="text-gray-600 text-sm">Water Efficiency</p>
                <p className="text-lg font-bold text-cyan-600 mt-2">
                  {results.irrigation_planning?.efficiency_percentage}%
                </p>
              </div>
              <div className="bg-green-50 rounded-lg p-4">
                <p className="text-gray-600 text-sm">Additional Water Needed</p>
                <p className="text-lg font-bold text-green-600 mt-2">
                  {results.irrigation_planning?.irrigation_required_mm}mm
                </p>
              </div>
              <div className="bg-orange-50 rounded-lg p-4">
                <p className="text-gray-600 text-sm">Cost per Acre</p>
                <p className="text-lg font-bold text-orange-600 mt-2">
                  Rs.{" "}
                  {results.irrigation_planning?.estimated_cost_per_acre?.toLocaleString(
                    "en-IN",
                  )}
                </p>
              </div>
            </div>

            {/* Water Requirement */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-4">
                Water Requirement Analysis
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <svg
                      className="w-6 h-6 text-blue-500"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3v-6"
                      />
                    </svg>
                    <span className="text-gray-600 font-medium">
                      Total Water Needed
                    </span>
                  </div>
                  <span className="text-xl font-bold text-blue-600">
                    {results.irrigation_planning?.total_water_needed_mm}mm
                  </span>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <svg
                      className="w-6 h-6 text-cyan-500"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.215A4.507 4.507 0 003 15z"
                      />
                    </svg>
                    <span className="text-gray-600 font-medium">
                      Available Rainfall
                    </span>
                  </div>
                  <span className="text-xl font-bold text-cyan-600">
                    {results.irrigation_planning?.rainfall_mm}mm
                  </span>
                </div>

                <div className="flex items-center justify-between p-4 bg-gradient-to-r from-primary-50 to-primary-100 rounded-lg border border-primary-200">
                  <div className="flex items-center space-x-2">
                    <svg
                      className="w-6 h-6 text-primary-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    <span className="text-gray-700 font-bold">
                      Additional Irrigation Required
                    </span>
                  </div>
                  <span className="text-2xl font-bold text-primary-600">
                    {results.irrigation_planning?.irrigation_required_mm}mm
                  </span>
                </div>
              </div>
            </div>

            {/* Irrigation Schedule */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-4">
                Irrigation Schedule
              </h3>
              <div className="space-y-3">
                {results.irrigation_planning?.irrigation_schedule?.map(
                  (stage, i) => (
                    <div
                      key={i}
                      className="border-l-4 border-primary-500 bg-gray-50 rounded-lg p-4"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h4 className="font-semibold text-gray-800">
                            {i + 1}. {stage.stage}
                          </h4>
                          <p className="text-sm text-gray-500 mt-1">
                            Days {stage.days_after_sowing}
                          </p>
                        </div>
                        <span className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-medium">
                          {stage.depth_mm}mm
                        </span>
                      </div>

                      <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-gray-200">
                        <div>
                          <p className="text-xs text-gray-500 uppercase tracking-wide">
                            Frequency
                          </p>
                          <p className="text-sm font-medium text-gray-700">
                            {stage.frequency}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-gray-500 uppercase tracking-wide">
                            Depth per Irrigation
                          </p>
                          <p className="text-sm font-medium text-gray-700">
                            {stage.depth_mm}mm
                          </p>
                        </div>
                      </div>

                      <p className="text-sm text-gray-600 mt-2 italic">
                        Note: {stage.notes}
                      </p>
                    </div>
                  ),
                )}
              </div>
            </div>

            {/* Cost & Efficiency Summary */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg p-5 border border-orange-200">
                <h4 className="font-semibold text-gray-800 mb-3">
                  Irrigation Cost
                </h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Cost per Acre</span>
                    <span className="font-bold text-orange-600">
                      Rs.{" "}
                      {results.irrigation_planning?.estimated_cost_per_acre?.toLocaleString(
                        "en-IN",
                      )}
                    </span>
                  </div>
                  <div className="flex justify-between border-t border-orange-200 pt-2 mt-2">
                    <span className="font-semibold text-gray-700">
                      Est. Total Cost
                    </span>
                    <span className="font-bold text-lg text-orange-600">
                      Rs.{" "}
                      {(
                        results.irrigation_planning?.estimated_cost_per_acre *
                        (results.profit_analysis?.revenue?.total_yield_quintal /
                          10 || 5)
                      )?.toLocaleString("en-IN")}
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-cyan-50 to-cyan-100 rounded-lg p-5 border border-cyan-200">
                <h4 className="font-semibold text-gray-800 mb-3">
                  Water Use Efficiency
                </h4>
                <div className="flex items-center mb-3">
                  <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-cyan-400 to-cyan-600 h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${results.irrigation_planning?.efficiency_percentage}%`,
                      }}
                    ></div>
                  </div>
                  <span className="ml-3 font-bold text-cyan-600 text-lg">
                    {results.irrigation_planning?.efficiency_percentage}%
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  Water loss through evaporation and runoff is minimal with{" "}
                  {results.irrigation_planning?.irrigation_method}
                </p>
              </div>
            </div>

            {/* Water Management Tips */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-4">
                Water Management Tips
              </h3>
              <div className="space-y-2">
                {results.irrigation_planning?.water_management_tips?.map(
                  (tip, i) => (
                    <div
                      key={i}
                      className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg border border-blue-200"
                    >
                      <svg
                        className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      <span className="text-gray-700 text-sm">{tip}</span>
                    </div>
                  ),
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === "disease" && (
          <div className="space-y-6">
            <div>
              <h3 className="font-semibold text-gray-800 mb-4">
                Disease Risk Assessment
              </h3>
              <div
                className={`inline-block px-4 py-2 rounded-lg font-medium ${
                  results.disease_risk?.disease_risk_level === "High"
                    ? "bg-red-100 text-red-700"
                    : results.disease_risk?.disease_risk_level === "Medium"
                      ? "bg-yellow-100 text-yellow-700"
                      : "bg-green-100 text-green-700"
                }`}
              >
                Risk Level: {results.disease_risk?.disease_risk_level}
              </div>
            </div>

            {results.disease_risk?.likely_diseases?.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-700 mb-2">
                  Likely Diseases
                </h4>
                <div className="flex flex-wrap gap-2">
                  {results.disease_risk?.likely_diseases?.map((disease, i) => (
                    <span
                      key={i}
                      className="px-3 py-1 bg-red-50 text-red-600 rounded-full text-sm"
                    >
                      {disease}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div>
              <h4 className="font-medium text-gray-700 mb-3">
                Recommended Pesticides
              </h4>
              <div className="space-y-3">
                {results.disease_risk?.pesticides?.map((pest, i) => (
                  <div key={i} className="bg-gray-50 rounded-lg p-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-medium text-gray-800">{pest.name}</p>
                        <p className="text-sm text-gray-600">
                          Dosage: {pest.dosage}
                        </p>
                        <p className="text-sm text-gray-500">{pest.timing}</p>
                      </div>
                      <span className="text-primary-600 font-medium">
                        Rs. {pest.cost_inr}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === "logistics" && (
          <div className="space-y-8">
            <div className="flex flex-col md:flex-row gap-6">
              <div className="flex-1 bg-gradient-to-br from-primary-50 to-white p-6 rounded-3xl border border-primary-100 shadow-sm">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-3 bg-primary-500 rounded-2xl text-white shadow-lg shadow-primary-500/20">
                    <Truck className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-800">Transportation Advice</h3>
                    <p className="text-sm text-gray-500 font-medium">Recommended mode and tips</p>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="p-4 bg-white rounded-2xl border border-primary-50 shadow-sm flex items-center justify-between">
                    <div>
                      <p className="text-xs text-gray-400 font-bold uppercase tracking-wider mb-1">Recommended Mode</p>
                      <p className="text-lg font-bold text-primary-700">{results.logistics_recommendation?.transport_mode || 'Local Transport'}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-400 font-bold uppercase tracking-wider mb-1">Est. Cost</p>
                      <p className="text-lg font-bold text-gray-800">Rs. {results.logistics_recommendation?.estimated_cost?.toLocaleString('en-IN') || '0'}</p>
                    </div>
                  </div>

                  <div className="p-4 bg-white rounded-2xl border border-primary-50 shadow-sm">
                    <p className="text-xs text-gray-400 font-bold uppercase tracking-wider mb-3">Transport Tips</p>
                    <ul className="space-y-3">
                      {results.logistics_recommendation?.transport_tips?.map((tip, i) => (
                        <li key={i} className="flex items-start gap-3 group">
                          <div className="mt-1 w-1.5 h-1.5 rounded-full bg-primary-400 group-hover:scale-125 transition-transform" />
                          <p className="text-sm text-gray-600 font-medium leading-relaxed">{tip}</p>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              <div className="flex-1 bg-gradient-to-br from-orange-50 to-white p-6 rounded-3xl border border-orange-100 shadow-sm">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-3 bg-orange-500 rounded-2xl text-white shadow-lg shadow-orange-500/20">
                    <Package className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-800">Storage Guidance</h3>
                    <p className="text-sm text-gray-500 font-medium">Safe storage practices</p>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="p-4 bg-white rounded-2xl border border-orange-50 shadow-sm">
                    <p className="text-xs text-gray-400 font-bold uppercase tracking-wider mb-3">Safe Storage Tips</p>
                    <ul className="space-y-3">
                      {results.logistics_recommendation?.storage_advice?.map((tip, i) => (
                        <li key={i} className="flex items-start gap-3 group">
                          <div className="mt-1 w-2 m-0.5 h-2 rounded-md bg-orange-300 group-hover:rotate-45 transition-transform" />
                          <p className="text-sm text-gray-700 font-medium leading-relaxed">{tip}</p>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="p-5 bg-gradient-to-br from-orange-500 to-orange-600 rounded-2xl text-white shadow-lg shadow-orange-500/30">
                    <div className="flex items-center gap-2 mb-2">
                      <Info className="w-5 h-5 text-white" />
                      <span className="font-bold">Mandi Info</span>
                    </div>
                    <p className="text-orange-50 text-sm leading-relaxed">
                      Your nearest recommended mandi for sale is <span className="font-bold text-white underline decoration-orange-300 underline-offset-4">{results.logistics_recommendation?.nearest_mandi || 'Local Market'}</span>.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "schemes" && (
          <div>
            <h3 className="font-semibold text-gray-800 mb-4">
              Eligible Government Schemes
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {results.government_schemes?.map((scheme, i) => (
                <div
                  key={i}
                  className="border rounded-lg p-4 hover:border-primary-300 transition-colors"
                >
                  <h4 className="font-semibold text-gray-800">{scheme.name}</h4>
                  <p className="text-primary-600 font-medium mt-1">
                    {scheme.benefit}
                  </p>
                  <span className="inline-block mt-2 px-2 py-1 bg-green-100 text-green-700 text-xs rounded">
                    {scheme.eligibility}
                  </span>
                  {scheme.apply_link && (
                    <a
                      href={scheme.apply_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block mt-3 text-sm text-primary-600 hover:underline"
                    >
                      Apply Now
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === "profit" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-gray-800 mb-4">Revenue</h3>
                <div className="bg-green-50 rounded-lg p-4 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Yield</span>
                    <span className="font-medium">
                      {results.profit_analysis?.revenue?.total_yield_quintal} Q
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Price/Quintal</span>
                    <span className="font-medium">
                      Rs. {results.profit_analysis?.revenue?.price_per_quintal}
                    </span>
                  </div>
                  <div className="flex justify-between border-t pt-2 mt-2">
                    <span className="font-semibold">Gross Revenue</span>
                    <span className="font-bold text-green-600">
                      Rs.{" "}
                      {results.profit_analysis?.revenue?.gross_revenue?.toLocaleString(
                        "en-IN",
                      )}
                    </span>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="font-semibold text-gray-800 mb-4">
                  Costs Breakdown
                </h3>
                <div className="bg-red-50 rounded-lg p-4 space-y-2">
                  {Object.entries(results.profit_analysis?.costs || {})
                    .filter(([key]) => key !== "total_cost")
                    .map(([key, value]) => (
                      <div
                        key={key}
                        className={`flex justify-between ${key === "irrigation" ? "bg-blue-50   rounded" : ""}`}
                      >
                        <span
                          className={`capitalize ${key === "irrigation" ? "font-semibold text-gray-700" : "text-gray-600"}`}
                        >
                          {key.replace("_", " ")}
                        </span>
                        <span
                          className={`font-medium ${key === "irrigation" ? "text-blue-600 font-bold" : ""}`}
                        >
                          Rs. {value?.toLocaleString("en-IN")}
                        </span>
                      </div>
                    ))}
                  <div className="flex justify-between border-t pt-2 mt-2">
                    <span className="font-semibold">Total Cost</span>
                    <span className="font-bold text-red-600">
                      Rs.{" "}
                      {results.profit_analysis?.costs?.total_cost?.toLocaleString(
                        "en-IN",
                      )}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-xl p-6 text-white">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                <div>
                  <p className="text-primary-100">Net Profit</p>
                  <p className="text-3xl font-bold mt-1">
                    Rs.{" "}
                    {results.profit_analysis?.net_profit?.toLocaleString(
                      "en-IN",
                    )}
                  </p>
                </div>
                <div>
                  <p className="text-primary-100">Profit/Acre</p>
                  <p className="text-3xl font-bold mt-1">
                    Rs.{" "}
                    {results.profit_analysis?.profit_per_acre?.toLocaleString(
                      "en-IN",
                    )}
                  </p>
                </div>
                <div>
                  <p className="text-primary-100">ROI</p>
                  <p className="text-3xl font-bold mt-1">
                    {results.profit_analysis?.roi_percentage}%
                  </p>
                </div>
              </div>
            </div>

            {/* Irrigation Cost Impact Analysis */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg p-4 border border-blue-200">
                <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
                  <svg
                    className="w-5 h-5 text-blue-600 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3v-6"
                    />
                  </svg>
                  Irrigation Cost Impact
                </h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Cost per Acre</span>
                    <span className="font-bold text-blue-600">
                      Rs.{" "}
                      {results.irrigation_planning?.estimated_cost_per_acre?.toLocaleString(
                        "en-IN",
                      )}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Irrigation Cost</span>
                    <span className="font-bold text-blue-600">
                      Rs.{" "}
                      {results.profit_analysis?.costs?.irrigation?.toLocaleString(
                        "en-IN",
                      )}
                    </span>
                  </div>
                  <div className="flex justify-between border-t border-blue-200 pt-2 mt-2">
                    <span className="text-gray-600">Cost as % of Total</span>
                    <span className="font-bold text-blue-600">
                      {(
                        (results.profit_analysis?.costs?.irrigation /
                          results.profit_analysis?.costs?.total_cost) *
                        100
                      )?.toFixed(1)}
                      %
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg p-4 border border-green-200">
                <h4 className="font-semibold text-gray-800 mb-3 flex items-center">
                  <svg
                    className="w-5 h-5 text-green-600 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                  Irrigation ROI
                </h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Irrigation Method</span>
                    <span className="font-bold text-gray-700">
                      {
                        results.irrigation_planning?.irrigation_method?.split(
                          "(",
                        )[0]
                      }
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Efficiency</span>
                    <span className="font-bold text-green-600">
                      {results.irrigation_planning?.efficiency_percentage}%
                    </span>
                  </div>
                  <div className="flex justify-between border-t border-green-200 pt-2 mt-2">
                    <span className="text-gray-600">Water Saved vs Flood</span>
                    <span className="font-bold text-green-600">
                      {100 - results.irrigation_planning?.efficiency_percentage}
                      %
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {results.profit_analysis?.comparison_with_alternatives?.length >
              0 && (
              <div>
                <h3 className="font-semibold text-gray-800 mb-4">
                  Comparison with Alternative Crops
                </h3>
                <div className="space-y-2">
                  {results.profit_analysis?.comparison_with_alternatives?.map(
                    (alt, i) => (
                      <div
                        key={i}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                      >
                        <span className="font-medium">{alt.crop}</span>
                        <span
                          className={`font-medium ${alt.estimated_profit > 0 ? "text-green-600" : "text-red-600"}`}
                        >
                          Rs. {alt.estimated_profit?.toLocaleString("en-IN")}
                        </span>
                      </div>
                    ),
                  )}
                </div>
              </div>
            )}

            {/* Download Report Button */}
            <div className="mt-12 pt-8 border-t border-gray-100 flex flex-col items-center">
              <div className="bg-gradient-to-br from-gray-50 to-white p-8 rounded-3xl border border-gray-200 shadow-sm text-center max-w-2xl w-full">
                <div className="mb-4 inline-flex p-4 bg-primary-100 rounded-2xl text-primary-600">
                  <FileText className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold text-gray-800 mb-2">Analysis Complete!</h3>
                <p className="text-gray-500 mb-8">
                  Get a comprehensive PDF report including soil data, crop recommendations, price trends, and profit analysis.
                </p>
                <button
                  onClick={async () => {
                    setDownloading(true);
                    try {
                      const success = await generatePDF(results);
                      if (success) {
                        alert("Your report is ready! The download should start automatically.");
                      }
                    } catch (error) {
                      console.error("PDF generation failed:", error);
                      alert("Error generating PDF. Please try again or use the print function.");
                    }
                    setDownloading(false);
                  }}
                  disabled={downloading}
                  className={`btn-primary w-full md:w-auto px-8 py-4 rounded-2xl shadow-xl transition-all flex items-center justify-center gap-3 ${
                    downloading ? "opacity-75 cursor-wait" : "hover:scale-[1.02] active:scale-[0.98]"
                  }`}
                >
                  {downloading ? (
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white/30 border-t-white" />
                  ) : (
                    <Download className="w-5 h-5" />
                  )}
                  <span className="font-bold tracking-wide">
                    {downloading ? "Generating Report..." : "Download Comprehensive Report (.PDF)"}
                  </span>
                </button>
                <p className="text-xs text-gray-400 mt-4 italic">
                  Note: This report contains all sections of the current analysis.
                </p>
              </div>
            </div>
          </div>
        )}
        </motion.div>
      </AnimatePresence>
    </motion.div>
  );
};

export default Results;
