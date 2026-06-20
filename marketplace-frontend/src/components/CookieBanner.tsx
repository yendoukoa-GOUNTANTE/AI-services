import React, { useState, useEffect } from 'react';
import { ShieldCheck, X } from 'lucide-react';

const CookieBanner: React.FC = () => {
  const [show, setShow] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem('cookie-consent');
    if (!consent) {
      const timer = setTimeout(() => setShow(true), 2000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem('cookie-consent', 'accepted');
    setShow(false);
  };

  const handleDecline = () => {
    localStorage.setItem('cookie-consent', 'declined');
    setShow(false);
  };

  if (!show) return null;

  return (
    <div className="fixed bottom-8 left-8 right-8 z-[100] animate-slide-up">
      <div className="max-w-4xl mx-auto bg-white dark:bg-gray-900 rounded-[32px] shadow-2xl border border-gray-100 dark:border-white/10 p-8 flex flex-col md:flex-row items-center justify-between gap-8 backdrop-blur-xl bg-white/90 dark:bg-gray-900/90">
        <div className="flex items-start space-x-6">
          <div className="w-14 h-14 bg-blue-50 dark:bg-blue-900/20 rounded-2xl flex items-center justify-center text-blue-600 shrink-0">
            <ShieldCheck size={28} />
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-black tracking-tight text-gray-900 dark:text-white">Privacy & Cookies</h3>
            <p className="text-gray-500 dark:text-gray-400 text-sm font-medium leading-relaxed max-w-xl">
              We use cookies to enhance your experience, analyze our traffic, and provide secure AI sessions.
              By clicking "Accept All", you consent to our use of cookies as described in our Privacy Policy.
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-4 w-full md:w-auto">
          <button
            onClick={handleDecline}
            className="flex-1 md:flex-none px-6 py-3.5 text-sm font-black text-gray-500 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            Manage
          </button>
          <button
            onClick={handleAccept}
            className="flex-1 md:flex-none bg-blue-600 text-white px-10 py-3.5 rounded-xl font-black text-sm hover:bg-blue-700 shadow-xl shadow-blue-100 dark:shadow-none transition-all active:scale-95"
          >
            Accept All
          </button>
          <button
            onClick={() => setShow(false)}
            className="hidden md:block p-2 text-gray-300 hover:text-gray-500 transition-colors"
          >
            <X size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default CookieBanner;
