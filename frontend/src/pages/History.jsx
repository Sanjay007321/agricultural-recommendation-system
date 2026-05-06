import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { analysisAPI } from '../services/api';

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await analysisAPI.getHistory();
      setHistory(response.data);
    } catch (err) {
      console.error('Failed to load history');
    }
    setLoading(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Analysis History</h1>
          <p className="text-gray-500 mt-1">View all your past crop recommendations</p>
        </div>
        <Link to="/analyze" className="btn-primary">New Recommendation</Link>
      </div>

      {history.length > 0 ? (
        <div className="card">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-4 px-4 text-sm font-medium text-gray-500">Analysis ID</th>
                  <th className="text-left py-4 px-4 text-sm font-medium text-gray-500">Recommended Crop</th>
                  <th className="text-left py-4 px-4 text-sm font-medium text-gray-500">Net Profit</th>
                  <th className="text-left py-4 px-4 text-sm font-medium text-gray-500">Date</th>
                  <th className="text-left py-4 px-4 text-sm font-medium text-gray-500">Action</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.analysis_id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-4">
                      <span className="font-medium text-gray-800">{item.analysis_id}</span>
                    </td>
                    <td className="py-4 px-4">
                      <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium">
                        {item.crop}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <span className={`font-semibold ${item.profit > 0 ? 'text-green-600' : 'text-red-600'}`}>
                        Rs. {item.profit?.toLocaleString('en-IN')}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-gray-500">
                      {new Date(item.created_at).toLocaleDateString('en-IN', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </td>
                    <td className="py-4 px-4">
                      <Link
                        to={`/results/${item.analysis_id}`}
                        className="inline-flex items-center space-x-1 text-primary-600 hover:text-primary-700 font-medium"
                      >
                        <span>View Details</span>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="card text-center py-12">
          <svg className="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 className="text-lg font-medium text-gray-700 mb-2">No Analysis History</h3>
          <p className="text-gray-500 mb-6 font-medium tracking-wide">You haven't received any crop recommendations yet.</p>
          <Link to="/analyze" className="btn-primary inline-block">
            Get Your First Recommendation
          </Link>
        </div>
      )}

      {history.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="stat-card border-primary-500">
            <p className="text-sm text-gray-500">Total Analyses</p>
            <p className="text-2xl font-bold text-gray-800 mt-1">{history.length}</p>
          </div>
          <div className="stat-card border-green-500">
            <p className="text-sm text-gray-500">Highest Profit</p>
            <p className="text-2xl font-bold text-green-600 mt-1">
              Rs. {Math.max(...history.map(h => h.profit || 0)).toLocaleString('en-IN')}
            </p>
          </div>
          <div className="stat-card border-earth-500">
            <p className="text-sm text-gray-500">Most Analyzed Crop</p>
            <p className="text-2xl font-bold text-gray-800 mt-1">
              {history.length > 0 ? 
                Object.entries(history.reduce((acc, h) => {
                  acc[h.crop] = (acc[h.crop] || 0) + 1;
                  return acc;
                }, {})).sort((a, b) => b[1] - a[1])[0]?.[0] || '-'
              : '-'}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default History;
