import React from 'react';

interface CategoryFilterProps {
  categories: string[];
  selectedCategory: string;
  onSelectCategory: (category: string) => void;
}

const CategoryFilter: React.FC<CategoryFilterProps> = ({ categories, selectedCategory, onSelectCategory }) => {
  return (
    <div className="flex space-x-2 overflow-x-auto pb-4 w-full md:w-auto no-scrollbar scroll-smooth">
      {categories.map(cat => (
        <button
          key={cat}
          onClick={() => onSelectCategory(cat)}
          className={`whitespace-nowrap px-8 py-3 rounded-2xl border-2 text-sm font-black transition-all duration-300 ${
            selectedCategory === cat
              ? 'bg-blue-600 text-white border-blue-600 shadow-xl shadow-blue-200 -translate-y-0.5'
              : 'bg-white text-gray-500 border-gray-100 hover:border-blue-200 hover:text-blue-600 hover:bg-blue-50/30'
          }`}
        >
          {cat}
        </button>
      ))}
    </div>
  );
};

export default CategoryFilter;
