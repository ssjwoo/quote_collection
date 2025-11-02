import { createContext, useContext, useEffect, useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";
import { AlertModal } from "../components/Modal/AlertModal";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [sevError, setSevError] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error,setError] = useState(false);
  const [alertMessage, setAlertMessage] = useState("");
  const [alertOpen, setAlertOpen] = useState(false);

  const showAlert = (message) => {
    setAlertMessage(message);
    setAlertOpen(true);
  };

  const closeAlert = () => setAlertOpen(false);

  const navigation = useNavigate();

  const login = async (email, password) => {
    try {
      const response = await axios.post(
        "/auth/login",
        new URLSearchParams({
          username: email,
          password: password,
        }),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      localStorage.setItem("accessToken", response.data.access_token);
      setError(false);
      await verifyJWT(); // Re-verify to set user and isAuthenticated state
      navigation("/");
      return true;
    } catch (error) {
      console.log(error.message);
      setError(true);
      // alert("아이디/혹은 비밀번호가 일치하지 않습니다.");
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    setIsAuthenticated(false);
    setUser(null);
    // alert("로그아웃 되었습니다.");
    showAlert("로그아웃 되었습니다.")
    navigation("/");
  };

  const signup = async ({ email, username, password }) => {
    try {
      const response = await axios.post("/auth/register", {
        email,
        username,
        password,
      });

      if (response.status === 200) {
        // alert("회원가입이 완료되었습니다.");
        showAlert("회원가입이 완료되었습니다.");
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
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setIsLoading(false);
      setIsAuthenticated(false);
      setUser(null);
      return false;
    }

    try {
      const response = await axios.get("/auth/me");
      setIsAuthenticated(true);
      setUser(response.data);
      return true;
    } catch (error) {
      if (error.response?.status === 401) {
        const detail = error.response.data?.detail;
        if (detail === "token_expired") {
          alert("세션이 만료되었습니다. 다시 로그인 해주세요.");
          logout();
        }
      }
      setIsAuthenticated(false);
      setUser(null);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    setIsLoading(true);
    console.log("[AuthProvider] Initializing... Running verifyJWT.");
    verifyJWT();
    setError(false);
  }, []);

  console.log("[AuthProvider] Rendering with state:", {
    isLoading,
    isAuthenticated,
    user,
  });

  return (
    <AuthContext.Provider
      value={{
        sevError,
        isAuthenticated,
        signup,
        user,
        logout,
        login,
        isLoading,
        error,
        setError,
        showAlert,
      }}
    >
      {children}

    <AlertModal open={alertOpen} onClose={closeAlert} message={alertMessage} />
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
