import React from 'react';
import { CreditCard, X, Menu, User as UserIcon, Sun, Moon } from 'lucide-react';
import { User } from '../api';

interface NavbarProps {
  user: User | null;
  credits: number;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  isMenuOpen: boolean;
  setIsMenuOpen: (isOpen: boolean) => void;
  setShowLoginModal: (show: boolean) => void;
  handleLogout: () => void;
  loading: boolean;
  isDarkMode: boolean;
  toggleDarkMode: () => void;
}

const Navbar: React.FC<NavbarProps> = ({
  user,
  credits,
  activeTab,
  setActiveTab,
  isMenuOpen,
  setIsMenuOpen,
  setShowLoginModal,
  handleLogout,
  loading,
  isDarkMode,
  toggleDarkMode
}) => {
  return (
    <nav className="bg-white border-b sticky top-0 z-50 shadow-sm transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex items-center space-x-2 group cursor-pointer" onClick={() => setActiveTab('marketplace')}>
              <img src="/logo.svg" alt="Yendoukoa AI Logo" className="h-9 w-9 group-hover:scale-110 transition-transform" />
              <span className="text-xl font-black text-gray-900 tracking-tight transition-colors">Yendoukoa <span className="text-blue-600">AI</span></span>
            </div>
            <div className="hidden md:ml-10 md:flex md:space-x-8">
              {[
                { id: 'marketplace', label: 'Official Services' },
                { id: 'agents-store', label: 'AI Agents Store' },
                { id: 'design-store', label: 'Design & API Store' },
                { id: 'dashboard', label: 'Dashboard' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-bold transition-all ${
                    activeTab === tab.id
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-900 hover:border-gray-300'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={toggleDarkMode}
              className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
              title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
              aria-label={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
            >
              {isDarkMode ? <Sun size={20} aria-hidden="true" /> : <Moon size={20} aria-hidden="true" />}
            </button>

            {user ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center bg-blue-50 text-blue-700 px-4 py-1.5 rounded-full text-sm font-black border border-blue-100 transition-colors">
                  <CreditCard size={16} className="mr-2" />
                  {credits} <span className="ml-1 opacity-70 text-xs">Credits</span>
                </div>
                <div className="hidden sm:flex items-center space-x-2 bg-gray-50 px-3 py-1.5 rounded-xl border border-gray-100 transition-colors">
                  <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center text-white text-[10px] font-bold">
                    {user.username.charAt(0).toUpperCase()}
                  </div>
                  <span className="text-sm font-bold text-gray-700 transition-colors">{user.username}</span>
                </div>
                <button
                  className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
                  onClick={handleLogout}
                  title="Logout"
                  aria-label="Logout"
                >
                  <X size={20} aria-hidden="true" />
                </button>
              </div>
            ) : (
              <button
                onClick={() => setShowLoginModal(true)}
                disabled={loading}
                className="bg-blue-600 text-white px-6 py-2.5 rounded-xl text-sm font-black hover:bg-blue-700 transition-all shadow-lg shadow-blue-200 active:scale-95 disabled:opacity-50"
              >
                {loading ? 'Connecting...' : 'Login / Register'}
              </button>
            )}
            <button
              className="md:hidden p-2 text-gray-500"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label={isMenuOpen ? "Close menu" : "Open menu"}
              aria-expanded={isMenuOpen}
            >
              {isMenuOpen ? <X size={24} aria-hidden="true" /> : <Menu size={24} aria-hidden="true" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-b px-4 pt-2 pb-6 space-y-2 transition-colors duration-300">
           {[
                { id: 'marketplace', label: 'Official Services' },
                { id: 'agents-store', label: 'AI Agents Store' },
                { id: 'design-store', label: 'Design & API Store' },
                { id: 'dashboard', label: 'Dashboard' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setIsMenuOpen(false);
                }}
                className={`block w-full text-left px-4 py-3 rounded-xl text-base font-bold ${
                  activeTab === tab.id ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50 transition-colors'
                }`}
              >
                {tab.label}
              </button>
            ))}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
