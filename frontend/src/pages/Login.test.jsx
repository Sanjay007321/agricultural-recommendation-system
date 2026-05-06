import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from './Login';

// Mock the AuthContext
const mockLogin = jest.fn();
jest.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    login: mockLogin
  })
}));

// Mock useNavigate
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate
}));

describe('Login Component', () => {
  beforeEach(() => {
    mockLogin.mockClear();
    mockNavigate.mockClear();
  });

  test('renders login form correctly', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    expect(screen.getByText('Welcome Back')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your mobile number')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Login/i })).toBeInTheDocument();
  });

  test('allows entering mobile number and password', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    const mobileInput = screen.getByPlaceholderText('Enter your mobile number');
    const passwordInput = screen.getByPlaceholderText('Enter your password');

    fireEvent.change(mobileInput, { target: { value: '9999999999' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    expect(mobileInput.value).toBe('9999999999');
    expect(passwordInput.value).toBe('password123');
  });

  test('shows error message when login fails', async () => {
    mockLogin.mockResolvedValue({
      success: false,
      error: 'Invalid credentials'
    });

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    const mobileInput = screen.getByPlaceholderText('Enter your mobile number');
    const passwordInput = screen.getByPlaceholderText('Enter your password');
    const submitButton = screen.getByRole('button', { name: /Login/i });

    fireEvent.change(mobileInput, { target: { value: '9999999999' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });
    fireEvent.click(submitButton);

    // Wait for async operation
    await screen.findByText('Invalid credentials');
  });

  test('navigates to dashboard on successful login', async () => {
    mockLogin.mockResolvedValue({
      success: true
    });

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    const mobileInput = screen.getByPlaceholderText('Enter your mobile number');
    const passwordInput = screen.getByPlaceholderText('Enter your password');
    const submitButton = screen.getByRole('button', { name: /Login/i });

    fireEvent.change(mobileInput, { target: { value: '9999999999' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    // Wait for navigation
    expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
  });

  test('displays loading spinner during login', async () => {
    mockLogin.mockImplementation(() => new Promise(resolve => {
      setTimeout(() => resolve({ success: true }), 100);
    }));

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    const submitButton = screen.getByRole('button', { name: /Login/i });
    fireEvent.click(submitButton);

    // Button should be disabled during loading
    expect(submitButton).toBeDisabled();
  });
});