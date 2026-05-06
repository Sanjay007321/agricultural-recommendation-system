import { useAuth } from "../context/AuthContext";

const MyStatus = ({ analysisCount = 0 }) => {
  const { user } = useAuth();

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">My Status</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Analysis Count Card */}
        <div className="bg-blue-400 rounded-2xl p-8 text-white transform transition-all duration-300 hover:scale-105 hover:shadow-lg cursor-pointer">
          <div className="flex flex-col items-center text-center">
            <svg
              className="w-16 h-16 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
            <h3 className="text-xl font-bold mb-3">Total Analysis</h3>
            <p className="text-4xl font-bold">{analysisCount}</p>
            <p className="text-sm mt-2 opacity-90">Completed</p>
          </div>
        </div>

        {/* Location Card */}
        <div className="bg-green-400 rounded-2xl p-8 text-white transform transition-all duration-300 hover:scale-105 hover:shadow-lg">
          <div className="flex flex-col items-center text-center">
            <svg
              className="w-16 h-16 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
              />
            </svg>
            <h3 className="text-xl font-bold mb-3">Current Location</h3>
            <p className="text-3xl font-bold">{user?.state || "Not Set"}</p>
          </div>
        </div>

        {/* Land Size Card */}
        <div className="bg-yellow-400 rounded-2xl p-8 text-white transform transition-all duration-300 hover:scale-105 hover:shadow-lg">
          <div className="flex flex-col items-center text-center">
            <svg
              className="w-16 h-16 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064"
              />
            </svg>
            <h3 className="text-xl font-bold mb-3">Land Size</h3>
            <p className="text-3xl font-bold">
              {user?.land_size_acres ? `${user.land_size_acres}` : "Not Set"}
            </p>
            <p className="text-sm mt-2 opacity-90">Acres</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MyStatus;
