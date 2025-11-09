import React, { useState, useEffect } from 'react';
import TopMenu from '../components/TopMenu';
import { fetchSessionData, SessionData } from '../services/api';
import './Session.css';

const Session: React.FC = () => {
  const [sessionData, setSessionData] = useState<SessionData | null>(null);
  const [hasError, setHasError] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadSessionData = async () => {
      try {
        setIsLoading(true);
        const data = await fetchSessionData();
        setSessionData(data);
        setHasError(false);
      } catch (error) {
        console.error('Failed to fetch session data:', error);
        setHasError(true);
        setSessionData(null);
      } finally {
        setIsLoading(false);
      }
    };

    loadSessionData();
  }, []);

  const getDisplayData = (): SessionData => {
    if (hasError || !sessionData) {
      return {
        organization: 'unknown',
        user: 'unknown',
        configuration: 'unknown',
        version_of_software: 'unknown',
        session_info: 'unknown',
      };
    }
    return sessionData;
  };

  const displayData = getDisplayData();

  return (
    <div className="session-page">
      <TopMenu hasError={hasError} />
      <div className="session-content">
        <div className="session-container">
          <h2 className="session-title">Session Information</h2>
          {isLoading ? (
            <div className="loading">Loading...</div>
          ) : (
            <table className="session-table">
              <thead>
                <tr>
                  <th>Field</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="field-name">Organization</td>
                  <td className="field-value">{displayData.organization}</td>
                </tr>
                <tr>
                  <td className="field-name">User</td>
                  <td className="field-value">{displayData.user}</td>
                </tr>
                <tr>
                  <td className="field-name">Configuration</td>
                  <td className="field-value">{displayData.configuration}</td>
                </tr>
                <tr>
                  <td className="field-name">Version of Software</td>
                  <td className="field-value">{displayData.version_of_software}</td>
                </tr>
                <tr>
                  <td className="field-name">Session Info</td>
                  <td className="field-value">{displayData.session_info}</td>
                </tr>
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default Session;

