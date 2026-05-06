import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Logo from "./Logo";
import { LogOut, User, Menu } from "lucide-react";
import { motion } from "framer-motion";

const Navbar = ({ onMenuClick }) => {
  const { user, logout } = useAuth();

  return (
    <nav className="glass fixed top-0 left-0 right-0 z-50">
      <div className="px-4 md:px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <motion.button
              whileTap={{ scale: 0.9 }}
              onClick={onMenuClick}
              className="p-2 bg-primary-50 text-primary-600 rounded-xl md:hidden hover:bg-primary-100 transition-colors"
            >
              <Menu className="w-6 h-6" />
            </motion.button>
            <motion.div 
              whileHover={{ rotate: 180 }}
              transition={{ duration: 0.5 }}
              className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/30"
            >
              <Logo className="w-6 h-6" fill="#ffffff" />
            </motion.div>
            <div className="hidden sm:block">
              <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-700 to-primary-500">
                ARS System
              </h1>
              <p className="text-xs text-gray-500 font-medium tracking-wide">
                Complete Agriculture Solutions
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-4 bg-white/50 px-4 py-2 rounded-2xl border border-white/60 shadow-sm transition-all hover:bg-white/80">
              <div className="text-right">
                <p className="text-sm font-semibold text-gray-800">
                  {user?.full_name || 'Guest User'}
                </p>
                <p className="text-xs text-primary-600 font-medium">{user?.farmer_id || 'ID-0000'}</p>
              </div>
              <div className="w-10 h-10 bg-gradient-to-br from-primary-100 to-primary-200 rounded-full flex items-center justify-center border-2 border-white shadow-inner">
                <span className="text-primary-700 font-bold text-lg">
                  {(user?.full_name?.charAt(0) || 'G').toUpperCase()}
                </span>
              </div>
            </div>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              onClick={logout}
              className="w-10 h-10 flex items-center justify-center bg-red-50 text-red-500 hover:bg-red-500 hover:text-white rounded-xl transition-all shadow-sm hover:shadow-red-500/30"
              title="Logout"
            >
              <LogOut className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
