import { useState, useEffect } from "react";
import { analysisAPI } from "../services/api";

const ClimateBoard = () => {
  const [climateData, setClimateData] = useState(null);
  const [climateLoading, setClimateLoading] = useState(true);

  useEffect(() => {
    loadClimateData();
  }, []);

  const loadClimateData = async () => {
    try {
      const response = await analysisAPI.getClimateDashboard();
      setClimateData(response);
    } catch (err) {
      console.error("Failed to load climate data");
    }
    setClimateLoading(false);
  };

  return (
    <div className="bg-white rounded-2xl shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Climate Dashboard
      </h2>

      {climateLoading ? (
        <div className="flex justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-600"></div>
        </div>
      ) : climateData ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Climate Cycle Visualization */}
          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <svg
                className="w-5 h-5 mr-2 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              Climate Cycle
            </h3>

            <div className="space-y-4">
              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-red-500 flex items-center justify-center text-white text-sm font-bold">
                  1
                </div>
                <div className="ml-3">
                  <div className="font-medium text-gray-800">Temperature</div>
                  <div className="text-sm text-gray-600">
                    Current: {climateData.current_weather.temperature}°C
                  </div>
                  <div className="text-xs text-gray-500">
                    Max: {climateData.current_weather.temp_max}°C | Min:{" "}
                    {climateData.current_weather.temp_min}°C
                  </div>
                </div>
              </div>

              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-yellow-500 flex items-center justify-center text-white text-sm font-bold">
                  2
                </div>
                <div className="ml-3">
                  <div className="font-medium text-gray-800">Humidity</div>
                  <div className="text-sm text-gray-600">
                    {climateData.current_weather.humidity}%
                  </div>
                </div>
              </div>

              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-gray-500 flex items-center justify-center text-white text-sm font-bold">
                  3
                </div>
                <div className="ml-3">
                  <div className="font-medium text-gray-800">Cloud Cover</div>
                  <div className="text-sm text-gray-600">
                    {climateData.current_weather.cloud_cover}% coverage
                  </div>
                </div>
              </div>

              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-bold">
                  4
                </div>
                <div className="ml-3">
                  <div className="font-medium text-gray-800">Visibility</div>
                  <div className="text-sm text-gray-600">
                    {climateData.current_weather.visibility} meters
                  </div>
                </div>
              </div>

              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white text-sm font-bold">
                  5
                </div>
                <div className="ml-3">
                  <div className="font-medium text-gray-800">Precipitation</div>
                  <div className="text-sm text-gray-600">
                    Current: {climateData.current_weather.rainfall}mm | Daily:{" "}
                    {climateData.current_weather.rain_sum}mm
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Current Weather */}
          <div className="bg-blue-50 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <svg
                className="w-5 h-5 mr-2 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"
                />
              </svg>
              Current Weather
            </h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-white rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {climateData.current_weather.temperature}°C
                </div>
                <div className="text-xs text-gray-600">Temp</div>
              </div>
              <div className="bg-white rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {climateData.current_weather.humidity}%
                </div>
                <div className="text-xs text-gray-600">Humidity</div>
              </div>
              <div className="bg-white rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {climateData.current_weather.rainfall}mm
                </div>
                <div className="text-xs text-gray-600">Rainfall</div>
              </div>
              <div className="bg-white rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {climateData.current_weather.cloud_cover}%
                </div>
                <div className="text-xs text-gray-600">Cloud</div>
              </div>
            </div>
            <div className="mt-3 text-xs text-gray-500 text-center">
              Updated:{" "}
              {new Date(
                climateData.current_weather.updated_at
              ).toLocaleString("en-IN")}
            </div>
          </div>

          {/* Top Crop Recommendations */}
          <div className="bg-green-50 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <svg
                className="w-5 h-5 mr-2 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
                />
              </svg>
              Top Recommendations
            </h3>
            <div className="space-y-3">
              {climateData.top_crop_recommendations.map((crop, index) => (
                <div key={index} className="bg-white rounded-lg p-3">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-semibold text-gray-800 text-sm">
                        {crop.crop}
                      </h4>
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full mt-1 ${
                          crop.suitability === "excellent"
                            ? "bg-green-100 text-green-800"
                            : crop.suitability === "good"
                            ? "bg-yellow-100 text-yellow-800"
                            : "bg-red-100 text-red-800"
                        }`}
                      >
                        {crop.suitability.toUpperCase()}
                      </span>
                    </div>
                    <div className="text-right text-xs">
                      <div className="text-gray-600">
                        {crop.optimal_temp_range}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          Climate data not available
        </div>
      )}
    </div>
  );
};

export default ClimateBoard;
