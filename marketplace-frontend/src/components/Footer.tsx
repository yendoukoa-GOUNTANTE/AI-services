import React from 'react';
import { Github, Twitter, Linkedin, Globe, MessageSquare } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white pt-24 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 mb-20">
          <div className="md:col-span-4">
            <div className="flex items-center space-x-2 mb-8">
              <img src="/logo.svg" alt="Yendoukoa AI Logo" className="h-10 w-10 brightness-0 invert" />
              <span className="text-2xl font-black tracking-tight">Yendoukoa <span className="text-blue-500">AI</span></span>
            </div>
            <p className="text-gray-400 text-lg leading-relaxed mb-8 font-medium">
              Empowering the next generation of builders with professional-grade AI services and autonomous agents.
            </p>
            <div className="flex space-x-5">
              {[Twitter, Github, Linkedin, MessageSquare].map((Icon, i) => (
                <a key={i} href="#" className="p-3 bg-white/5 rounded-xl text-gray-400 hover:text-white hover:bg-blue-600 transition-all border border-white/5">
                  <Icon size={20} />
                </a>
              ))}
            </div>
          </div>

          <div className="md:col-span-2 md:col-start-6">
            <h4 className="font-black mb-8 text-white uppercase tracking-widest text-xs">Marketplace</h4>
            <ul className="space-y-4 text-gray-400 font-bold">
              <li><a href="#" className="hover:text-blue-500 transition-colors">Development</a></li>
              <li><a href="#" className="hover:text-blue-500 transition-colors">Design Store</a></li>
              <li><a href="#" className="hover:text-blue-500 transition-colors">Security Ops</a></li>
              <li><a href="#" className="hover:text-blue-500 transition-colors">Business AI</a></li>
            </ul>
          </div>

          <div className="md:col-span-2">
            <h4 className="font-black mb-8 text-white uppercase tracking-widest text-xs">Resources</h4>
            <ul className="space-y-4 text-gray-400 font-bold">
              <li><a href="./CHANGELOG.md" target="_blank" className="hover:text-blue-500 transition-colors">Changelog</a></li>
              <li><a href="#" className="hover:text-blue-500 transition-colors">Documentation</a></li>
              <li><a href="#" className="hover:text-blue-500 transition-colors">API Keys</a></li>
              <li><a href="#" className="hover:text-blue-500 transition-colors">Pricing</a></li>
            </ul>
          </div>

          <div className="md:col-span-3">
            <h4 className="font-black mb-8 text-white uppercase tracking-widest text-xs">Stay Updated</h4>
            <p className="text-gray-500 text-sm mb-6 font-medium">Get the latest AI agents and security updates delivered to your inbox.</p>
            <form className="relative group">
              <input
                type="email"
                placeholder="email@example.com"
                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 px-6 text-sm font-bold text-white placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
              />
              <button className="absolute right-2 top-2 bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-black hover:bg-blue-700 transition-colors">
                Join
              </button>
            </form>
          </div>
        </div>

        <div className="pt-12 border-t border-white/5 flex flex-col md:flex-row justify-between items-center text-gray-500 font-bold text-xs">
          <p>&copy; 2026 Yendoukoa AI. Built for the autonomous future.</p>
          <div className="flex space-x-8 mt-6 md:mt-0">
             <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
             <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
             <a href="#" className="hover:text-white transition-colors">Cookies</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
