import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { usePropertyBySlug } from '../hooks/useProperties';
import { api } from '../lib/api';

const PropertyDetail = () => {
  const { slug } = useParams<{ slug: string }>();
  const { data: property, isLoading, error } = usePropertyBySlug(slug!);

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitMessage('');

    try {
      await api.createInquiry({
        name: formData.name,
        email: formData.email,
        phone: formData.phone || undefined,
        message: formData.message,
        property_id: property?.id,
      });

      setSubmitMessage('Thank you! Your inquiry has been sent successfully.');
      setFormData({ name: '', email: '', phone: '', message: '' });
    } catch (error) {
      setSubmitMessage('Sorry, there was an error sending your inquiry. Please try again.');
    }

    setIsSubmitting(false);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !property) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">Property not found or error loading property details.</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{property.title}</h1>
        <p className="text-gray-600">{property.city}, {property.state}</p>
      </div>

      {/* Image Gallery */}
      {property.images && property.images.length > 0 && (
        <div className="mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {property.images.map((image: any) => (
              <img
                key={image.id}
                src={image.url}
                alt={image.caption || property.title}
                className="w-full h-64 object-cover rounded-lg"
              />
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Details */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-semibold mb-4">Property Details</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{property.bedrooms}</div>
                <div className="text-sm text-gray-600">Bedrooms</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{property.bathrooms}</div>
                <div className="text-sm text-gray-600">Bathrooms</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{property.area}</div>
                <div className="text-sm text-gray-600">Sq Ft</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">
                  {property.property_type}
                </div>
                <div className="text-sm text-gray-600">Type</div>
              </div>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">Description</h3>
              <p className="text-gray-700">{property.description}</p>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">Features</h3>
              <div className="flex flex-wrap gap-2">
                {property.parking && (
                  <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                    Parking
                  </span>
                )}
                {property.furnished && (
                  <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                    Furnished
                  </span>
                )}
                {property.is_featured && (
                  <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                    Featured
                  </span>
                )}
                {property.is_special_offer && (
                  <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">
                    Special Offer
                  </span>
                )}
              </div>
            </div>

            {property.address && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-2">Address</h3>
                <p className="text-gray-700">{property.address}</p>
                {property.zip_code && <p className="text-gray-700">{property.zip_code}</p>}
              </div>
            )}

            {property.gmap_url && (
              <div className="mb-6">
                <a
                  href={property.gmap_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  View on Google Maps
                </a>
              </div>
            )}
          </div>
        </div>

        {/* Contact Form Sidebar */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6 sticky top-6">
            <h3 className="text-xl font-semibold mb-4">Contact Agent</h3>
            <div className="mb-4">
              <div className="text-3xl font-bold text-gray-900 mb-2">
                ₹{property.price.toLocaleString()}
              </div>
              <div className="text-sm text-gray-600">
                {property.property_type === 'RENT' ? 'per month' : 'total price'}
              </div>
            </div>

            {submitMessage && (
              <div className={`mb-4 p-3 rounded-lg ${
                submitMessage.includes('error') || submitMessage.includes('Sorry')
                  ? 'bg-red-50 text-red-700 border border-red-200'
                  : 'bg-green-50 text-green-700 border border-green-200'
              }`}>
                {submitMessage}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <input
                  type="text"
                  name="name"
                  placeholder="Your Name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <input
                  type="email"
                  name="email"
                  placeholder="Your Email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <input
                  type="tel"
                  name="phone"
                  placeholder="Your Phone (optional)"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <textarea
                  name="message"
                  placeholder="Your Message"
                  rows={4}
                  value={formData.message}
                  onChange={handleInputChange}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                ></textarea>
              </div>
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Sending...' : 'Send Inquiry'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PropertyDetail;
