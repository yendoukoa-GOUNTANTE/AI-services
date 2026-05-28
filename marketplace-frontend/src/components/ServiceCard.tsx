import React from 'react';
import { CreditCard, Zap, Bot, Layout } from 'lucide-react';
import { AIService } from '../types';

interface ServiceCardProps {
  service: AIService;
  onLaunch: (service: AIService) => void;
  isStoreItem?: boolean;
}

const ServiceCard: React.FC<ServiceCardProps> = ({ service, onLaunch, isStoreItem }) => {
  const Icon = service.icon;

  if (service.featured && !isStoreItem) {
    return (
      <div className="group relative bg-white border-2 border-blue-600 rounded-3xl overflow-hidden shadow-xl transform transition-all hover:-translate-y-2 hover:shadow-2xl">
        <div className="p-8">
          <div className="flex items-center justify-between mb-8">
            <div className="p-5 bg-blue-600 rounded-2xl text-white shadow-lg shadow-blue-200 group-hover:scale-110 transition-transform">
              <Icon size={32} />
            </div>
            <div className="flex items-center bg-blue-100 text-blue-700 px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest border border-blue-200">
              <Zap size={10} className="mr-1.5 fill-current" /> Core Agent
            </div>
          </div>
          <h3 className="text-2xl font-black text-gray-900 mb-3 tracking-tight">
            {service.name}
          </h3>
          <p className="text-gray-500 text-sm line-clamp-3 mb-10 font-medium leading-relaxed">
            {service.description}
          </p>
          <button
            onClick={() => onLaunch(service)}
            className="w-full bg-blue-600 text-white py-4 rounded-2xl text-sm font-black hover:bg-blue-700 transition-all shadow-xl shadow-blue-100 active:scale-95"
          >
            Launch Agent
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="group bg-white border border-gray-100 rounded-3xl overflow-hidden shadow-sm hover:shadow-2xl transition-all duration-500 hover:-translate-y-1 hover:border-blue-100">
      <div className="p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="p-4 bg-gray-50 rounded-2xl text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-all duration-300">
            <Icon size={24} />
          </div>
          <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest bg-gray-50 px-3 py-1.5 rounded-lg group-hover:text-blue-400 transition-colors">
            {service.category}
          </span>
        </div>
        <h3 className="text-xl font-black text-gray-900 group-hover:text-blue-600 transition-colors tracking-tight">
          {service.name}
        </h3>
        {isStoreItem && (
           <p className="mt-1 text-[10px] text-blue-600 font-black uppercase tracking-widest opacity-70">Community Asset</p>
        )}
        <p className="mt-4 text-sm text-gray-500 line-clamp-2 leading-relaxed font-medium">
          {service.description}
        </p>
        <div className="mt-8 pt-8 border-t border-gray-50 flex items-center justify-between">
          <div className="flex items-center text-gray-900">
             <CreditCard size={14} className="mr-2 text-blue-600" />
             <span className="text-sm font-black">{service.price || 50} <span className="text-[10px] text-gray-400 uppercase ml-0.5">Credits</span></span>
          </div>
          <button
            onClick={() => onLaunch(service)}
            className={`px-6 py-3 rounded-xl text-xs font-black transition-all shadow-md active:scale-95 ${
              service.type === 'design'
                ? 'bg-purple-600 text-white hover:bg-purple-700 shadow-purple-100'
                : 'bg-gray-900 text-white hover:bg-blue-600 shadow-gray-100'
            }`}
          >
            {service.type === 'design' ? 'Purchase Design' : 'Deploy Agent'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ServiceCard;
