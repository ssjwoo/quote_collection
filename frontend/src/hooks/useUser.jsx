import { createContext, useContext } from "react";
import axios from "../api/axios";

const UserContext = createContext(null);

export const UserProvider = ({ children }) => {
  const getuser = async ({ userid }) => {
    try {
      const response = await axios.get("/api/users", {
        userid,
      });

      if (response.status === 200) {
        return response.data;
      }

      if (response.status === 404) alert(response.data.detail);
      return false;
    } catch (error) {
      // setSevError(error.response?.data.detail || "회원정보 열람에 실패했습니다.");
      console.log(
        error.response?.data.detail || "회원정보 열람에 실패했습니다."
      );
      return false;
    }
  };

  return (
    <UserContext.Provider value={{ getuser }}>{children}</UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("context error");
  }
  return context;
};
