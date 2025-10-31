import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useProperties } from '../hooks/useProperties';
import LoginSignupModal from '../components/LoginSignupModal';
import { useAuth } from '../contexts/AuthContext';

const Home = () => {
  const { isAuthenticated, user } = useAuth();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { data: featuredProperties, isLoading } = useProperties({
    limit: 6,
    is_featured: true,
  });

  return (
    <div>
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Welcome to Tirupur Homes
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Find your perfect property in Tirupur, Tamil Nadu
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            to="/properties"
            className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors text-lg font-medium"
          >
            Browse All Properties
          </Link>
          {!isAuthenticated ? (
            <button
              onClick={() => setIsModalOpen(true)}
              className="bg-white text-blue-600 border-2 border-blue-600 px-8 py-3 rounded-lg hover:bg-blue-50 transition-colors text-lg font-medium"
            >
              Sign In / Sign Up
            </button>
          ) : (
            <div className="text-lg text-gray-700">
              Welcome back, {user?.name}!
            </div>
          )}
        </div>
      </div>

      {/* Featured Properties */}
      <div className="mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Featured Properties</h2>

        {isLoading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : featuredProperties && featuredProperties.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredProperties.map((property: any) => (
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
            <p className="text-gray-600">No featured properties available at the moment.</p>
          </div>
        )}
      </div>

      {/* Quick Search */}
      <div className="bg-gray-100 rounded-lg p-8 text-center">
        <h2 className="text-2xl font-semibold mb-4">Quick Property Search</h2>
        <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-2xl mx-auto">
          <a
            href="/properties?property_type=BUY"
            className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors font-medium"
          >
            Buy Properties
          </a>
          <a
            href="/properties?property_type=RENT"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Rent Properties
          </a>
          <a
            href="/properties?city=Tirupur"
            className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors font-medium"
          >
            Properties in Tirupur
          </a>
        </div>
      </div>

      <LoginSignupModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};

export default Home;
