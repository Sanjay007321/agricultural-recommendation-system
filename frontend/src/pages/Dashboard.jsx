import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { analysisAPI } from "../services/api";
import Logo from "../components/Logo";
import MyStatus from "../components/MyStatus";
import ClimateBoard from "../components/ClimateBoard";
import { motion } from "framer-motion";
import { ArrowRight, Activity, Beaker, History, User, Sparkles } from "lucide-react";

const Dashboard = () => {
  const { user } = useAuth();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await analysisAPI.getHistory();
      setHistory(response.data.slice(0, 4));
    } catch (err) {
      console.error("Failed to load history");
    }
    setLoading(false);
  };

  const dashboardCards = [
    {
      title: "Get Recommendation",
      icon: <Beaker className="w-8 h-8" />,
      path: "/analyze",
      gradient: "from-orange-400 to-orange-500",
      shadow: "shadow-orange-500/30",
    },
    {
      title: "Analysis History",
      icon: <History className="w-8 h-8" />,
      path: "/history",
      gradient: "from-blue-400 to-indigo-500",
      shadow: "shadow-blue-500/30",
    },
    {
      title: "Update Profile",
      icon: <User className="w-8 h-8" />,
      path: "/profile",
      gradient: "from-emerald-400 to-emerald-600",
      shadow: "shadow-emerald-500/30",
    },
    {
      title: "More Services",
      icon: <Activity className="w-8 h-8" />,
      path: "/analyze",
      gradient: "from-purple-400 to-purple-600",
      shadow: "shadow-purple-500/30",
    },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { 
      y: 0, 
      opacity: 1,
      transition: { type: "spring", stiffness: 300, damping: 24 }
    }
  };

  return (
    <motion.div 
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="pb-12"
    >
      {/* Header */}
      <motion.div variants={itemVariants} className="mb-10 flex border-b border-gray-200/50 pb-6 items-center justify-between">
        <div>
          <h1 className="text-4xl font-extrabold text-gray-800 tracking-tight flex items-center gap-3">
            Welcome back, {user?.full_name?.split(" ")[0] || 'Guest'}!
            <Sparkles className="w-6 h-6 text-yellow-500 animate-pulse" />
          </h1>
          <p className="text-gray-500 mt-2 font-medium">Farmer ID: {user?.farmer_id || 'ID-0000'} • Let's grow a better future together.</p>
        </div>
      </motion.div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        
        {/* Left Column (Cards + Components) */}
        <div className="xl:col-span-2 space-y-8">
          
          {/* Dashboard Cards Grid */}
          <motion.div variants={itemVariants} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {dashboardCards.map((card, index) => (
              <Link key={index} to={card.path}>
                <motion.div 
                  whileHover={{ y: -5, scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`bg-gradient-to-br ${card.gradient} rounded-3xl p-6 text-white shadow-lg ${card.shadow} overflow-hidden relative group h-full flex flex-col`}
                >
                  <div className="absolute -right-4 -top-4 opacity-20 transform group-hover:scale-110 transition-transform duration-500">
                    <div className="w-24 h-24">{card.icon}</div>
                  </div>
                  <div className="bg-white/20 w-14 h-14 rounded-2xl flex items-center justify-center backdrop-blur-md mb-5 border border-white/20 shadow-inner">
                    {card.icon}
                  </div>
                  <h3 className="text-lg font-bold tracking-wide mt-auto">{card.title}</h3>
                  <div className="mt-3 flex items-center text-sm font-semibold opacity-90 group-hover:opacity-100 transition-opacity">
                    <span>Explore</span>
                    <ArrowRight className="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform" />
                  </div>
                </motion.div>
              </Link>
            ))}
          </motion.div>

          {/* Climate Board */}
          <motion.div variants={itemVariants} className="animate-fade-in relative z-10 block">
            <ClimateBoard />
          </motion.div>
        </div>

        {/* Right Column (History & Status) */}
        <div className="space-y-8">
          
          {/* Latest Analysis Wrapper */}
          <motion.div variants={itemVariants} className="glass rounded-[2rem] p-6 flex flex-col h-[400px]">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                <History className="w-5 h-5 text-indigo-500" />
                Latest Analysis
              </h2>
              <Link to="/history" className="text-sm text-indigo-600 font-semibold hover:text-indigo-700 flex items-center">
                View All <ArrowRight className="w-4 h-4 ml-1" />
              </Link>
            </div>

            <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
              {loading ? (
                <div className="flex justify-center items-center h-full">
                  <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-600"></div>
                </div>
              ) : history.length > 0 ? (
                <div className="space-y-3">
                  {history.map((item, idx) => (
                    <Link
                      key={item.analysis_id}
                      to={`/results/${item.analysis_id}`}
                      className="block bg-white/70 border border-gray-100 hover:border-indigo-200 rounded-2xl p-4 transition-all hover:shadow-md group relative overflow-hidden"
                    >
                      <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-indigo-400 to-indigo-600 group-hover:w-2 transition-all"></div>
                      <div className="ml-2">
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="font-bold text-gray-800 text-lg group-hover:text-indigo-600 transition-colors">{item.crop}</h3>
                          <span className="text-xs bg-indigo-50 text-indigo-700 py-1 px-2 rounded-lg font-bold border border-indigo-100">
                            Rs. {item.profit?.toLocaleString("en-IN") || "0"}
                          </span>
                        </div>
                        <div className="flex justify-between items-center text-xs text-gray-500 font-medium">
                          <span>{item.analysis_id.substring(0,8)}</span>
                          <span>{new Date(item.created_at).toLocaleDateString("en-IN")}</span>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <div className="w-16 h-16 bg-gray-50 text-gray-400 rounded-full flex items-center justify-center mb-4">
                    <History className="w-8 h-8 opacity-50" />
                  </div>
                  <p className="text-gray-500 font-medium mb-5">No analyses yet</p>
                  <Link
                    to="/analyze"
                    className="btn-primary text-sm shadow-lg shadow-primary-500/30"
                  >
                    Get Recommendation
                  </Link>
                </div>
              )}
            </div>
          </motion.div>

          <motion.div variants={itemVariants}>
            <MyStatus analysisCount={history.length} />
          </motion.div>
          
        </div>
      </div>
    </motion.div>
  );
};

export default Dashboard;
