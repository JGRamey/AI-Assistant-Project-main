import axios from 'axios';
import { supabase } from './supabase';

const api = axios.create({
  baseURL: 'https://your-api-gateway-id-id.execute-api.us-east-1.amazonaws.com/prod',
});

api.interceptors.request.use(async (config) => {
  const { data: { session } } = await supabase.auth.getSession();
  if (session) {
    config.headers.Authorization = `Bearer ${session.access_token}`;
  }
  return config;
});

export const fetchTabData = async (tab, userId) => {
  try {
    const response = await api.post('', {
      data: 'dashboard',
      task: 'fetch_tab_data',
      tab,
      user_id: userId
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching tab data:', error);
    return {};
  }
};

export const triggerAgent = async (action, data) => {
  try {
    const response = await api.post('', {
      action:,
      ...data
    });
    return response.data;
  } catch (error) {
    return { status: 'error', result: error.message };
  }
};