import axios from "axios";

export default {
  namespaced: true,
  state: {
    user: null,
    token: localStorage.getItem("token") || "",
    loading: false,
    error: null,
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
      localStorage.setItem("userid", user.id); // บันทึก userid แยก
      localStorage.setItem("username", user.username); // บันทึก username แยก
    },
    SET_TOKEN(state, token) {
      state.token = token;
      localStorage.setItem("token", token);
    },
    LOGOUT(state) {
      state.user = null;
      state.token = "";
      localStorage.removeItem("token");
      localStorage.removeItem("userid"); // ลบ userid
      localStorage.removeItem("username"); // ลบ username
    },
    SET_LOADING(state, loading) {
      state.loading = loading;
    },
    SET_ERROR(state, error) {
      state.error = error;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      commit("SET_LOADING", true);
      try {
        const response = await axios.post("http://localhost:5000/api/login", credentials);
        commit("SET_USER", response.data.user);
        commit("SET_TOKEN", response.data.token);
        commit("SET_ERROR", null);
        return response;
      } catch (error) {
        const errorMessage = error.response?.data?.message || "Login failed, please try again.";
        commit("SET_ERROR", errorMessage);
        throw new Error(errorMessage);
      } finally {
        commit("SET_LOADING", false);
      }
    },
    async signup({ commit }, userData) {
      commit("SET_LOADING", true);
      try {
        const response = await axios.post("http://localhost:5000/api/signup", userData);
        commit("SET_USER", response.data.user);
        commit("SET_TOKEN", response.data.token);
        commit("SET_ERROR", null);
        return response;
      } catch (error) {
        const errorMessage = error.response?.data?.message || "Signup failed, please try again.";
        commit("SET_ERROR", errorMessage);
        throw new Error(errorMessage);
      } finally {
        commit("SET_LOADING", false);
      }
    },
    logout({ commit }) {
      try {
        commit("LOGOUT");
        commit("SET_ERROR", null);
      } catch (error) {
        commit("SET_ERROR", "Logout failed, please try again.");
      }
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
    getUser: (state) => {
      return {
        id: state.user?.id, 
        username: state.user?.username, 
      };
    },
    getToken: (state) => state.token,
    isLoading: (state) => state.loading,
    getError: (state) => state.error,
  },
};