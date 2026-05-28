import React from 'react';
import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  maxWidth?: string;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children, maxWidth = 'max-w-2xl' }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[60] overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 transition-opacity" aria-hidden="true" onClick={onClose}>
          <div className="absolute inset-0 bg-gray-900/60 backdrop-blur-sm opacity-100 transition-opacity"></div>
        </div>
        <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div className={`relative inline-block align-bottom bg-white rounded-3xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle ${maxWidth} w-full z-[70] border border-gray-100`}>
          <div className="bg-white px-6 pt-6 pb-4 sm:p-8 sm:pb-6">
            <div className="flex items-center justify-between mb-8">
              <h3 className="text-2xl font-black text-gray-900 tracking-tight uppercase tracking-widest text-sm">
                {title}
              </h3>
              <button
                onClick={onClose}
                className="p-2 text-gray-400 hover:text-gray-900 hover:bg-gray-50 rounded-xl transition-all"
              >
                <X size={24} />
              </button>
            </div>
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
