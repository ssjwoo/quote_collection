import { createContext, useContext, useEffect, useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [sevError, setSevError] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const [user, setUser] = useState({});

  const navigation = useNavigate();

  const logout = () => {
    localStorage.removeItem("accessToken"); // Clear the token
    setIsAuthenticated(false);
    setUser(null);
    alert("로그아웃 되었습니다."); // Inform the user
    navigation("/login"); // Redirect to login page
  };

  const signup = async ({ email, username, password }) => {
    try {
      const response = await axios.post("/auth/register", {
        email,
        username,
        password,
      });

      if (response.status === 200) {
        alert("회원가입이 완료되었습니다.");
        return true;
      }

      if (response.status === 400) alert(response.data.detail);
      return false;
    } catch (error) {
      setSevError(error.response?.data.detail || "회원가입에 실패했습니다.");
      return false;
    }
  };

  const verifyJWT = async () => {
    try {
      const response = await axios.get("/auth/me");
      setIsAuthenticated(true);
      setUser(response.data);
      return true;
    } catch (error) {
      if (error.response?.status === 401) {
        // Changed from 404 to 401
        const detail = error.response.data?.detail;

        if (detail === "token_expired") {
          alert("세션이 만료되었습니다. 다시 로그인 해주세요.");
          logout(); // Call logout function
        }
      }
      setIsAuthenticated(false);
      setUser(null);
      return false;
    }
  };

  useEffect(() => {
    const checkAuth = async () => {
      // Define the async function
      await verifyJWT();
    };
    checkAuth(); // Call the async function
  }, []);

  return (
    <AuthContext.Provider
      value={{ sevError, isAuthenticated, signup, user, logout }}
    >
      {" "}
      // Add logout to value
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("context error");
  }
  return context;
};
