import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import nationwideBg from "../nationwide-presence.jpg";
import Logo from "../components/Logo";
import { motion } from "framer-motion";
import { ArrowRight, Loader2 } from "lucide-react";

const Login = () => {
  const [formData, setFormData] = useState({
    mobile: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const result = await login(formData.mobile, formData.password);

    if (result.success) {
      navigate("/dashboard");
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden"
      style={{
        backgroundImage: `url(${nationwideBg})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundAttachment: "fixed",
      }}
    >
      <div className="absolute inset-0 bg-black/50 backdrop-blur-[2px]"></div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="w-full max-w-md relative z-10"
      >
        <div className="text-center mb-8">
          <motion.div 
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ duration: 0.7, type: "spring", bounce: 0.5 }}
            className="w-24 h-24 bg-white/90 backdrop-blur-md rounded-full flex items-center justify-center mx-auto mb-6 shadow-2xl border-[3px] border-white/50"
          >
            <Logo className="w-14 h-14" fill="#16a34a" />
          </motion.div>
          <h1 className="text-4xl font-extrabold text-white drop-shadow-lg tracking-tight">
            ARS System
          </h1>
          <p className="text-primary-100 mt-2 font-medium tracking-wide">Welcome back to smart farming</p>
        </div>

        <div className="glass rounded-[2.5rem] p-10 shadow-2xl relative overflow-hidden border border-white/60">
          <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-primary-400 via-primary-500 to-primary-600"></div>
          
          <h2 className="text-2xl font-bold text-gray-800 mb-8 text-center flex items-center justify-center gap-2">
            Secure Login
          </h2>

          {error && (
            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="bg-red-50/90 backdrop-blur-sm border border-red-200 text-red-600 px-4 py-3 rounded-xl mb-6 shadow-sm">
              <span className="font-medium">{error}</span>
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">
                Mobile Number
              </label>
              <input
                type="text"
                name="mobile"
                value={formData.mobile}
                onChange={handleChange}
                placeholder="Enter 10-digit number"
                className="input-field bg-white/60 focus:bg-white transition-colors"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                className="input-field bg-white/60 focus:bg-white transition-colors"
                required
              />
            </div>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-700 hover:to-primary-600 text-white py-4 rounded-xl flex items-center justify-center space-x-2 shadow-lg shadow-primary-500/30 overflow-hidden relative group font-bold text-lg mt-8"
            >
              {loading ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : (
                <>
                  <span className="relative z-10">Login</span>
                  <ArrowRight className="w-5 h-5 relative z-10 transform group-hover:translate-x-1 transition-transform" />
                  <div className="absolute inset-0 bg-white/10 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                </>
              )}
            </motion.button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-gray-600 font-medium">
              Don't have an account?{" "}
              <Link
                to="/register"
                className="text-primary-600 font-bold hover:text-primary-700 transition-colors ml-1 hover:underline"
              >
                Register here
              </Link>
            </p>
          </div>
        </div>

        <p className="text-center text-white/80 text-sm mt-8 drop-shadow-lg font-medium">
          Empowering Indian Farmers with Technology
        </p>
      </motion.div>
    </div>
  );
};

export default Login;
