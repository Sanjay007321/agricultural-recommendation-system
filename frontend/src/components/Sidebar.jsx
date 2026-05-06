import { NavLink, useLocation } from 'react-router-dom';
import { LayoutDashboard, Beaker, History, User, HeartHandshake, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Sidebar = ({ isOpen, setIsOpen }) => {
  const location = useLocation();
  const isHomePage = location.pathname === '/dashboard';
  
  const allMenuItems = [
    {
      path: '/dashboard',
      label: 'Dashboard',
      icon: <LayoutDashboard className="w-5 h-5" />,
    },
    {
      path: '/analyze',
      label: 'Get Recommendation',
      icon: <Beaker className="w-5 h-5" />,
    },
    {
      path: '/history',
      label: 'Analysis History',
      icon: <History className="w-5 h-5" />,
    },
    {
      path: '/profile',
      label: 'My Profile',
      icon: <User className="w-5 h-5" />,
    },
  ];

  // Rule: In mobile devices view show only dashboard on home page
  // We'll filter the menu items if we are on the home page and on a small screen
  // React check for screen size usually requires a hook, but we can simplify 
  // by just showing/hiding based on logic if preferred, or using CSS.
  // The user specifically asked to "show only dashboard" in the menu on home page for mobile.
  const menuItems = isHomePage ? [allMenuItems[0]] : allMenuItems;

  return (
    <>
      {/* Mobile Backdrop */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsOpen(false)}
            className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 md:hidden"
          />
        )}
      </AnimatePresence>

      <aside className={`w-64 glass fixed left-0 top-0 md:top-[72px] bottom-0 overflow-y-auto border-r border-white/50 z-50 transition-transform duration-300 transform ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'} pb-6`}>
        <div className="p-5 h-full flex flex-col">
          {/* Mobile Header (Side-by-side with Navbar ARS text) */}
          <div className="flex md:hidden items-center justify-between mb-8 pt-2">
            <span className="text-xl font-bold text-primary-600">ARS Menu</span>
            <button onClick={() => setIsOpen(false)} className="p-2 bg-gray-100 rounded-lg text-gray-500">
              <X className="w-5 h-5" />
            </button>
          </div>

          <nav className="space-y-3 flex-grow md:mt-2">
            {menuItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-4 py-3.5 rounded-xl transition-all duration-300 relative group overflow-hidden ${
                    isActive
                      ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-md shadow-primary-500/30'
                      : 'text-gray-600 hover:bg-white/80 hover:text-primary-600 border border-transparent hover:border-white/50 hover:shadow-sm'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <div className="relative z-10">{item.icon}</div>
                    <span className="font-medium relative z-10">{item.label}</span>
                    {isActive && (
                      <motion.div
                        layoutId="sidebarActiveBg"
                        className="absolute inset-0 bg-gradient-to-r from-primary-500 to-primary-600"
                        initial={false}
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                        style={{ zIndex: 0 }}
                      />
                    )}
                  </>
                )}
              </NavLink>
            ))}
          </nav>
          
          <div className="mt-auto pt-8">
            <div className="p-5 bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl text-white shadow-lg shadow-primary-500/40 relative overflow-hidden group">
              <motion.div 
                whileHover={{ scale: 1.1, rotate: 10 }}
                className="absolute top-0 right-0 -mr-4 -mt-4 opacity-20 transition-transform duration-500"
              >
                <HeartHandshake className="w-24 h-24" />
              </motion.div>
              <h3 className="font-bold mb-2 relative z-10 tracking-wide">Need Help?</h3>
              <p className="text-sm text-primary-100 mb-5 relative z-10 leading-relaxed font-medium">
                Get farming advice from our experts
              </p>
              <button className="w-full py-2.5 bg-white text-primary-700 rounded-xl font-bold hover:bg-primary-50 active:scale-95 transition-all shadow-sm relative z-10">
                Contact Support
              </button>
            </div>
            
            <div className="mt-6 text-center text-xs text-gray-500 font-medium">
              <p>ARS System v1.0</p>
              <p className="mt-1 text-primary-600/60 font-semibold">Made for Indian Farmers</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
