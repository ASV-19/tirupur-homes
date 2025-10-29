import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useProperties } from '../hooks/useProperties';

const Properties = () => {
  const [filters, setFilters] = useState({
    property_type: '' as 'BUY' | 'SELL' | 'RENT' | '',
    min_price: '',
    max_price: '',
    min_bedrooms: '',
    city: '',
    search: '',
  });

  const { data: properties, isLoading, error } = useProperties({
    limit: 20,
    property_type: filters.property_type || undefined,
    min_price: filters.min_price ? parseInt(filters.min_price) : undefined,
    max_price: filters.max_price ? parseInt(filters.max_price) : undefined,
    min_bedrooms: filters.min_bedrooms ? parseInt(filters.min_bedrooms) : undefined,
    city: filters.city || undefined,
    search: filters.search || undefined,
  });

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">Error loading properties. Please try again later.</p>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Properties</h1>

      {/* Filters */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-semibold mb-4">Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <select
            value={filters.property_type}
            onChange={(e) => handleFilterChange('property_type', e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Types</option>
            <option value="BUY">Buy</option>
            <option value="RENT">Rent</option>
            <option value="SELL">Sell</option>
          </select>

          <input
            type="number"
            placeholder="Min Price"
            value={filters.min_price}
            onChange={(e) => handleFilterChange('min_price', e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <input
            type="number"
            placeholder="Max Price"
            value={filters.max_price}
            onChange={(e) => handleFilterChange('max_price', e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <input
            type="number"
            placeholder="Min Bedrooms"
            value={filters.min_bedrooms}
            onChange={(e) => handleFilterChange('min_bedrooms', e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <input
            type="text"
            placeholder="City"
            value={filters.city}
            onChange={(e) => handleFilterChange('city', e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <input
            type="text"
            placeholder="Search"
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Properties Grid */}
      {properties && properties.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {properties.map((property: any) => (
            <div key={property.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              {property.thumbnail && (
                <img
                  src={property.thumbnail}
                  alt={property.title}
                  className="w-full h-48 object-cover"
                />
              )}
              <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold text-gray-900">{property.title}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    property.property_type === 'BUY' ? 'bg-green-100 text-green-800' :
                    property.property_type === 'RENT' ? 'bg-blue-100 text-blue-800' :
                    'bg-purple-100 text-purple-800'
                  }`}>
                    {property.property_type}
                  </span>
                </div>
                <p className="text-gray-600 mb-2">{property.city}, {property.state}</p>
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span>{property.bedrooms} bed</span>
                  <span>{property.bathrooms} bath</span>
                  <span>{property.area} sq ft</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-gray-900">
                    ₹{property.price.toLocaleString()}
                  </span>
                  <Link
                    to={`/properties/${property.slug}`}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-600">No properties found matching your criteria.</p>
        </div>
      )}
    </div>
  );
};

export default Properties;
