import { apiClient } from "./client";

export const getTraffic = (storeId: string, start: string, end: string) =>
  apiClient.get(`/analytics/${storeId}/traffic`, { params: { start, end } });

export const getDwellByZone = (storeId: string, start: string, end: string) =>
  apiClient.get(`/analytics/${storeId}/dwell`, { params: { start, end } });

export const getHeatmap = (storeId: string, start: string, end: string) =>
  apiClient.get(`/analytics/${storeId}/heatmap`, { params: { start, end } });

export const getRecommendations = (storeId: string) =>
  apiClient.get(`/recommendations/${storeId}/latest`);
