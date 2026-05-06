import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [formData, setFormData] = useState({
    full_name: "",
    land_size_acres: "",
  });

  // Sync formData with user data whenever user changes or editing starts
  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user?.full_name || "",
        land_size_acres: user?.land_size_acres || "",
      });
    }
  }, [user]);

  // Reset message after 3 seconds
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => setMessage(""), 3000);
      return () => clearTimeout(timer);
    }
  }, [message]);

  const handleEditToggle = () => {
    if (editing) {
      // If canceling edit, reset formData to user data
      setFormData({
        full_name: user?.full_name || "",
        land_size_acres: user?.land_size_acres || "",
      });
    }
    setEditing(!editing);
  };

  const handleSaveChanges = async () => {
    if (!formData.full_name.trim()) {
      setMessage("Name cannot be empty");
      return;
    }

    setSaving(true);
    const result = await updateUser({
      full_name: formData.full_name.trim(),
      land_size_acres: parseFloat(formData.land_size_acres) || 0,
    });
    setSaving(false);

    if (result.success) {
      setMessage("Profile updated successfully!");
      setEditing(false);
    } else {
      setMessage(result.error || "Failed to update profile");
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">My Profile</h1>
        <p className="text-gray-500 mt-1">Manage your account details</p>
      </div>

      {/* Edit/Save Button */}
      <div className="flex justify-between items-center">
        <div className="flex-1">
          {message && (
            <div
              className={`p-3 rounded-lg text-sm font-medium ${
                message.includes("success")
                  ? "bg-green-100 text-green-800"
                  : "bg-red-100 text-red-800"
              }`}
            >
              {message}
            </div>
          )}
        </div>
        <button
          onClick={handleEditToggle}
          className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
            editing
              ? "bg-gray-300 text-gray-700 hover:bg-gray-400"
              : "bg-primary-600 text-white hover:bg-primary-700"
          }`}
        >
          {editing ? "Cancel" : "Edit Profile"}
        </button>
      </div>

      {/* Profile Card */}
      <div className="card">
        <div className="flex items-center space-x-6 pb-6 border-b">
          <div className="w-24 h-24 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
            <span className="text-4xl font-bold text-white">
              {(
                formData.full_name?.charAt(0) ||
                user?.full_name?.charAt(0) ||
                ""
              ).toUpperCase()}
            </span>
          </div>
          <div>
            {editing ? (
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) =>
                  setFormData({ ...formData, full_name: e.target.value })
                }
                className="text-2xl font-bold text-gray-800 px-2 py-1 border border-gray-300 rounded mb-2 w-full"
              />
            ) : (
              <h2 className="text-2xl font-bold text-gray-800">
                {user?.full_name}
              </h2>
            )}
            <p className="text-primary-600 font-medium">{user?.farmer_id}</p>
            <p className="text-gray-500 mt-1">
              {user?.state}, {user?.district}
            </p>
          </div>
        </div>

        <div className="pt-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">
                Full Name
              </label>
              {editing ? (
                <input
                  type="text"
                  value={formData.full_name}
                  onChange={(e) =>
                    setFormData({ ...formData, full_name: e.target.value })
                  }
                  className="text-lg text-gray-800 px-3 py-2 border border-gray-300 rounded w-full focus:outline-none focus:border-primary-600"
                />
              ) : (
                <p className="text-lg text-gray-800">{user?.full_name}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">
                Mobile Number
              </label>
              <p className="text-lg text-gray-800">{user?.mobile}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">
                Aadhar Number
              </label>
              <p className="text-lg text-gray-800">
                {user?.aadhar_number
                  ? `${user.aadhar_number.slice(0, 4)} ${user.aadhar_number.slice(4, 8)} ${user.aadhar_number.slice(8, 12)}`
                  : "Not provided"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">
                State
              </label>
              <p className="text-lg text-gray-800">{user?.state}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">
                District
              </label>
              <p className="text-lg text-gray-800">{user?.district}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">
                Village
              </label>
              <p className="text-lg text-gray-800">
                {user?.village || "Not specified"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">
                Land Size (Acres)
              </label>
              {editing ? (
                <input
                  type="number"
                  value={formData.land_size_acres}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      land_size_acres: e.target.value,
                    })
                  }
                  className="text-lg text-gray-800 px-3 py-2 border border-gray-300 rounded w-full focus:outline-none focus:border-primary-600"
                  placeholder="Enter land size"
                />
              ) : (
                <p className="text-lg text-gray-800">
                  {user?.land_size_acres
                    ? `${user.land_size_acres} Acres`
                    : "Not specified"}
                </p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">
                Farmer ID
              </label>
              <p className="text-lg text-primary-600 font-medium">
                {user?.farmer_id}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-1">
                Member Since
              </label>
              <p className="text-lg text-gray-800">
                {user?.created_at
                  ? new Date(user.created_at).toLocaleDateString("en-IN", {
                      day: "numeric",
                      month: "long",
                      year: "numeric",
                    })
                  : "-"}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card bg-primary-50 border-primary-200">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <svg
                className="w-6 h-6 text-primary-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                />
              </svg>
            </div>
            <div>
              <p className="text-sm text-primary-600">Account Status</p>
              <p className="font-semibold text-primary-700">Verified</p>
            </div>
          </div>
        </div>

        <div className="card bg-earth-50 border-earth-200">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-earth-100 rounded-lg flex items-center justify-center">
              <svg
                className="w-6 h-6 text-earth-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064"
                />
              </svg>
            </div>
            <div>
              <p className="text-sm text-earth-600">Land Registered</p>
              <p className="font-semibold text-earth-700">
                {editing && formData.land_size_acres
                  ? `${formData.land_size_acres} Acres`
                  : user?.land_size_acres
                    ? `${user.land_size_acres} Acres`
                    : "Not Set"}
              </p>
            </div>
          </div>
        </div>

        <div className="card bg-blue-50 border-blue-200">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg
                className="w-6 h-6 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                />
              </svg>
            </div>
            <div>
              <p className="text-sm text-blue-600">Location</p>
              <p className="font-semibold text-blue-700">
                {user?.district}, {user?.state}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Farmer ID Card */}
      <div className="card bg-gradient-to-br from-primary-600 to-primary-700 text-white">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-primary-200 text-sm">Digital Farmer ID Card</p>
            <h3 className="text-2xl font-bold mt-2">
              {editing ? formData.full_name : user?.full_name}
            </h3>
            <p className="text-primary-100 mt-1">{user?.farmer_id}</p>
            <div className="mt-4 space-y-1">
              <p className="text-sm text-primary-200">
                <span className="text-white font-medium">State:</span>{" "}
                {user?.state}
              </p>
              <p className="text-sm text-primary-200">
                <span className="text-white font-medium">District:</span>{" "}
                {user?.district}
              </p>
              {user?.village && (
                <p className="text-sm text-primary-200">
                  <span className="text-white font-medium">Village:</span>{" "}
                  {user?.village}
                </p>
              )}
              {user?.aadhar_number && (
                <p className="text-sm text-primary-200">
                  <span className="text-white font-medium">Aadhar:</span>{" "}
                  {user.aadhar_number.slice(0, 4)}{" "}
                  {user.aadhar_number.slice(4, 8)}{" "}
                  {user.aadhar_number.slice(8, 12)}
                </p>
              )}
            </div>
          </div>
          <div className="hidden md:block">
            <div className="w-24 h-24 bg-white/20 rounded-xl flex items-center justify-center">
              <svg
                className="w-16 h-16 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-primary-500">
          <p className="text-xs text-primary-200">Valid Digital ID</p>
        </div>
      </div>

      {/* Save Button when editing */}
      {editing && (
        <div className="flex justify-end gap-4 mt-6">
          <button
            onClick={handleSaveChanges}
            disabled={saving}
            className="px-6 py-2 rounded-lg font-semibold bg-primary-600 text-white hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? "Saving..." : "Save Changes"}
          </button>
        </div>
      )}
    </div>
  );
};

export default Profile;
