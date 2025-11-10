import axios from 'axios';

// In production behind nginx, use relative URLs. Otherwise use environment variable or default
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' ? '/api/v1' : 'http://localhost:8000/api/v1');

export interface SessionData {
  organization: string;
  user: string;
  configuration: string;
  version_of_software: string;
  session_info: string;
}

export const fetchSessionData = async (): Promise<SessionData> => {
  try {
    const response = await axios.get<SessionData>(`${API_BASE_URL}/session/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

