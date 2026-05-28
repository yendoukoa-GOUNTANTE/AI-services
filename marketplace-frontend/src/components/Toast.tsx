import React from 'react';
import { CheckCircle2, AlertCircle, X, Info } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'info';

interface ToastProps {
  message: string;
  type: ToastType;
  onClose: () => void;
}

const Toast: React.FC<ToastProps> = ({ message, type, onClose }) => {
  const bgColor = {
    success: 'bg-green-600',
    error: 'bg-red-600',
    info: 'bg-blue-600'
  }[type];

  const Icon = {
    success: CheckCircle2,
    error: AlertCircle,
    info: Info
  }[type];

  return (
    <div className="fixed bottom-8 right-8 z-[100] animate-slide-up">
      <div className={`${bgColor} text-white px-6 py-4 rounded-[20px] shadow-2xl flex items-center space-x-3 min-w-[300px]`}>
        <Icon size={20} />
        <span className="font-bold text-sm flex-1">{message}</span>
        <button onClick={onClose} className="p-1 hover:bg-white/20 rounded-lg transition-colors">
          <X size={16} />
        </button>
      </div>
    </div>
  );
};

export default Toast;
