import { useQuery } from '@tanstack/react-query';
import { api, queryKeys } from '../lib/api';

export const useProperties = (params?: {
  skip?: number;
  limit?: number;
  property_type?: 'BUY' | 'SELL' | 'RENT';
  min_price?: number;
  max_price?: number;
  min_bedrooms?: number;
  city?: string;
  search?: string;
  is_featured?: boolean;
}) => {
  return useQuery({
    queryKey: [...queryKeys.properties, params],
    queryFn: () => api.getProperties(params),
  });
};

export const useProperty = (id: number) => {
  return useQuery({
    queryKey: queryKeys.property(id),
    queryFn: () => api.getProperty(id),
    enabled: !!id,
  });
};

export const usePropertyBySlug = (slug: string) => {
  return useQuery({
    queryKey: queryKeys.propertyBySlug(slug),
    queryFn: () => api.getPropertyBySlug(slug),
    enabled: !!slug,
  });
};
