import axios, { AxiosRequestConfig, AxiosError } from "axios";

// ============================================================
// HARDCODED BASE URL - CHANGE FOR PRODUCTION
// ============================================================
const API_BASE_URL = "http://localhost:8000";

// ============================================================
// AXIOS INSTANCE
// ============================================================
export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,                    // 10 second timeout
  withCredentials: false,            // No cookies needed
  headers: {
    "Content-Type": "application/json",
  },
});

// ============================================================
// REQUEST INTERCEPTOR (with logging)
// ============================================================
api.interceptors.request.use(
  (config) => {
    console.log(`📤 ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error("❌ Request setup failed:", error.message);
    return Promise.reject(error);
  }
);

// ============================================================
// RESPONSE INTERCEPTOR (with error handling)
// ============================================================
api.interceptors.response.use(
  (response) => {
    console.log(`✅ ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`);
    return response;
  },
  (error: AxiosError) => {
    // Log detailed error info
    if (error.response) {
      // Server responded with error status
      console.error(`❌ ${error.config?.method?.toUpperCase()} ${error.config?.url} - ${error.response.status}`);
      console.error("Response data:", error.response.data);
    } else if (error.request) {
      // Request made but no response received
      console.error("❌ No response from server:", error.message);
      console.error("Backend may not be running at:", API_BASE_URL);
    } else {
      // Error setting up request
      console.error("❌ Request error:", error.message);
    }

    // Auto logout on 401
    if (error.response?.status === 401 && typeof window !== "undefined") {
      console.log("🔒 Unauthorized - redirecting to login");
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

// ============================================================
// API CLIENT HELPERS
// ============================================================
export const apiClient = {
  get: async <T = any>(url: string, config?: AxiosRequestConfig) => {
    try {
      const res = await api.get<T>(url, config);
      return res.data;
    } catch (error) {
      console.error(`GET ${url} failed:`, error);
      throw error;
    }
  },

  post: async <T = any>(url: string, data?: any, config?: AxiosRequestConfig) => {
    try {
      const res = await api.post<T>(url, data, config);
      return res.data;
    } catch (error) {
      console.error(`POST ${url} failed:`, error);
      throw error;
    }
  },

  put: async <T = any>(url: string, data?: any, config?: AxiosRequestConfig) => {
    try {
      const res = await api.put<T>(url, data, config);
      return res.data;
    } catch (error) {
      console.error(`PUT ${url} failed:`, error);
      throw error;
    }
  },

  delete: async <T = any>(url: string, config?: AxiosRequestConfig) => {
    try {
      const res = await api.delete<T>(url, config);
      return res.data;
    } catch (error) {
      console.error(`DELETE ${url} failed:`, error);
      throw error;
    }
  },
};

// ============================================================
// TASK-SPECIFIC APIs
// ============================================================
export const taskAPI = {
  getTasks: () => apiClient.get("/dashboard/tasks"),
  createTask: (data: any) => apiClient.post("/dashboard/tasks", data),
  updateTask: (id: number, data: any) => apiClient.put(`/dashboard/tasks/${id}`, data),
  deleteTask: (id: number) => apiClient.delete(`/dashboard/tasks/${id}`),
};

// ============================================================
// UTILITY FUNCTIONS
// ============================================================
export const checkBackendHealth = async (): Promise<boolean> => {
  try {
    await api.get("/");
    return true;
  } catch {
    return false;
  }
};

export const getApiBaseUrl = (): string => API_BASE_URL;
