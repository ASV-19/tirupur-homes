import { QueryClient } from '@tanstack/react-query';

// API Base URL
const API_BASE_URL = '/api/v1';

// Create query client
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// API Response types
export interface Property {
  id: number;
  title: string;
  slug: string;
  description: string;
  price: number;
  property_type: 'BUY' | 'SELL' | 'RENT';
  status: 'AVAILABLE' | 'SOLD' | 'RENTED' | 'PENDING';
  address?: string;
  city: string;
  state: string;
  zip_code?: string;
  bedrooms: number;
  bathrooms: number;
  area: number;
  parking: boolean;
  furnished: boolean;
  is_featured: boolean;
  is_special_offer?: boolean;
  offer_text?: string;
  latitude?: number;
  longitude?: number;
  images: PropertyImage[];
  created_at: string;
  updated_at?: string;
  gmap_url?: string;
  directions_url?: string;
  thumbnail?: string;
}

export interface PropertyImage {
  id: number;
  url: string;
  public_id?: string;
  caption?: string;
  order: number;
  uploaded_at: string;
}

export interface InquiryCreate {
  name: string;
  email: string;
  phone?: string;
  message: string;
  property_id?: number;
}

// API Functions
export const api = {
  // Properties
  async getProperties(params?: {
    skip?: number;
    limit?: number;
    property_type?: 'BUY' | 'SELL' | 'RENT';
    min_price?: number;
    max_price?: number;
    min_bedrooms?: number;
    city?: string;
    search?: string;
    is_featured?: boolean;
  }) {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.set(key, value.toString());
        }
      });
    }

    const response = await fetch(`${API_BASE_URL}/properties?${searchParams}`);
    if (!response.ok) throw new Error('Failed to fetch properties');
    return response.json();
  },

  async getProperty(id: number): Promise<Property> {
    const response = await fetch(`${API_BASE_URL}/properties/${id}`);
    if (!response.ok) throw new Error('Failed to fetch property');
    return response.json();
  },

  async getPropertyBySlug(slug: string): Promise<Property> {
    const response = await fetch(`${API_BASE_URL}/properties/slug/${slug}`);
    if (!response.ok) throw new Error('Failed to fetch property');
    return response.json();
  },

  // Inquiries
  async createInquiry(inquiry: InquiryCreate) {
    const response = await fetch(`${API_BASE_URL}/inquiries`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(inquiry),
    });
    if (!response.ok) throw new Error('Failed to create inquiry');
    return response.json();
  },
};

// Query keys for React Query
export const queryKeys = {
  properties: ['properties'] as const,
  property: (id: number) => ['properties', id] as const,
  propertyBySlug: (slug: string) => ['properties', 'slug', slug] as const,
};
