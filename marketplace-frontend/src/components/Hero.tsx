import React from 'react';
import { Search } from 'lucide-react';
import { AIService } from '../types';

interface HeroProps {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  onTryAI: () => void;
}

const Hero: React.FC<HeroProps> = ({ searchQuery, setSearchQuery, onTryAI }) => {
  return (
    <div className="bg-gradient-to-br from-blue-700 via-blue-600 to-indigo-700 text-white py-24 relative overflow-hidden">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1200px] h-[1200px] bg-white rounded-full blur-[140px] opacity-10 -z-0"></div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center">
          <div className="inline-flex items-center space-x-2 bg-blue-500/30 border border-blue-400/30 px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-widest mb-8 animate-fade-in">
             <span className="relative flex h-2 w-2 mr-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-white"></span>
             </span>
             New: Gemini 1.5 Pro Integrated
          </div>
          <h1 className="text-5xl font-black tracking-tight sm:text-7xl lg:text-8xl mb-8 leading-[0.9]">
            Ship faster with <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-100 to-indigo-200">AI Engineers</span>
          </h1>
          <p className="mt-8 text-xl text-blue-100 max-w-2xl mx-auto font-medium leading-relaxed opacity-90">
            Professional-grade AI specialists that write code, manage infrastructure, and grow your business 24/7.
          </p>
          <div className="mt-12 flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
            <button
              onClick={onTryAI}
              className="bg-white text-blue-600 px-10 py-5 rounded-2xl font-black text-xl hover:bg-blue-50 transition-all shadow-2xl hover:-translate-y-1 active:translate-y-0"
            >
              Try AI Engineer Free
            </button>
            <button className="text-blue-100 font-bold hover:text-white transition-colors flex items-center group">
               Watch Demo <span className="ml-2 group-hover:translate-x-1 transition-transform">→</span>
            </button>
          </div>

          <div className="mt-16 max-w-3xl mx-auto">
            <div className="relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-blue-400 to-indigo-400 rounded-3xl blur opacity-20 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
              <div className="relative flex items-center">
                <div className="absolute inset-y-0 left-0 pl-6 flex items-center pointer-events-none">
                  <Search className="h-6 w-6 text-blue-600" />
                </div>
                <input
                  type="text"
                  className="block w-full pl-16 pr-4 py-6 border-none rounded-3xl leading-5 bg-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-blue-400/50 shadow-2xl text-xl font-bold"
                  placeholder="Search for agents, roles, or domains..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <div className="absolute right-4">
                  <button className="bg-gray-900 text-white px-8 py-3.5 rounded-2xl font-black text-sm hover:bg-black transition-colors shadow-lg">
                    Search
                  </button>
                </div>
              </div>
            </div>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <span className="text-blue-200 text-sm font-black self-center mr-2 uppercase tracking-widest opacity-60">Trending:</span>
              {['Security', 'Development', 'National Security', 'USSD', 'Fine-tuning'].map(tag => (
                <button
                  key={tag}
                  onClick={() => setSearchQuery(tag)}
                  className="bg-white/10 hover:bg-white/20 text-white px-5 py-2 rounded-xl text-xs font-black transition-all border border-white/10 backdrop-blur-md"
                >
                  #{tag}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
