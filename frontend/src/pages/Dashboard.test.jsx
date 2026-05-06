import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from './Dashboard';

// Mock the AuthContext
const mockUser = {
  full_name: 'Test Farmer',
  farmer_id: 'KR-MH-2026-00001',
  land_size_acres: 5.5,
  district: 'Pune',
  created_at: '2024-01-01T00:00:00Z'
};

jest.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    user: mockUser
  })
}));

// Mock the API service
jest.mock('../services/api', () => ({
  getAnalysisHistory: jest.fn()
}));

describe('Dashboard Component', () => {
  test('renders welcome message with user name', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    expect(screen.getByText('Namaste, Test!')).toBeInTheDocument();
    expect(screen.getByText('Welcome to your Crop Management Dashboard')).toBeInTheDocument();
  });

  test('displays user stats correctly', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    expect(screen.getByText('Land Size')).toBeInTheDocument();
    expect(screen.getByText('5.5 Acres')).toBeInTheDocument();
    expect(screen.getByText('Location')).toBeInTheDocument();
    expect(screen.getByText('Pune')).toBeInTheDocument();
    expect(screen.getByText('Member Since')).toBeInTheDocument();
  });

  test('displays quick action buttons', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    expect(screen.getByText('New Crop Analysis')).toBeInTheDocument();
    expect(screen.getByText('View History')).toBeInTheDocument();
    expect(screen.getByText('Update Profile')).toBeInTheDocument();
  });

  test('displays farmer ID correctly', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    expect(screen.getByText('KR-MH-2026-00001')).toBeInTheDocument();
  });

  test('renders recent analyses section', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    expect(screen.getByText('Recent Analyses')).toBeInTheDocument();
    expect(screen.getByText('View All')).toBeInTheDocument();
  });
});