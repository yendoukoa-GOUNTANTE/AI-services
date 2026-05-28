import { LucideIcon } from 'lucide-react';

export interface AIService {
  id: string | number;
  name: string;
  category: string;
  icon: LucideIcon;
  description: string;
  featured?: boolean;
  isStoreItem?: boolean;
  type?: 'agent' | 'design';
  price?: number;
}
